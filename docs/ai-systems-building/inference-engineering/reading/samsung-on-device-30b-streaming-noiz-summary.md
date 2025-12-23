# Samsung on-device “30B under 3GB via streaming” (Noiz summary notes)

Source video (YouTube): `https://www.youtube.com/watch?v=IiItHlD6-WI`

This note captures **claims** from a Noiz transcript summary included in the prompt. Treat specifics as **to verify** until corroborated by primary sources (Samsung technical writeups, conference talks, papers).

## On-device AI (claims)

- Samsung is described as running **~30B parameter models** on-device by compressing “>16GB” memory requirements down to **<3GB** by:
  - streaming only the needed model pieces in real time
  - using **8/4-bit quantization**
  - coordinating **CPU + GPU + NPU** as a single system
- A runtime is described as dynamically reallocating work across CPU/GPU/NPU when bottlenecks occur, framed as enabling “near cloud-level accuracy” while reducing latency and bandwidth.

## Verification checklist

- What the “streaming” mechanism is (layer streaming, expert streaming, paging, KV offload, or something else).
- Where the <3GB figure comes from (weights only vs weights+KV; which quantization; which model architecture).
- What “runtime engine” is being referenced (product name, release, public docs).
- Hardware assumptions (which Samsung devices/SoCs/NPUs) and performance metrics (tokens/s, latency, quality).

## Appendix: Raw Notes (Preserved)

- “Samsung compresses 30B parameter models requiring over 16GB memory down to under 3GB by streaming only needed model pieces in real-time…”
- “Samsung's AI runtime engine dynamically reallocates resources across CPU, GPU, NPU…”
