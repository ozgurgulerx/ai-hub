# Day 01 — Theory (RLFT/RFT on Azure AI Foundry)

This is the **minimum operational + mechanistic** mental model you should be able to explain while looking at Foundry RLFT curves.

Companion: deeper concepts and use-case map in `../../../../docs/ai-systems-advanced/reinforcement-learning/planning/rlft_concepts.md`.

---

## TL;DR (one sentence)

RLFT/RFT optimizes a **policy** to increase probability of outputs that score higher under **grader-defined reward**, by sampling **groups of candidates**, scoring them, computing **relative advantage**, and updating the policy with **conservative (PPO-like) steps + KL-to-reference control**.  
(Microsoft Learn RLFT guide: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reinforcement-fine-tuning?view=foundry-classic)

---

## The 10 nouns you must be fluent in (or you can’t debug)

- **Policy** πθ: the model you are updating.
- **Reference** πref: a frozen copy (often starting checkpoint). Used for **KL control**.
- **Prompt / episode** x: one training item (messages array).
- **Completion / trajectory** y: one sampled output sequence from πθ for prompt x.
- **Group size (G)**: number of sampled completions per prompt in a step.
- **Reward** r = R(x, y): scalar from graders.
- **Baseline** b(x): per-prompt baseline (often group mean reward).
- **Advantage** a = r - b: “better than siblings?” signal.
- **Clip**: prevents giant policy jumps (PPO-style ratio clipping).
- **KL penalty**: keeps πθ near πref (stability + anti-drift).

If you can’t say what each is *and what it does*, you’re not operational.

---

## Why verifiable tasks are the sweet spot (RLVR)

RLFT is easiest to debug when reward is:

- **deterministic** (Python grader / rule checks)
- **hard to game** (anti-cheat checks, strict schemas)
- **aligned** with real success metric (pass/fail, constraint satisfaction)

If reward is vague, RL will Goodhart it. Your job: design reward so **“high score” == “actually correct.”**

---

## What actually happens (the RLFT/GRPO-ish loop)

### One training step, mechanistically

For each prompt x in a batch:

1) **Sample a group** of completions  
   y₁…y_G ~ πθ(.|x)  (controlled sampling)

2) **Grade each completion**  
   rᵢ = R(x, yᵢ) using grader(s)

3) **Compute group-relative advantage**  
   b(x) = mean(r₁…r_G)  
   aᵢ = rᵢ - b(x)  
   (optional) normalize: aᵢ ← aᵢ / (std(r)+ε)

4) **Policy update with conservative objective**  
   - PPO-like clipped ratio objective (stability)  
   - + KL(πθ || πref) regularization (drift control)

5) **Log** metrics + examples (debugging is 80% logging)

### Why “group-relative” helps

- avoids training a **critic/value model** (huge memory/complexity reduction vs PPO)
- fits LLM reality: reward is usually **end-of-sequence**
- turns “absolute correctness is sparse” into “which attempt was best among siblings?”

---

## The three contracts (operational RLFT)

### 1) Data contract (validator-enforced)

(Microsoft Learn: RLFT data format in the same RLFT guide)

Must-haves:

- JSONL with `messages[]`; **last message must be user**
- `train` + `validation` required
- extra fields become `item.*` (store metadata here)

**Minimal item**

```json
{
  "messages": [
    {"role": "system", "content": "You output strict JSON only."},
    {"role": "user", "content": "Return {\"answer\":56} for 7*8."}
  ],
  "id": "m1",
  "difficulty": "easy"
}
```

### 2) Output contract (`response_format`)

Strict output makes grading cheap + reliable.

- strict JSON schema
- `additionalProperties: false`
- tight `required`
- enums whenever possible

