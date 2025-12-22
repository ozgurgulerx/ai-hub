# Day 02 — Theory (DPO + PPO)

This day is a **field manual** for preference optimization:

- **DPO** (first-class in Azure AI Foundry)
- **PPO** (classic RLHF algorithm, typically self-hosted / open-source)

…and a precise mental map between them.

---

## 0) One-sentence definitions (if you can’t say this, you can’t debug)

- **DPO**: directly trains the policy to prefer a “winner” completion over a “loser” completion for the same input, using a KL-regularized objective that avoids training a reward model.
- **PPO (RLHF)**: trains a reward model (or uses a reward function), then updates the policy with a clipped policy-gradient objective using advantages, usually with KL-to-reference control for stability.

---

## 1) The preference-learning triad (the 3 moving parts)

Every preference method is defined by:

1) **Data**: how you represent “what I prefer”
2) **Objective**: what loss you optimize
3) **Regularization**: how you stop the policy from drifting / collapsing

DPO and PPO differ mostly in (2): DPO bakes the preference comparison into the loss; PPO routes it through rewards + advantages.

---

## 2) DPO — what it optimizes (minimal math, maximum insight)

Given:

- input x
- preferred completion y⁺ and non-preferred y⁻
- reference policy π_ref (frozen baseline model)
- trainable policy π_θ
- beta β controls “how hard we push preferences”

Core idea: increase the **relative log-prob gap** between preferred and non-preferred, while staying near π_ref.

A canonical DPO objective (conceptually):

- maximize log σ( β * [ (log π_θ(y⁺|x) - log π_θ(y⁻|x)) - (log π_ref(y⁺|x) - log π_ref(y⁻|x)) ] )

Interpretation:

- if π_θ already prefers y⁺ over y⁻, reinforce.
- if not, push probability mass from y⁻ → y⁺.
- subtracting the reference-gap acts like KL-style anchoring.

**Operational takeaway**

- DPO is “pairwise ranking as training signal.”
- Your dataset quality dominates your results.

---

## 3) Azure DPO — the data contract (this is everything)

Azure DPO JSONL requires **exactly two completions** per input:

- `input`
- `preferred_output`
- `non_preferred_output`

Each JSONL line looks like:

```json
{
  "input": {
    "messages": [...],
    "tools": [...],
    "parallel_tool_calls": true
  },
  "preferred_output": [{"role":"assistant","content": "..."}],
  "non_preferred_output": [{"role":"assistant","content": "..."}]
}
```

Rules:

- input is the conversation context (system + initial user, optionally tools metadata)
- preferred/non_preferred must contain at least one assistant message
- roles allowed in preferred/non_preferred are (assistant, tool)

This is not negotiable; validation will fail otherwise.

---

## 4) DPO dataset design: the 6 rules that matter

### Rule A — “Same prompt, same constraints”

The pair must be identical in:

- user intent
- system policy
- allowed tools

Only the *assistant choice* differs.

### Rule B — Prefer “near-miss” negatives, not garbage

Bad: y⁻ is obviously wrong/toxic nonsense → the model learns nothing subtle.  
Good: y⁻ is plausible but violates one key preference (tone, verbosity, policy, format).

### Rule C — One reason to win (per pair)

Make the preference label explainable:

- “winner follows JSON schema”
- “winner cites policy”
- “winner is concise”

Not 5 reasons at once, or you can’t debug.

### Rule D — Cover the boundary conditions

For each preference dimension, include:

- easy wins
- borderline wins
- tricky edge cases (tempt the model)

### Rule E — Counterfactual symmetry

If you only ever punish “too verbose”, model might under-explain.  
Include pairs where “too short” loses.

### Rule F — Build a *static* regression set

A small set (~50) of preference pairs you never train on.  
This is your “unit test suite” for alignment.

---

## 5) Azure DPO — invoking the job (REST mental model)

Azure OpenAI DPO job creation uses the fine-tuning jobs endpoint with:

- method.type = "dpo"
- beta and l2_multiplier hyperparameters

(Keep the platform defaults first; tune later.)

