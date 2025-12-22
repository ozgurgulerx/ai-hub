"""
Template: GRPO fine-tuning with Unsloth.

Unsloth provides fast training recipes (often LoRA/QLoRA + efficient generation),
which makes GRPO/RLVR loops feasible on smaller hardware.

This file is a wiring template:
dataset -> generate K completions -> deterministic reward -> GRPO update -> log curves.

Pass/fail (for you):
1) You can find and set K (group size), temperature, and sequence length limits.
2) You can wire a deterministic grader and show anti-cheat checks.
3) You can export curves (reward/KL/entropy/length/diversity) for debugging.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunConfig:
    model_name_or_path: str
    train_jsonl: Path
    valid_jsonl: Path
    output_dir: Path
    group_size: int = 8
    kl_beta: float = 0.05
    clip_eps: float = 0.2
    temperature: float = 1.0


def main() -> None:
    cfg = RunConfig(
        model_name_or_path="Qwen/Qwen2.5-0.5B-Instruct",
        train_jsonl=Path("data/train.jsonl"),
        valid_jsonl=Path("data/valid.jsonl"),
        output_dir=Path("runs/unsloth-grpo"),
    )

    try:
        import torch  # noqa: F401
        import unsloth  # noqa: F401
    except Exception as e:  # pragma: no cover
        raise SystemExit(
            "Missing deps. Install in your own env per Unsloth docs (torch + unsloth)."
        ) from e

    # PSEUDOCODE (align to your Unsloth version / recipe):
    #
    # 1) Load model/tokenizer with Unsloth helpers.
    # 2) Define a reward function (deterministic grader; fail closed; anti-cheat).
    # 3) Configure GRPO knobs:
    #    - group_size (K)
    #    - kl_beta / target_kl
    #    - clip_eps
    #    - temperature (exploration)
    # 4) Train and log:
    #    - reward_mean, success_rate, kl_mean, entropy/diversity, clipfrac, length
    #
    raise SystemExit("Template only. Fill in the TODOs and align to your Unsloth recipe.")


if __name__ == "__main__":
    main()