Example schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {"answer": {"type": "integer"}},
  "required": ["answer"]
}
```

### 3) Reward contract (graders)

Graders are software. Treat them like prod code.

- deterministic, idempotent, fast
- explicit failure reasons
- anti-cheat checks
- gate soft preferences behind correctness

Canonical pattern:

- if correctness fails → reward = 0 immediately
- else apply small shaped bonuses/penalties (brevity, format cleanliness, etc.)

---

## The knobs (what you tune first)

### Group size (G)

- higher G → better baseline + more exploration, but token cost explodes
- start: G=4–8, raise only if signal is too noisy

### Sampling (temperature/top_p/max_tokens)

- too cold → no exploration → RL can’t discover better trajectories
- too hot → noisy rewards + KL blowups
- rule: keep diversity without destroying coherence

### KL beta (reference control)

- too low → drift + reward hacking
- too high → flat learning (reward doesn’t move)
- treat KL like a safety rail

### Clip range

- too tight → slow learning
- too loose → oscillation / collapse

### Reward shaping (for sparse reward)

Binary pass/fail is brutal if pass rate is near zero. Add intermediate shaping that is:

- hard to game
- aligned with progress
- doesn’t dominate final correctness

---

## The curves you read first (Foundry)

From Foundry metrics:

- `train_reward_mean` vs `valid_reward_mean`
- `train_reasoning_tokens_mean` vs `valid_reasoning_tokens_mean`

Add these mentally (even if UI doesn’t show all):

- `KL_to_ref_mean` (critical)
- pass rate (if reward is binary)
- output length stats (verbosity hacks)
- advantage stats (collapse vs healthy variance)

---

## Fast triage (debug in 60 seconds)

- train↑, valid↓/flat  
  → reward hacking OR valid OOD  
  Fix: tighten grader + align valid distribution + add anti-cheat + reduce hack surface

- reasoning tokens↑, reward flat (“thinking tax”)  
  → you’re paying for thoughts without signal  
  Fix: reward shaping, better grader coverage, cap max_tokens, penalize verbosity

- reward oscillation  
  → unstable updates or inconsistent grading  
  Fix: simplify reward, increase eval samples, reduce LR/clip looseness, stabilize sampling

- KL steadily rising  
  → drifting off reference  
  Fix: increase KL beta, reduce sampling temperature, reduce update aggressiveness

- reward collapses to near-constant  
  → advantage collapsed (no contrast) OR grader degenerate  
  Fix: inspect per-sample reward histogram; add informative shaping; validate grader

---

## Grader engineering cookbook (the part most people skip)

### Deterministic correctness

- exact match / numeric tolerance
- schema validity
- unit tests pass (code)
- SQL result matches reference

### Anti-cheat checklist

- strict schema validation first
- length limits
- disallow extra keys (`additionalProperties:false`)
- parse > regex
- randomized tests / adversarial cases for code graders
- punish “format tricks” (e.g., hiding answer in extra fields)

### Multi-grader composition (recommended)

- Correctness grader (hard gate)
- then Preference graders (style, brevity, safety policy, etc.) as small deltas

---

## When RLFT/GRPO is a good idea (and when it isn’t)

Best fit:

- unambiguous tasks where experts agree on “correct”
- verifiable outcomes (tests, parsers, calculators, schema, reference answers)
- base model already has non-zero success probability

Bad fit:

- subjective preferences without a reliable grader
- tasks where “good” is inherently fuzzy (you’ll Goodhart)

---

## Mental mapping: Foundry RLFT ↔ OpenAI RFT ↔ GRPO conceptually

Regardless of platform:

- group sampling per prompt
- reward → group-relative advantage
- conservative update (clip) + KL-to-reference
- monitoring reward + tokens + drift signals

If you understand that loop, you can use any implementation.

---

## Day01 “I actually get it” checklist

You can:

- explain the loop in 5 steps
- define the 3 contracts and why each reduces failure modes
- predict how curves move when you change: G, sampling temp, KL beta
- design a grader that is deterministic + hard to game
- diagnose: hacking vs OOD vs thinking tax vs drift in < 2 minutes
