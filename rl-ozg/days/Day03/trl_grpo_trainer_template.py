"""
Template: GRPO fine-tuning with 🤗 TRL (GRPOTrainer).

This is intentionally a *skeleton* so you can adapt it to the exact `trl` version
you have installed (APIs move quickly). The learning goal is wiring:

dataset (prompts) -> generate K completions -> compute verifiable reward -> GRPO update -> log curves.

Pass/fail (for you):
1) You can point to where K is controlled.
2) You can point to where KL control is applied (or configured).
3) You can point to where reward is computed (and how it is anti-cheat).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Sequence


@dataclass(frozen=True)
class RunConfig:
    model_name_or_path: str
    train_jsonl: Path
    valid_jsonl: Path
    output_dir: Path
    group_size: int = 8
    kl_beta: float = 0.05
    clip_eps: float = 0.2
    learning_rate: float = 1e-5


def read_prompts_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def verifiable_reward(prompt: Dict[str, Any], completion_text: str) -> float:
    """
    Replace this with your RLVR grader.

    Rules of thumb:
    - deterministic
    - fail closed
    - anti-cheat checks (>=3)
    """
    # TODO: implement real grader (JSON schema + rule checks + anti-cheat).
    _ = prompt
    _ = completion_text
    return 0.0


def compute_rewards(prompts: Sequence[Dict[str, Any]], completions: Sequence[str]) -> List[float]:
    return [float(verifiable_reward(p, c)) for p, c in zip(prompts, completions)]


def main() -> None:
    # TODO: set these for your environment.
    cfg = RunConfig(
        model_name_or_path="Qwen/Qwen2.5-0.5B-Instruct",
        train_jsonl=Path("data/train.jsonl"),
        valid_jsonl=Path("data/valid.jsonl"),
        output_dir=Path("runs/grpo"),
    )

    try:
        import torch  # noqa: F401
        from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: F401
        from trl import GRPOTrainer  # noqa: F401
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Missing deps. Install in your own env: pip install torch transformers datasets trl accelerate peft"
        ) from e

    # PSEUDOCODE (adapt to your TRL version):
    #
    # tokenizer = AutoTokenizer.from_pretrained(cfg.model_name_or_path)
    # model = AutoModelForCausalLM.from_pretrained(cfg.model_name_or_path, ...)
    #
    # train_rows = read_prompts_jsonl(cfg.train_jsonl)
    # valid_rows = read_prompts_jsonl(cfg.valid_jsonl)
    #
    # trainer = GRPOTrainer(
    #     model=model,
    #     tokenizer=tokenizer,
    #     train_dataset=train_rows,
    #     eval_dataset=valid_rows,
    #     reward_fn=compute_rewards,  # (prompts, completions) -> rewards
    #     group_size=cfg.group_size,  # K
    #     kl_beta=cfg.kl_beta,
    #     clip_range=cfg.clip_eps,
    #     learning_rate=cfg.learning_rate,
    #     output_dir=str(cfg.output_dir),
    # )
    #
    # trainer.train()
    #
    # What to log (minimum):
    # - reward_mean, success_rate, kl_mean, entropy/diversity, clipfrac
    #
    raise SystemExit("Template only. Fill in the TODOs and align to your TRL version.")


if __name__ == "__main__":
    main()

