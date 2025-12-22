# Day 01 — Lab (RLFT field drill)

Goal: do one end-to-end RLFT run you can **reproduce**, and learn to read curves by intentionally breaking things.

---

## Lab 0 — Choose a verifiable task (pick ONE)

### Option A (fastest): Arithmetic → strict JSON

- Prompt: “Return JSON {answer:int} for X op Y”
- Reward: 1 if correct & schema-valid else 0

### Option B (best learning): Code → unit tests

- Prompt: “Write function f() …”
- Reward: fraction of tests passed (0..1)

### Option C (businessy): SQL → result match

- Prompt: “Write SQL for …”
- Reward: compare query result to reference

Recommended: **Option B** if you can run tests safely; otherwise Option A.

---

## Lab 1 — Build the dataset (train/valid)

- Train: 100–300 items
- Valid: 50 items
- Keep valid distribution aligned with train (same difficulty mix)

Store metadata in `item.*`:

- difficulty bucket
- expected answer hash
- family/category (so you can detect overfit)

---

## Lab 2 — Define the output contract (`response_format`)

Use strict JSON schema:

- `additionalProperties:false`
- tight `required`
- narrow types

This is your **hack-surface reducer**.

---

## Lab 3 — Implement the grader (deterministic + anti-cheat)

### Minimal arithmetic grader (illustrative)

```python
import json

def grade(example, model_output_json: str) -> float:
    # 1) Parse output
    try:
        obj = json.loads(model_output_json)
    except Exception:
        return 0.0

    # 2) Enforce schema-like constraints (do real schema validation in prod)
    if set(obj.keys()) != {"answer"}:
        return 0.0
    if not isinstance(obj["answer"], int):
        return 0.0

    # 3) Compute expected
    expected = example["item"]["expected_answer"]
    if obj["answer"] == expected:
        return 1.0

    return 0.0
```

Anti-cheat upgrades to add:

- cap output length (e.g., max chars)
- reject NaN / weird ints
- ensure no extra keys
- log failure reasons for debugging

---

## Lab 4 — Run RLFT with conservative defaults

Start conservative; your aim is to observe clean learning:

- group size G: 4–8
- sampling: mild diversity (avoid extreme temperature)
- KL beta: moderate (avoid drift)
- max tokens: capped (prevent verbosity hacks)

Run a short job first (cheap sanity check), then scale.

---

## Lab 5 — Build the diagnostic dashboard (must-log)

Track per step:

- `train_reward_mean`, `valid_reward_mean`
- pass rate (binary reward tasks)
- `reasoning_tokens_mean` (train/valid)
- `KL_to_ref_mean` (if available)
- output length stats
- reward histogram per batch (debugging gold)

---

## Lab 6 — Deliberately break it (learn faster)

Do these 3 ablations and predict curves before you run them:

1) Weaken schema / allow extra keys  
   Expect: reward hacking, strange outputs, train↑ valid↓.

2) Set KL beta too low  
   Expect: KL drift, brittle behavior, possible reward spikes then collapse.

3) Increase max_tokens a lot  
   Expect: reasoning tokens↑, reward flat (“thinking tax”), verbosity hacks.

Write down:

- predicted symptom
- observed symptom
- fix

---

## Deliverables (commit to repo)

Create:

- `days/Day01/artifacts/`:
  - `schema.json`
  - `grader.py`
  - `dataset_train.jsonl`, `dataset_valid.jsonl` (or generation script)
  - `eval.py` (baseline eval that prints pass_rate + tokens stats)
  - `notes.md` (what broke, what fixed)

Minimum proof:

- baseline metrics
- RLFT metrics curves snapshot (or logged numbers)
- 10 failure cases before + after

---

If you want, I can also generate a `days/Day01/NOTES.md` with a one-page debugging matrix (symptom → root cause → knob to turn → what should happen to curves).
