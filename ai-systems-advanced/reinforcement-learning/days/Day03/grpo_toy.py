from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Literal, Tuple

import numpy as np


RewardMode = Literal["sparse", "dense", "hackable", "hardened"]
RunMode = Literal["train", "eval"]


@dataclass(frozen=True)
class ToyItem:
    prompt: str
    target: List[int]


@dataclass(frozen=True)
class Config:
    seed: int = 7
    n_prompts: int = 8
    seq_len: int = 3
    vocab: str = "0123"
    group_size: int = 16
    ppo_epochs: int = 4
    steps: int = 80
    lr: float = 0.35
    clip_eps: float = 0.2
    kl_beta: float = 0.05
    temperature: float = 1.0
    reward: RewardMode = "sparse"
    log_every: int = 5


def _softmax(logits: np.ndarray, temperature: float) -> np.ndarray:
    x = logits / max(temperature, 1e-9)
    x = x - np.max(x, axis=-1, keepdims=True)
    ex = np.exp(x)
    return ex / np.sum(ex, axis=-1, keepdims=True)


def _entropy(p: np.ndarray) -> float:
    p = np.clip(p, 1e-12, 1.0)
    return float(-np.sum(p * np.log(p), axis=-1).mean())


def _kl_per_position(p: np.ndarray, q: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    KL(p || q) and its gradient wrt logits that generate p via softmax.

    For categorical softmax logits z, p=softmax(z):
      d/dz KL(p||q) = p * ((log p - log q) - KL(p||q))  (per position)
    """
    p = np.clip(p, 1e-12, 1.0)
    q = np.clip(q, 1e-12, 1.0)
    log_ratio = np.log(p) - np.log(q)
    kl = np.sum(p * log_ratio, axis=-1)  # [...,]
    grad = p * (log_ratio - kl[..., None])  # [..., V]
    return kl, grad


def make_dataset(cfg: Config, rng: np.random.Generator) -> List[ToyItem]:
    vocab = cfg.vocab
    items: List[ToyItem] = []
    for i in range(cfg.n_prompts):
        target = [int(x) for x in rng.choice(list(vocab), size=cfg.seq_len, replace=True)]
        items.append(ToyItem(prompt=f"prompt_{i}", target=target))
    return items


def reward_fn(
    seq: np.ndarray, *, target: List[int], mode: RewardMode, hack_token: int
) -> float:
    correct = float(np.all(seq.tolist() == target))
    if mode == "sparse":
        return correct
    if mode == "dense":
        return float(np.mean(seq == np.asarray(target, dtype=np.int64)))

    # Intentionally hackable: reward gives a bonus for emitting a specific token anywhere.
    if mode == "hackable":
        bonus = 0.5 if int(hack_token) in set(int(x) for x in seq.tolist()) else 0.0
        return correct + bonus

    # Hardened: gate bonus behind correctness AND penalize hack token when wrong.
    if mode == "hardened":
        bonus = 0.5 if correct == 1.0 else 0.0
        penalty = 0.25 if (correct == 0.0 and int(hack_token) in set(int(x) for x in seq.tolist())) else 0.0
        return correct + bonus - penalty

    raise ValueError(f"unknown reward mode: {mode}")


def sample_group(
    rng: np.random.Generator,
    logits_prompt: np.ndarray,  # [T,V]
    *,
    group_size: int,
    temperature: float,
) -> Tuple[np.ndarray, np.ndarray]:
    t, v = logits_prompt.shape
    probs = _softmax(logits_prompt, temperature=temperature)  # [T,V]
    seqs = np.zeros((group_size, t), dtype=np.int64)
    logps = np.zeros((group_size,), dtype=np.float64)
    for i in range(group_size):
        lp = 0.0
        for pos in range(t):
            tok = int(rng.choice(v, p=probs[pos]))
            seqs[i, pos] = tok
            lp += float(math.log(float(probs[pos, tok])))
        logps[i] = lp
    return seqs, logps


def logp_of_sequences(probs_prompt: np.ndarray, seqs: np.ndarray) -> np.ndarray:
    # probs_prompt: [T,V], seqs: [N,T]
    t = probs_prompt.shape[0]
    out = np.zeros((seqs.shape[0],), dtype=np.float64)
    for i in range(seqs.shape[0]):
        lp = 0.0
        for pos in range(t):
            tok = int(seqs[i, pos])
            lp += float(math.log(float(np.clip(probs_prompt[pos, tok], 1e-12, 1.0))))
        out[i] = lp
    return out


def grad_logp(probs_prompt: np.ndarray, seq: np.ndarray) -> np.ndarray:
    # ∂/∂logits log π(y) = one_hot(y) - p
    t, v = probs_prompt.shape
    g = np.zeros((t, v), dtype=np.float64)
    for pos in range(t):
        tok = int(seq[pos])
        g[pos, :] -= probs_prompt[pos, :]
        g[pos, tok] += 1.0
    return g


def ppo_clipped_objective_mask(ratio: np.ndarray, advantage: np.ndarray, clip_eps: float) -> np.ndarray:
    """
    Return mask indicating whether the unclipped term is active (gradient flows).

    PPO surrogate: min(r*A, clip(r)*A).
      - If A>0 and r>1+eps -> clipped (no grad from r*A)
      - If A<0 and r<1-eps -> clipped (no grad from r*A)
    """
    upper = 1.0 + clip_eps
    lower = 1.0 - clip_eps
    clipped = ((advantage >= 0.0) & (ratio > upper)) | ((advantage < 0.0) & (ratio < lower))
    return ~clipped


def evaluate(
    logits: np.ndarray,
    dataset: List[ToyItem],
    *,
    seed: int,
    n_samples: int = 64,
    temperature: float = 1.0,
    reward: RewardMode = "sparse",
    hack_token: int,
) -> Dict[str, float]:
    rng = np.random.default_rng(seed)
    total_reward = 0.0
    total_success = 0.0
    total_div = 0.0
    for pid, item in enumerate(dataset):
        seqs, _ = sample_group(rng, logits[pid], group_size=n_samples, temperature=temperature)
        rewards = np.array(
            [reward_fn(s, target=item.target, mode=reward, hack_token=hack_token) for s in seqs],
            dtype=np.float64,
        )
        total_reward += float(rewards.mean())
        total_success += float(np.mean([np.all(s.tolist() == item.target) for s in seqs]))
        uniq = {tuple(s.tolist()) for s in seqs}
        total_div += float(len(uniq)) / float(n_samples)

    probs = _softmax(logits, temperature=temperature)
    return {
        "reward_mean": total_reward / float(len(dataset)),
        "success_rate": total_success / float(len(dataset)),
        "entropy_mean": _entropy(probs),
        "diversity": total_div / float(len(dataset)),
    }


def train(cfg: Config) -> Dict[str, float]:
    rng = np.random.default_rng(cfg.seed)
    dataset = make_dataset(cfg, rng)

    n_prompts = len(dataset)
    seq_len = cfg.seq_len
    vocab_size = len(cfg.vocab)
    hack_token = vocab_size - 1  # last token

    logits = 0.01 * rng.normal(size=(n_prompts, seq_len, vocab_size)).astype(np.float64)
    ref_logits = logits.copy()
    ref_probs = _softmax(ref_logits, temperature=1.0)

    metrics_path = Path(__file__).resolve().parent / "eval" / "toy_metrics.jsonl"
    metrics_path.parent.mkdir(parents=True, exist_ok=True)

    baseline = evaluate(
        logits,
        dataset,
        seed=cfg.seed + 1,
        n_samples=64,
        temperature=cfg.temperature,
        reward=cfg.reward,
        hack_token=hack_token,
    )

    with metrics_path.open("w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "step": 0,
                    "phase": "baseline",
                    "baseline_reward_mean": baseline["reward_mean"],
                    "baseline_success_rate": baseline["success_rate"],
                    "baseline_entropy_mean": baseline["entropy_mean"],
                    "baseline_diversity": baseline["diversity"],
                }
            )
            + "\n"
        )

    for step in range(1, cfg.steps + 1):
        old_logits = logits.copy()

        # Batch: for each prompt, sample K sequences from old policy.
        batch: List[Dict[str, np.ndarray]] = []
        for pid, item in enumerate(dataset):
            seqs, logp_old = sample_group(
                rng, old_logits[pid], group_size=cfg.group_size, temperature=cfg.temperature
            )
            rewards = np.array(
                [reward_fn(s, target=item.target, mode=cfg.reward, hack_token=hack_token) for s in seqs],
                dtype=np.float64,
            )
            r_mean = float(rewards.mean())
            r_std = float(rewards.std())
            adv = rewards - r_mean
            if r_std > 1e-8:
                adv = adv / (r_std + 1e-8)
            batch.append(
                {
                    "pid": np.array([pid], dtype=np.int64),
                    "seqs": seqs,
                    "logp_old": logp_old,
                    "rewards": rewards,
                    "adv": adv,
                }
            )

        # PPO-style multiple epochs over the same samples.
        clipfracs: List[float] = []
        adv_means: List[float] = []
        adv_stds: List[float] = []
        reward_means: List[float] = []

        for _epoch in range(cfg.ppo_epochs):
            probs = _softmax(logits, temperature=1.0)  # policy distribution (no temp in training)
            grad = np.zeros_like(logits, dtype=np.float64)

            # Policy gradient term (clipped surrogate) — sequence-constant advantage.
            total_samples = 0
            clipped_samples = 0

            for group in batch:
                pid = int(group["pid"][0])
                seqs = group["seqs"]
                logp_old = group["logp_old"]
                adv = group["adv"]

                probs_prompt = probs[pid]  # [T,V]
                logp_new = logp_of_sequences(probs_prompt, seqs)
                ratio = np.exp(logp_new - logp_old)
                mask = ppo_clipped_objective_mask(ratio, adv, cfg.clip_eps)

                total_samples += int(seqs.shape[0])
                clipped_samples += int(np.sum(~mask))

                for i in range(seqs.shape[0]):
                    if not bool(mask[i]):
                        continue
                    g = grad_logp(probs_prompt, seqs[i])
                    grad[pid] += float(adv[i] * ratio[i]) * g

            clipfrac = float(clipped_samples) / float(max(total_samples, 1))
            clipfracs.append(clipfrac)

            # KL penalty term to reference (explicit, distribution-level).
            kl, kl_grad = _kl_per_position(probs, ref_probs)  # [P,T], [P,T,V]
            kl_mean = float(kl.mean())

            # Gradient ascent on: mean(surrogate) - kl_beta * mean(KL)
            grad /= float(max(total_samples, 1))
            grad -= cfg.kl_beta * (kl_grad / float(kl_grad.shape[0] * kl_grad.shape[1]))
            logits += cfg.lr * grad

            # Metrics for this epoch
            all_rewards = np.concatenate([g["rewards"] for g in batch], axis=0)
            all_adv = np.concatenate([g["adv"] for g in batch], axis=0)
            reward_means.append(float(all_rewards.mean()))
            adv_means.append(float(all_adv.mean()))
            adv_stds.append(float(all_adv.std()))

        if step % cfg.log_every == 0 or step == cfg.steps:
            eval_metrics = evaluate(
                logits,
                dataset,
                seed=cfg.seed + 2,
                n_samples=64,
                temperature=cfg.temperature,
                reward=cfg.reward,
                hack_token=hack_token,
            )
            probs_now = _softmax(logits, temperature=1.0)
            kl_now, _ = _kl_per_position(probs_now, ref_probs)
            row = {
                "step": step,
                "train_reward_mean": float(np.mean(reward_means)),
                "train_adv_mean": float(np.mean(adv_means)),
                "train_adv_std": float(np.mean(adv_stds)),
                "clipfrac": float(np.mean(clipfracs)),
                "kl_mean": float(kl_now.mean()),
                "entropy_mean": _entropy(probs_now),
                "eval_reward_mean": eval_metrics["reward_mean"],
                "eval_success_rate": eval_metrics["success_rate"],
                "eval_diversity": eval_metrics["diversity"],
            }
            with metrics_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row) + "\n")
            print(json.dumps(row))

    final = evaluate(
        logits,
        dataset,
        seed=cfg.seed + 3,
        n_samples=128,
        temperature=cfg.temperature,
        reward=cfg.reward,
        hack_token=hack_token,
    )
    return {"baseline": baseline, "final": final}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["train", "eval"], default="train")
    p.add_argument("--reward", choices=["sparse", "dense", "hackable", "hardened"], default="sparse")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--steps", type=int, default=80)
    p.add_argument("--group-size", type=int, default=16)
    p.add_argument("--ppo-epochs", type=int, default=4)
    p.add_argument("--lr", type=float, default=0.35)
    p.add_argument("--clip-eps", type=float, default=0.2)
    p.add_argument("--kl-beta", type=float, default=0.05)
    p.add_argument("--temperature", type=float, default=1.0)
    args = p.parse_args()

    cfg = Config(
        seed=args.seed,
        steps=args.steps,
        group_size=args.group_size,
        ppo_epochs=args.ppo_epochs,
        lr=args.lr,
        clip_eps=args.clip_eps,
        kl_beta=args.kl_beta,
        temperature=args.temperature,
        reward=args.reward,
    )

    rng = np.random.default_rng(cfg.seed)
    dataset = make_dataset(cfg, rng)
    vocab_size = len(cfg.vocab)
    hack_token = vocab_size - 1
    logits = 0.01 * rng.normal(size=(len(dataset), cfg.seq_len, vocab_size)).astype(np.float64)

    if args.mode == "eval":
        out = evaluate(
            logits,
            dataset,
            seed=cfg.seed + 100,
            n_samples=128,
            temperature=cfg.temperature,
            reward=cfg.reward,
            hack_token=hack_token,
        )
        print(json.dumps(out))
        return

    result = train(cfg)
    print("baseline:", result["baseline"])
    print("final:", result["final"])


if __name__ == "__main__":
    main()
