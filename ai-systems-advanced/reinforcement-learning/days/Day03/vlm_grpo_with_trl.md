# VLM GRPO Post-Training with 🤗 TRL (Practical Notes)

This is a **multimodal** (vision + language) adaptation of the Day03 GRPO workflow: dataset → generate **K** completions per prompt → compute **verifiable** reward → GRPO update (clip + KL control) → evaluate.

Primary external reference (readable walkthrough): `https://pub.towardsai.net/training-your-reasoning-model-with-grpo-a-practical-guide-for-vlms-post-training-with-trl-266411c0b844`

## 1) RL framing (map RL components to a VLM)

- **Agent**: the VLM policy model (the thing you’re updating).
- **State**: the input context (e.g., system prompt + image + text question).
- **Action**: the next token (VLM still generates tokens autoregressively).
- **Policy**: `πθ(y|x)` over completions `y` given prompt `x`.
- **Reward**: your grader signal (format correctness, answer correctness, tool-use correctness, etc.).
- **Trajectory**: the generated token sequence (often reward is *terminal* / end-of-sequence).

## 2) What GRPO is optimizing (intuition)

GRPO is a PPO-style policy-gradient update that:

- Samples **a group** of completions per prompt (`K` generations).
- Computes a **group-relative advantage** (baseline = group mean reward, often normalized).
- Applies **ratio clipping** (PPO stability) and **KL-to-reference** control (prevents drift).
- Avoids a learned value model/critic (one reason it’s simpler/cheaper than PPO in many LLM/VLM settings).

Operator interpretation:

- If one completion in the group scores better than its peers, GRPO increases probability of the tokens that produced it (conservatively).
- If the policy drifts too far from the reference, the KL penalty pushes it back.

## 3) “Reasoning traces” + reward design (format + accuracy)

If you want the model to emit structured reasoning + an answer, treat it as a **format constraint** and put it in the reward.

Example target format:

```text
<think> ...reasoning... </think><answer> ...final answer... </answer>
```

Operational note: many production systems *do not* expose full reasoning traces to users. If you train on explicit `<think>` traces, decide upfront whether that trace is meant to be user-visible, internal-only, or stripped at serving time.

Typical two-part reward (common RLVR pattern):

1) **Format reward**: `1.0` if the completion matches the required `<think>...</think><answer>...</answer>` structure, else `0.0`.
2) **Accuracy reward**: verify the final answer against the ground truth (prefer verifiable checks over judge models when you can).

Notes for math-style tasks:

- If the dataset answer is LaTeX, parse + verify **equivalence** (not string equality) when possible.
- If verification fails, “fail closed” (return `0` or `None` consistently) to reduce reward hacking.

### Reward sketches (concrete)

Format reward is often just a regex gate:

```python
import re

FORMAT_RE = re.compile(
    r"^<think>\\n.*?\\n</think>\\n<answer>\\n.*?\\n</answer>$", re.DOTALL | re.MULTILINE
)

def format_reward(text: str) -> float:
    return 1.0 if FORMAT_RE.match(text) else 0.0
```

Accuracy reward should be verifiable. For math, prefer equivalence checking over string matching:

- LaTeX-equivalence: parse and verify symbolic equivalence when possible.
- Fallback: normalized string equality only when parsing isn’t possible.

## 4) TRL wiring (what to implement)

At a minimum you need:

- A dataset with fields like: `prompt` (already formatted with the model’s chat template), `image` (or image path), and optionally `solution` / `answer`.
- A reward function that can evaluate generated completions (ideally deterministic).
- GRPO settings that control:
  - `K` (group size): often `num_generations` or `group_size` depending on TRL version.
  - Max completion length (`max_completion_length` / `max_new_tokens`).
  - KL control (`beta` / `kl_beta`) and PPO clip range (`clip_range` / `clip_eps`).

For multimodal models, you typically use:

- `AutoProcessor` (or model-specific processor) to build inputs from image + text.
- A VLM class (model-specific) that can generate conditioned on image inputs.

### Minimal config knobs (how they map to GRPO)

These are the “operator” knobs you’ll tune most:

- `num_generations` / `group_size` (K): how many samples per prompt form a group.
- `max_completion_length` / `max_new_tokens`: caps compute per sample (and affects reward sparsity).
- `learning_rate`, `num_train_epochs`, `per_device_train_batch_size`: training throughput/stability.
- `beta` / `kl_beta`: KL-to-reference strength (prevents drift / nonsense).
- `clip_range` / `clip_eps`: PPO-style ratio clipping (prevents destructive updates).

Example starter values (from the referenced walkthrough; treat as “works on one setup”, not gospel):

- `learning_rate = 1e-5`
- `num_train_epochs = 1`
- `per_device_train_batch_size = 2`
- `max_completion_length = 1024`
- `num_generations = 2`
- `max_prompt_length = 2048`
- log/save every ~`10` steps

## 5) Dataset transformation (VLM chat prompt)

Common pattern:

- System prompt: instruct the model to output `<think>` then `<answer>`.
- User content: include the image + the textual problem.
- Convert to a single prompt string using the model’s chat template (processor helper).

This keeps GRPO’s “prompt → K completions → reward” loop identical to text-only training; only input construction differs.

### Minimal “conversation” shape (typical)

Most VLMs want something like:

- `system`: the `<think>/<answer>` formatting instruction
- `user`: `[{"type": "image"}, {"type": "text", "text": "<problem>"}]`

Then you apply the model’s chat template to get a single `prompt` string.

## 6) Parameter-efficient GRPO (LoRA)

For VLMs, you’ll usually apply LoRA/QLoRA to keep GRPO feasible:

- Use PEFT LoRA on attention projections (commonly `q_proj`, `v_proj` for many transformer backbones; exact module names vary by model).
- Keep the base model (or a reference) frozen for KL control.

## 7) Compute: renting a GPU (optional)

If you don’t have a local GPU, the “rent + SSH” workflow is straightforward:

- Create an instance (any provider), add your SSH public key, then SSH in.
- Clone your training repo, install deps, and ensure your PyTorch build matches CUDA.
- Run training + log metrics (e.g., TensorBoard), and shut the instance down when done to avoid charges.

Concrete “SSH key” commands (provider-agnostic):

```bash
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
```

## 8) Where this helps (practical applications)

VLM GRPO tends to be most valuable when you have:

- **Verifiable outcomes** (math answers, structured outputs, unit tests, tool-call correctness).
- Tasks needing **multi-step reasoning** across image + text (geometry, charts/plots, diagram QA).
- A clear reward that penalizes “getting the right answer for the wrong reason” less than DPO-style preference training would.
