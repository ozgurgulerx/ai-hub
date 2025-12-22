from __future__ import annotations

import itertools
import json
from pathlib import Path

from grpo_toy import Config, train


def main() -> None:
    out_path = Path(__file__).resolve().parent / "eval" / "sweep_results.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    group_sizes = [4, 8, 16]
    kl_betas = [0.0, 0.05, 0.2]

    results = []
    for group_size, kl_beta in itertools.product(group_sizes, kl_betas):
        cfg = Config(
            seed=11,
            reward="sparse",
            steps=60,
            group_size=group_size,
            kl_beta=kl_beta,
            lr=0.35,
            ppo_epochs=4,
            clip_eps=0.2,
            temperature=1.0,
            log_every=9999,  # keep sweep quiet
        )
        run = train(cfg)
        results.append(
            {
                "group_size": group_size,
                "kl_beta": kl_beta,
                "baseline_success": run["baseline"]["success_rate"],
                "final_success": run["final"]["success_rate"],
                "baseline_entropy": run["baseline"]["entropy_mean"],
                "final_entropy": run["final"]["entropy_mean"],
                "baseline_diversity": run["baseline"]["diversity"],
                "final_diversity": run["final"]["diversity"],
            }
        )

    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Wrote:", out_path)
    print("Top runs (by final_success):")
    for row in sorted(results, key=lambda r: r["final_success"], reverse=True)[:5]:
        print(
            json.dumps(
                {
                    "group_size": row["group_size"],
                    "kl_beta": row["kl_beta"],
                    "final_success": row["final_success"],
                    "final_entropy": row["final_entropy"],
                    "final_diversity": row["final_diversity"],
                }
            )
        )


if __name__ == "__main__":
    main()

