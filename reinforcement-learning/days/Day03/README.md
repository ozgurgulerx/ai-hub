# Day 03 — GRPO for LLM Post-Training (RLVR / RFT)

You’re building **top-1% practical + theoretical** competence in **Group Relative Policy Optimization (GRPO)** for LLM post-training, with an operator mindset: *define reward → sample groups → update conservatively → debug from metrics*.

This is framework-agnostic first, then mapped to:

- (A) **OpenAI RFT-style** mental model (graders + sampling + updates)
- (B) **Hugging Face TRL** `GRPOTrainer`
- (C) **Unsloth** GRPO recipes
- (D) **VLM GRPO (multimodal) with TRL**: `days/Day03/vlm_grpo_with_trl.md`

<details>
<summary><strong>Quick navigation</strong></summary>

- [A) Level map (L0–L6)](#a-level-map-l0l6)
- [B) First 12 microtasks](#b-first-12-microtasks-in-order)
- [C) Diagnostic dashboard spec](#c-diagnostic-dashboard-spec-grpo-specific)
- [D) 1% competency rubric](#d-final-1-competency-rubric)
</details>

---

## Canonical baseline (what this Day 03 fully covers)

From the notes you provided, this curriculum explicitly covers:

- **What GRPO is and why it matters**: RL optimizer for LLM post-training; emerged as the “default” optimizer for **RL with verifiable rewards (RLVR)**; used in “reasoning model” training narratives.
- **PPO vs GRPO**: group sampling per prompt; **group-relative advantage baseline**; **no critic/value model**; sequence-level (constant) advantage; PPO-style clipping remains.
- **KL control**: keep policy near a reference; treat KL either as reward shaping or explicit penalty; debug with KL/entropy/drift signals.
- **RLVR use cases**: math answer checking, code+tests, tool-use correctness, planning games; and **when not to use** (ambiguous preferences).
- **Tooling**: OpenAI RFT mental model; 🤗 TRL `GRPOTrainer`; Unsloth recipes and practical tips.
- **Failure modes**: reward hacking, KL blow-up/mode collapse, “thinking tax”, overfit/OOD collapse, oscillations from inconsistent grading.
- **Variants + research directions**: GSPO-style ideas, GRPO tweaks for sparse rewards / verbosity, hybrid (human + verifiable) setups.

---

## A) Level map (L0–L6)

> Each level includes: concepts, microtasks, lab, rubric, failure drills, artifact.

### L0 — Frame LLM generation as RL (objective is computable)

**Objective (1 sentence):** model “generation” as a stochastic policy over token sequences and reason about **sequence-level rewards** (sparse, end-of-sequence).

- Concepts: trajectories = tokens; `πθ(y|x)`; sequence reward; credit assignment reality; why “non-zero baseline skill” matters.
- Lab: implement a tiny policy that samples sequences and receives a verifiable reward.
- Rubric: you can write the objective and explain why sparse rewards are hard.
- Failure drills: show why 0% base success → no learning.
- Artifact: `days/Day03/grpo_toy.py` (sampling + reward + eval).

### L1 — PPO essentials (what GRPO keeps)

**Objective:** derive PPO’s clipped surrogate and explain what clipping buys you (stability, bounded updates).

- Concepts: `ratio = πθ/πθ_old`, clipping, advantages, (critic role), KL as constraint/penalty.
- Lab: implement PPO clip selection logic and verify edge cases.
- Rubric: given A and ratio, you predict gradient direction and clipping regime.
- Failure drills: too-large LR / no clip → collapse.
- Artifact: `days/Day03/grpo_toy.py` (PPO-style clipped update core).

### L2 — GRPO core (what GRPO changes)

**Objective:** implement GRPO’s **group-relative advantage** and train without a value network.

- Concepts: sample **K outputs per prompt**; baseline = group mean reward; normalize; constant advantage across tokens; no critic.
- Lab: implement GRPO update end-to-end on a toy conditional “LM”.
- Rubric: you can explain why the baseline reduces variance and what compute is saved by dropping the critic.
- Failure drills: group size too small → noisy advantage; reward sparsity; KL drift.
- Artifact: `days/Day03/grpo_toy.py` (GRPO training loop + logs).

### L3 — Reward/Grader engineering (the moat)

**Objective:** design graders that are deterministic, anti-cheat, and shape sparse rewards without ruining the objective.

- Concepts: RLVR graders; anti-cheat; reward shaping; gating; verbosity/length penalties; multi-objective reward.
- Lab: implement a “hackable” reward, demonstrate exploitation, then harden it.
- Rubric: you can predict how a weak grader will be gamed and fix it with one targeted ablation.
- Failure drills: reward hacking; “thinking tax”; inconsistent grading oscillations.
- Artifact: `days/Day03/CAPSTONE.md` (grader + eval spec template).

### L4 — Real GRPO on open models (TRL + Unsloth)

**Objective:** run GRPO on an open model with a verifiable reward and a reproducible eval.

- Concepts: generation groups, batching, memory; LoRA/QLoRA; dataset format; reward function wiring; logging.
- Lab: TRL `GRPOTrainer` run + Unsloth run on same RLVR task; compare curves + eval.
- Rubric: you can reproduce a run, rerun with a knob change, and interpret curves.
- Failure drills: OOM, low diversity, KL spikes, reward flat.
- Artifact: training config + run log + eval report (paths under `days/Day03/`).

### L5 — Variants and ablations (GSPO / sparse reward fixes)

**Objective:** replicate one GRPO variant idea and show the trade-off with an ablation table.

- Concepts: GSPO-style sequence tweaks, alternative normalization, exploration controls, verbosity control.
- Lab: implement one tweak on the toy setup + (optionally) one open-model run.
- Rubric: you can explain why the tweak helps and where it breaks.
- Failure drills: “wins on train, loses on OOD”.
- Artifact: ablation table + curves + interpretation.

### L6 — Capstone (production-grade RLVR story)

**Objective:** ship a reproducible “reasoning/coding correctness” improvement with evals and a debugging narrative.

- Concepts: task selection, dataset, grader, baseline, GRPO run, eval harness, cost/compute accounting.
- Lab: end-to-end case study (baseline vs GRPO) with failure drill + fix.
- Rubric: another engineer can reproduce results; your eval catches regressions.
- Failure drills: deploy wrong checkpoint; KL drift; reward hacking.
- Artifact: case study report + scripts + talk outline.

---

## B) First 12 microtasks (in order)

Rules:

- 5–20 minutes each. Ship tiny artifacts. Pass/fail is explicit.
- “Session” = 4 microtasks. **Every 3rd session is spaced repetition** via a harder drill.

### Session 1 (Microtasks 01–04): RL framing + PPO core

#### Microtask 01 — RL framing for LLM generation (sequence reward reality)

- Timebox: 15 minutes
- Inputs: this `days/Day03/README.md`; your own baseline GRPO notes
- Steps:
  1. Write the RL framing in 12–20 lines: define `x` (prompt), `y` (completion tokens), `πθ(y|x)`, and sequence reward `R(x,y)`.
  2. Add the one engineering constraint that matters: *end-of-sequence rewards are sparse*.
  3. Add one “operator rule”: *if base success ≈ 0%, fix the task/reward before RL*.
- Pass/fail:
  - PASS if you can explain (from memory) why sparse rewards + long sequences → weak gradients.
  - FAIL if you can’t state the objective in one line.
- Expected artifact snippet (commit as `days/Day03/notes/rl_framing.md`):

  ```text
  Objective: maximize E_{y ~ πθ(·|x)}[R(x,y)] with conservative updates (KL/clipping).
  Reality: reward is often terminal and sparse → you need a foothold or shaping.
  ```

#### Microtask 02 — PPO clipped surrogate (minimal derivation + edge cases)

- Timebox: 20 minutes
- Inputs: PPO objective; your baseline notes; the toy code you’ll run later
- Steps:
  1. Derive (or restate) the PPO surrogate: `L = E[min(r*A, clip(r)*A)]` where `r = exp(logπθ − logπold)`.
  2. Write down the two clipping regimes:
     - A>0 and r>1+ε → clipped (no gradient)
     - A<0 and r<1−ε → clipped (no gradient)
  3. Implement a 10-line “clip selector” function (pure Python).
- Pass/fail:
  - PASS if your selector matches the regimes above on a 6-case table (you test it).
  - FAIL if you can’t predict which branch is active for a given (A,r).
- Expected artifact snippet (commit as `days/Day03/notes/ppo_clip_table.md`):

  ```text
  A>0: min(rA, clip(r)A) clips upper side.
  A<0: min(rA, clip(r)A) clips lower side.
  ```

#### Microtask 03 — Group-relative baseline (GRPO advantage)

- Timebox: 15 minutes
- Inputs: GRPO definition; “group mean baseline”
- Steps:
  1. Define group rewards `{r_i}` for K samples for the same prompt.
  2. Compute baseline `b = mean(r_i)` and advantage `A_i = r_i − b`.
  3. Add optional normalization: `A_i ← (A_i − mean)/ (std + ε)` (state when you’d use it).
- Pass/fail:
  - PASS if `sum_i A_i ≈ 0` per group (you verify numerically on a random example).
  - FAIL if you can’t explain why subtracting a baseline reduces variance without changing the expectation.
- Expected artifact snippet (commit as `days/Day03/notes/grpo_advantage.md`):

  ```text
  For prompt x: sample y1..yK, rewards r1..rK.
  Baseline b = mean(r); advantage Ai = ri - b (optionally normalize).
  ```

#### Microtask 04 — Session 1 checkpoint (spaced repetition seed)

- Timebox: 10 minutes
- Inputs: your artifacts from 01–03
- Steps:
  1. Write a 6-bullet “PPO vs GRPO: what stays / what changes”.
  2. Add 2 “if X do Y” operator rules (clipping/KL/reward sparsity).
- Pass/fail:
  - PASS if you can explain GRPO in 30 seconds without saying “it’s like PPO but…”.
  - FAIL if you can’t state where the value network went.
- Expected artifact snippet (append to `days/Day03/notes/ppo_vs_grpo.md`):

  ```text
  Keeps: ratio + clipping + KL control.
  Changes: advantage baseline from group mean; no critic; group sampling per prompt.
  ```

**Session 1 ends — checklist, oral exam, artifact**

- Checklist (you can now do):
  - write the RL objective for LLM generation
  - explain PPO clipping regimes from memory
  - compute group-relative advantages and explain why the baseline helps
- 5-question oral exam:
  1. What is the “trajectory” in an LLM RL setup?
  2. Why does terminal reward create credit assignment pain?
  3. For A<0 and r<1−ε, why does PPO clip?
  4. Why does subtracting a baseline not change the expected gradient?
  5. What is the *one* reason you keep KL control in post-training?
- Artifact to commit: `days/Day03/notes/` (the four notes above).

---

### Session 2 (Microtasks 05–08): Implement GRPO from scratch (toy)

#### Microtask 05 — Read the toy GRPO code path (instrument-first)

- Timebox: 10 minutes
- Inputs: `days/Day03/grpo_toy.py`
- Steps:
  1. Identify where: group sampling happens, reward is computed, advantages are formed, PPO update runs, KL is computed.
  2. Add one print/log line that surfaces a hidden variable (clipfrac or advantage std).
- Pass/fail:
  - PASS if you can point to the exact function that implements “no critic”.
  - FAIL if you can’t map code sections to the conceptual loop.
- Expected artifact snippet (commit in `days/Day03/grpo_toy.py`):

  ```python
  # print(f"clipfrac={clipfrac:.3f} adv_std={adv_std:.3f}")
  ```

#### Microtask 06 — Run baseline + prove “non-zero skill” (or fix it)

- Timebox: 15 minutes
- Inputs: `python3 days/Day03/grpo_toy.py --mode eval`
- Steps:
  1. Run evaluation on the initial policy.
  2. Record success rate and entropy.
  3. If success is ~0, shorten sequence length or use dense reward mode and rerun.
- Pass/fail:
  - PASS if baseline success is measurably non-zero *or* you fix the setup so it becomes non-zero.
  - FAIL if you proceed to training with a dead signal.
- Expected artifact snippet (append to `days/Day03/TIER01.log`):

  ```text
  Baseline: success=0.08 entropy=1.38 (non-zero foothold ✓)
  ```

#### Microtask 07 — Train with GRPO and hit a quantitative improvement

- Timebox: 20 minutes
- Inputs: `python3 days/Day03/grpo_toy.py --mode train`
- Steps:
  1. Train for N steps with defaults (group size, clip ε, KL β).
  2. Confirm reward mean rises and KL stays bounded.
  3. Run eval after training; compare success to baseline.
- Pass/fail:
  - PASS if eval success increases by a nontrivial margin (define it: e.g., +0.20 absolute).
  - FAIL if reward rises but success doesn’t (you’re optimizing the wrong signal).
- Expected artifact snippet (append to `days/Day03/TIER01.log`):

  ```text
  After GRPO: success=0.55 (Δ +0.47), KL=0.08, clipfrac=0.12
  ```

#### Microtask 08 — Debugging playbook (GRPO-specific)

- Timebox: 20 minutes
- Inputs: your own curves from toy run; the dashboard spec below
- Steps:
  1. Write 10 “if/then” rules mapping signals → actions (reward/KL/entropy/diversity).
  2. Include at least one rule for each failure mode: reward hacking, KL blow-up, thinking tax, overfit/OOD.
- Pass/fail:
  - PASS if each rule specifies what to change *and* what metric should respond.
  - FAIL if rules are untestable (“try tuning stuff”).
- Expected artifact snippet (commit as `days/Day03/notes/debug_playbook.md`):

  ```text
  If reward↑ and KL↑ fast → increase KL beta; reduce LR; measure KL and entropy next 200 steps.
  ```

**Session 2 ends — checklist, oral exam, artifact**

- Checklist:
  - run a GRPO loop end-to-end (sample→reward→advantage→clip/KL update)
  - read basic curves and decide whether it’s learning vs hacking
  - make one knob change with a hypothesis
- 5-question oral exam:
  1. Why does GRPO not need a critic?
  2. Why is advantage constant over tokens in the simplest GRPO framing?
  3. What does group size K trade off?
  4. Where can KL enter: shaping vs explicit penalty?
  5. What curve pattern screams “reward hacking”?
- Artifact: `days/Day03/grpo_toy.py` + `days/Day03/TIER01.log` + `days/Day03/notes/debug_playbook.md`.

---

### Session 3 (Microtasks 09–12): Spaced repetition (harder drills + mapping to real tooling)

#### Microtask 09 — Reward hacking drill (break it on purpose, then fix it)

- Timebox: 20 minutes
- Inputs: `days/Day03/grpo_toy.py` (hack mode)
- Steps:
  1. Run the “hackable reward” mode and observe the model exploit it.
  2. Harden the reward with one anti-cheat constraint (fail closed / penalty / gating).
  3. Rerun and show that the exploit no longer improves reward without improving success.
- Pass/fail:
  - PASS if you can produce: exploit evidence → fix → metric reversal (reward stops lying).
  - FAIL if you “fix” it without proving the exploit is dead.
- Expected artifact snippet (append to `days/Day03/TIER02.log`):

  ```text
  Hack: reward↑, success flat, KL↑. Fix: add penalty; now reward tracks success.
  ```

#### Microtask 10 — Knob sweep (K, KL β, clip ε, temperature)

- Timebox: 20 minutes
- Inputs: `python3 days/Day03/run_sweep.py`
- Steps:
  1. Sweep K ∈ {4, 8, 16} and KL β ∈ {0.0, 0.05, 0.2}.
  2. Save a small JSON report: final success, KL, entropy, diversity.
  3. Write one sentence: “best setting for this toy task and why”.
- Pass/fail:
  - PASS if you can defend one setting using the metrics (not vibes).
  - FAIL if you pick the highest reward with collapsing diversity/KL blow-up.
- Expected artifact snippet (commit `days/Day03/eval/sweep_results.json`):

  ```json
  {"K":16,"kl_beta":0.05,"success":0.62,"kl":0.09,"entropy":1.21,"diversity":0.77}
  ```

#### Microtask 11 — Map GRPO to 3 practical pathways (A/B/C)

- Timebox: 15 minutes
- Inputs: your notes; the baseline “tools” section above
- Steps:
  1. Write a single-page mapping: what corresponds to “dataset item”, “group sampling”, “grader”, “KL control”, “metrics”.
  2. Do it for:
     - (A) OpenAI RFT-style managed loop
     - (B) TRL `GRPOTrainer`
     - (C) Unsloth GRPO recipe
- Pass/fail:
  - PASS if you can point to exactly where reward function is injected in each path.
  - FAIL if you can’t name what to log and where to read it.
- Expected artifact snippet (commit `days/Day03/notes/framework_mapping.md`):

  ```text
  A/OpenAI-RFT: grader = reward; platform samples K and updates policy; you watch reward/KL.
  B/TRL: reward_fn(batch)->rewards; GRPOTrainer handles sampling+update; you log via callbacks.
  C/Unsloth: recipe wires reward + fast generation; you tune K/KL/temperature for stability.
  ```

#### Microtask 12 — Capstone definition (verifiable task + grader + eval)

- Timebox: 20 minutes
- Inputs: your product interests; RLVR use-case list
- Steps:
  1. Pick a verifiable task (math, tests, tool JSON validity, routing).
  2. Define: dataset, reward/grader, anti-cheat, baseline eval, GRPO run plan, ablations.
  3. Fill out `days/Day03/CAPSTONE.md`.
- Pass/fail:
  - PASS if your grader is deterministic and your eval can catch reward hacking.
  - FAIL if “success” is subjective preferences without a consistent judge.
- Expected artifact snippet (in `days/Day03/CAPSTONE.md`):

  ```text
  Task: code correctness on 50 unit-test prompts.
  Reward: pass-rate (1/0) + penalty for timeouts; anti-cheat: sandbox + output schema.
  ```

**Session 3 ends — checklist, oral exam, artifact**

- Checklist:
  - demonstrate and kill one reward hack
  - run a knob sweep and justify settings from metrics
  - map GRPO concepts to OpenAI/TRL/Unsloth implementations
  - define a real RLVR capstone with deterministic grading
- 5-question oral exam:
  1. What is the strongest argument for GRPO over PPO in RLVR?
  2. What knob most directly controls “policy drift” and how do you measure it?
  3. How can reward shaping help sparse rewards without changing the true optimum?
  4. Why can “reward up, success flat” happen?
  5. What is one plausible benefit of GSPO-style sequence tweaks?
- Artifact: `days/Day03/run_sweep.py`, `days/Day03/CAPSTONE.md`, `days/Day03/notes/framework_mapping.md`.

---

## C) Diagnostic dashboard spec (GRPO-specific)

Log these **per step** and plot as curves. If you don’t log it, you can’t debug it.

| Signal | What it is | Good looks like | Bad looks like | If bad, do this (and re-measure) |
| --- | --- | --- | --- | --- |
| `reward_mean` | mean raw reward across all samples | steady ↑ then plateau | ↑ only on train prompts | tighten grader; add OOD eval; add anti-cheat |
| `success_rate` | task-specific pass rate (verifiable) | tracks reward ↑ | reward↑ but success flat | reward hacking → change reward, not LR |
| `kl_mean` | mean KL(policy || ref) | bounded, slow drift | spikes / runaway | increase KL β; lower LR; reduce epochs |
| `entropy_mean` | token entropy (diversity proxy) | moderate; not collapsing | collapses to near 0 | increase temperature; reduce KL pressure; add diversity incentives |
| `clipfrac` | fraction clipped in PPO objective | low/moderate | ~0 always or ~1 always | if ~0: LR too small / not moving; if ~1: LR too big |
| `adv_mean/std` | advantage stats (after normalization) | mean≈0, std stable | std→0 or huge | if std→0: reward too flat; if huge: reward too noisy → increase K |
| `group_diversity` | unique outputs / K per prompt | not collapsing | collapses rapidly | raise temperature; penalize duplicates; increase K |
| `len_mean` / `reasoning_tokens_mean` | length / reasoning tokens | stable or justified | “thinking tax” (len↑, reward flat) | penalize verbosity; gate reward on correctness first |

**Primary knobs (turn with a hypothesis):**

- **Group size K:** bigger K → lower-variance baseline, better exploration, more compute.
- **KL β:** bigger β → less drift, more stability, potentially slower improvement.
- **Clip ε:** smaller ε → more conservative updates; too small → stalled learning.
- **Sampling temperature:** higher → more exploration/diversity; too high → noisy rewards.
- **Reward shaping:** add intermediate/dense signals to avoid dead learning; verify it doesn’t change the target behavior.

---

## D) Final 1% competency rubric

You’re “top-1% GRPO” only if you can do all of this on a fresh RLVR task without hand-holding:

1. **Explain precisely (math + intuition)**
   - GRPO vs PPO vs RLHF vs DPO: what objective is optimized; what data is needed; what failure modes dominate.
   - Why group-relative baseline works; why critic removal is a compute win; why KL is non-negotiable.

2. **Implement from scratch**
   - Write a minimal GRPO loop (group sampling, group-relative advantage, PPO clipping, KL penalty) and show it improves a verifiable metric.
   - Demonstrate that sparse reward requires a foothold or shaping and fix it.

3. **Operate real tooling**
   - Run GRPO with TRL and with Unsloth on an open model; reproduce results; run ablations.
   - Build deterministic graders and harden them (anti-cheat, fail closed, gating).

4. **Debug like an operator**
   - Given curves alone (reward/KL/entropy/clipfrac/diversity/length), diagnose the failure mode and prescribe fixes with expected metric changes.
   - Prove you killed at least one reward hack with before/after evidence.

5. **Choose correctly**
   - Map product problems to: GRPO (RLVR) vs DPO/RLHF vs SFT; defend the choice with measurability, cost, and safety.

6. **Ship a capstone**
   - A reproducible case study with: baseline eval, GRPO run, ablations, debugging story, and a readme another engineer can follow.