You should think about these knobs:

- **beta**: preference strength (higher = more aggressive)
- **l2_multiplier**: stabilizer (reduces overfitting / oversteer)
- prompt_loss_weight may exist depending on API surface; treat it as “keep prompting behavior stable”

---

## 6) DPO metrics & debugging (what to look at)

### Offline metrics (you own these)

1) **Pairwise win-rate** on heldout preference pairs:
   - Evaluate: does the tuned model assign higher logprob to y⁺ than y⁻?
2) **Style regressions**
   - Use a deterministic checker (JSON schema, max length, banned phrases)
3) **Task outcome metrics**
   - If preference is “helpfulness”, measure downstream CSAT proxy (even if crude)

### Online metrics (platform + product)

- A/B test: tuned vs base on real traffic
- “Escalation rate”, “deflection rate”, “policy violation rate”

### Failure modes (DPO-specific)

- **Oversteer**: model becomes “too” aligned (e.g., refuses too much, too terse)
- **Mode collapse**: always uses one template response
- **Reward-by-proxy**: learns superficial cues (keywords) instead of intent

Countermeasures:

- add counterexamples (template loses)
- add symmetry pairs (too terse loses sometimes)
- add hard constraints in system prompt + output schema for format

---

## 7) PPO (RLHF) — why it exists, and when it beats DPO

PPO matters when:

- you have **scalar reward** (not only pairwise)
- you want **multi-objective optimization** with explicit tradeoffs (helpfulness vs safety vs latency)
- you can afford / build a **reward model** or reliable reward function

PPO is heavier but can be more controllable when reward is well-shaped.

---

## 8) PPO mechanics (what actually happens)

Key objects:

- policy π_θ (trainable)
- reference π_ref (anchor)
- reward model R_φ(x, y) or reward function R(x,y)
- value function V_ψ(x, y_t) (critic)
- advantage Â (reward-to-go minus baseline)

Loop:

1) sample rollouts (prompt → completion)
2) compute reward for each completion
3) compute advantages (GAE or simpler)
4) update policy using PPO clipped surrogate:
   - ratio r_t = π_θ(a_t|s_t) / π_old(a_t|s_t)
   - maximize E[ min(r_t Â_t, clip(r_t,1-ε,1+ε) Â_t ) ]
5) apply KL penalty to π_ref to prevent drift

The critic is expensive (memory + instability), but it enables smoother credit assignment than pure sequence-level reward.

---

## 9) PPO vs DPO vs RFT (GRPO) — the decision table

Use this, not vibes:

### Use DPO when:

- preference is subjective (tone, style, “better answer”)
- you can create many reliable y⁺/y⁻ pairs from logs / A/B tests
- you want cheaper training than PPO
- you want predictable, inspectable training signal

### Use PPO (RLHF) when:

- you need scalar reward shaping (partial credit, multi-objective)
- you can build/validate a reward model or reward function
- you need fine-grained steering and can afford complexity

### Use RFT/GRPO when:

- reward is verifiable / programmatic (tests, checkers)
- you want RL without training a reward model or critic
- the task is “objective correctness”, not preference

---

## 10) Day02 “I get it” checklist

You can:

- design a preference rubric and produce 200+ high-signal DPO pairs
- run a DPO job in Foundry and evaluate with a heldout preference suite
- explain DPO objective and what beta does
- explain PPO clipped objective and why critics exist
- choose between DPO/PPO/RFT for a product task and defend it

---

## Sources (align to what Azure actually supports)

- Azure AI Foundry DPO how-to (dataset format + job creation): https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning-direct-preference-optimization?view=foundry-classic
- Foundry fine-tuning workflow (methods list, artifacts, checkpoints): https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning?view=foundry-classic
- Foundry RLFT/RFT how-to (for mapping PPO mental model to RFT/GRPO): https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/reinforcement-fine-tuning?view=foundry-classic
- InstructGPT / PPO mental model (RLHF framing): https://arxiv.org/abs/2203.02155
- DPO paper (canonical reference): https://arxiv.org/abs/2305.18290
