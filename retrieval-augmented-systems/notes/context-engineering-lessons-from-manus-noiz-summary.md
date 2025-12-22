# Context Engineering Lessons from Manus — Notes

Summary for: https://youtu.be/OaUOHEHtlOU  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-transcript  
Status: **To verify**

## KV Cache / Prompt Stability

- Place dynamic system variables (e.g., date, tool lists) at the **end** of the context window because changing them early can kill KV cache reuse and force recomputation (cost/latency impact). [Unverified]
- Cache hits are described as requiring static, unchanging token sequences; changing prefix tokens or breaking continuity implies cache misses. [Unverified]
- Provider-side “dynamic caching” is described as opaque: providers may precompute/store repeated sequences, but users don’t control cache decisions. [Unverified]
- Cache evaluation is described as relying on provider usage metrics; a suggested test is repeating the same request and checking whether caching triggers for a shared prefix (may require larger context windows). [Unverified]

## Tool Calling Optimization (Prompt + UX)

- Mask dynamic tools when not in use to reduce irrelevant choices and improve tool selection. [Unverified]
- Repeating key actions in long tool-call sequences is described as improving throughput by reducing drift (example: ~50 tool calls per sequence). [Unverified]
- Store incorrect tool-call sequences as “stack traces” for debugging and self-correction. [Unverified]
- Adjust tool availability by mode/context (example: “work mode” vs “non-work mode”) to prevent inappropriate tool selection. [Unverified]

## Constrained Decoding / Structured Output

- When the model emits an “action token”, providers are described as being able to restrict decoding to tokens that match the tool specification (constrained decoding for determinism). [Unverified]
- “Tool calling / structured output / function calling” are framed as interchangeable: constraining output into a deterministic program for machine consumption rather than human readability. [Unverified]
- Tool naming is described as materially affecting tool-calling accuracy and requires iterative intuition-building. [Unverified]

## Context Management + Prompting Tactics

- Context compression is described as improving efficiency by including only relevant context and using URLs instead of full content when possible. [Unverified]
- Few-shot prompting is described as effective when using minimal tokens and carefully chosen examples (similar/opposite/unrelated), avoiding identifiers models struggle to remember. [Unverified]
- For smaller models, avoid dumping full stack traces during error recovery; they may get lost in details. [Unverified]
- System messages are described as having special impact; place them early for maximum effect (training-dependent). [Unverified]
- Repetition/recitation strategies can reinforce important info but should be used judiciously to avoid overload. [Unverified]

## Implementation Notes (As Described)

- Tokenizer vocabulary is described as affecting tool-calling success (especially for smaller models with long context). [Unverified]
- Caching optimization is framed as improving speed/cost for prompts that already work, not as a substitute for initial prompt iteration. [Unverified]

