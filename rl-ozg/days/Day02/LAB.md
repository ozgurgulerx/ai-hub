# Day 02 — Lab (Azure DPO + PPO baseline)

You will ship:

- a preference dataset generator
- an evaluation harness (pairwise win-rate + regression suite)
- an Azure DPO job run (or at least a fully validated dataset + job spec)
- a local PPO baseline run (TRL) to solidify the mental model

---

## Part A — DPO in Azure (do this first)

### Lab A1 — Pick a preference axis (choose ONE)

Examples:

- “concise but complete support replies”
- “strict JSON outputs”
- “policy-compliant refusal style”
- “tone: calm, non-snarky, no emojis”

Write a 5-line rubric:

- 3 must-haves
- 2 must-not-haves

### Lab A2 — Generate 200 preference pairs (high-signal)

Source options:

1) Real logs + human labeling
2) Synthetic: base model generates 2 candidates; you label winner using rules + minimal human pass
3) A/B results: winner = variant with higher downstream metric

Rules:

- near-miss negatives
- one reason to win per pair
- add symmetry pairs

### Lab A3 — Validate JSONL against the DPO schema

Hard checks:

- top-level keys exist: input / preferred_output / non_preferred_output
- preferred/nonpreferred each contain ≥1 assistant message
- no illegal roles in outputs

### Lab A4 — Create an “alignment unit test suite”

Make `data/dpo_regression.jsonl` with ~50 pairs you never train on.

### Lab A5 — Run DPO in Foundry (portal or REST)

- start with defaults (don’t “tune” before you measure)
- keep a strict suffix naming pattern (e.g., `dpo_tone_v1`)

### Lab A6 — Evaluate (offline + qualitative)

Offline:

- pairwise win-rate on regression suite
- format regressions (schema, length, forbidden tokens)

Qualitative:

- 30 random prompts; compare base vs tuned; label failure reasons

Deliverables:

- `eval/pairwise_winrate.py`
- `eval/format_checks.py`
- `notes.md` with 10 before/after examples

---

## Part B — PPO baseline (local, TRL)

Goal: internalize PPO mechanics. This is not Azure-hosted; it’s your ground-truth lab.

### Lab B1 — Choose a reward function you trust

Pick one:

- code passes unit tests (scalar = % tests passed)
- JSON schema validity + correctness (scalar)
- string match / numeric tolerance (scalar)

### Lab B2 — Run PPOTrainer on a small open model

- small model first (so you can iterate)
- log: reward mean, KL to ref, output length, success rate

### Lab B3 — Ablate 3 knobs and predict curves

- KL coef too low (expect drift)
- reward too sparse (expect no learning)
- max_new_tokens too high (expect verbosity hacks)

Deliverables:

- `scripts/run_ppo_trl.py`
- `notes_ppo.md` with predicted vs observed

---

## Capstone for Day02 (minimum acceptable)

- DPO: +10–20% pairwise win-rate on heldout suite, with no format regressions
- PPO: a clean run where reward increases without KL exploding, and you can explain why

