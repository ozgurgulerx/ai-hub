import json
import sys
from pathlib import Path


def main() -> None:
    day_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(day_dir))

    from graders.python_grader import grade  # noqa: WPS433 (runtime import for portability)

    payload = json.loads(
        (Path(__file__).resolve().parent / "smoke_test_payload.json").read_text(encoding="utf-8")
    )
    item = payload["item"]
    samples = payload["samples"]

    for i, sample in enumerate(samples):
        score = grade(sample=sample, item=item)
        print(f"sample[{i}] score={score}")


if __name__ == "__main__":
    main()
