# Kimi-K2

Kimi-K2 refers to a **Kimi-series** large language model from **Moonshot AI** (the team behind the Kimi assistant), positioned as a reasoning-capable model aimed at strong performance on multi-step tasks (e.g., math, coding, tool-assisted problem solving) and long-context use cases.

This note is intentionally **spec-light**: add official links/papers and verified numbers (context length, sizes, benchmarks) as you collect sources.

## What It Is

- A general-purpose LLM in the Kimi family, commonly discussed in the context of **reasoning** and **agent/tool** workflows.
- Often used as a strong **Chinese + English** model for analysis-heavy tasks and long documents.

## What’s Different / Notable (Compared to “Generic” Chat LLMs)

- **Long-context orientation**: the Kimi line is widely associated with long-context behavior; this tends to matter for reasoning over large inputs (multi-doc synthesis, codebase navigation, lengthy policies/specs).
- **Reasoning-first usage**: commonly evaluated/marketed on multi-step tasks (math/coding), where failure modes are easier to measure and regress.
- **Agent readiness (practical)**: value tends to show up when paired with tool use (retrieval, code execution, search, planning), not just single-turn Q&A.

## Innovations To Track (Add Sources)

Use this as a checklist for what to look for in official releases and third-party writeups:

- **Training recipe for reasoning**: outcome-based vs. process-based supervision, verifier use, synthetic reasoning trace generation.
- **Long-context training**: data strategies, attention/scaling choices, and how well the model maintains correctness deep into context.
- **Attention mechanism**: any confirmed details on Kimi-K2’s attention (e.g., linear-attention variants such as KDA) and their practical trade-offs.
- **Post-training for reliability**: safety alignment, refusal behavior, and reductions in hallucinations on multi-hop tasks.
- **Tool-use competence**: structured function calling, planning stability, and robustness against prompt injection in tool outputs.

## Attention (KDA / “Kimi Diagonal Attention”) — Third-Party Mental Model (Unverified)

This is a useful way to think about “improved linear attention” variants often discussed around Kimi (add a primary source when you find it).

### Two equivalent views of linear attention

- **Fast-memory view**: maintain a per-head “memory” matrix that accumulates key-weighted values; multiplying that matrix by a query yields an attention-like readout without softmax.
- **Optimization view**: the same update can be interpreted as iteratively optimizing a loss that ties keys to values; changing the loss changes what the memory stores and how accurately queries recover values.

### Evolution of the loss / update rule

- **Correlation-style update (naive)**: pushes memory so that matching a key helps retrieve the associated value (inner-product matching).
- **Reconstruction (MSE) update (DeltaNet-style)**: optimizes key→value reconstruction so retrieval becomes more precise than pure correlation.
- **Scalar-gated forgetting (Gated DeltaNet-style)**: adds a decay/gate so older key-value influence fades over time while learning new associations.

### What KDA adds (the “diagonal” gate idea)

Scalar decay forgets everything uniformly within a head. KDA-style gating instead uses a **per-dimension gate** (a diagonal matrix, usually implemented as a vector) so each channel can forget at a different rate. A common decomposition is:

- **Token-dependent gate**: how much to forget *for this token* (per dimension).
- **Token-independent gate**: a learned “baseline” forgetting rate (per dimension).

Implementation notes you’ll often see: rewrite updates in chunks for speed and materialize the diagonal matrix as a vector so inference remains efficient.

## How To Compare Kimi-K2 (Suggested Criteria)

- **Reasoning**: math (GSM8K/MATH), logic (ARC), multi-hop QA (HotpotQA/StrategyQA).
- **Code**: HumanEval/MBPP, repo-level tasks (patch generation, unit-test pass rate).
- **Long-context**: needle-in-haystack, multi-doc synthesis, citation integrity, truncation sensitivity.
- **Agent/tool**: function-call accuracy, tool selection, recovery from tool errors, approval/guardrail compliance.
- **Ops**: latency, cost, rate limits, and determinism (variance under sampling).

## Links (TODO)

- Official announcement / model card:
- Technical report:
- Provider docs / API guide:
