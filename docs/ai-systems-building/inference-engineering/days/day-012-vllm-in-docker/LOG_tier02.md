# Day 012 – vLLM in Docker (GPU Containerization)
## Tier 2 – vLLM SLM Server in Docker

> **Goal**: Run your SLM vLLM server inside a GPU‑enabled container, with equivalent flags and model paths to your bare‑metal setup.
>
> **Outcome**: A runnable containerized vLLM SLM, plus notes on image choice, volumes, env, and any gotchas.

---

## Tier 2 – Deepen (If Time/Energy Allow)

**Title** – vLLM SLM Server in Docker  
**Time Budget** – ~75–120 min

---

### 0) Choose an image strategy

Pick one approach:

- Use an **official vLLM image** (if available), or  
- Build your own from a CUDA/PyTorch base.

If building your own, create:

- `days/day-012-vllm-in-docker/Dockerfile.vllm-slm`

Skeleton idea (fill in later when you’re on the box):

- Base: CUDA + Python image (e.g., `nvidia/cuda:12.4.0-runtime-ubuntu22.04`).  
- Install Python deps (`pip install vllm` and friends).  
- Set entrypoint to `python -m vllm.entrypoints.openai.api_server ...`.

Record the chosen strategy in a new note:

- `days/day-012-vllm-in-docker/vllm_container_notes.md`

---

### 1) Run vLLM SLM as a container

Create:

- `days/day-012-vllm-in-docker/run_vllm_container.sh`

Stub responsibilities:

- `docker run --rm --gpus all \`  
  `  -p 8000:8000 \`  
  `  -v /path/to/models:/models:ro \`  
  `  -e MODEL="microsoft/Phi-3-mini-4k-instruct" \`  
  `  <your-vllm-image> \`  
  `  python -m vllm.entrypoints.openai.api_server ...`

Adapt:

- MODEL, ports, and flags to match Day 007’s `serve_slm_vllm.sh`.  
- Ensure the container can see the same weights location (via `-v`).

Verify:

- `curl http://127.0.0.1:8000/v1/models` from the host.  
- Optionally run Day 007’s `ttft_probe.py` against the container endpoint.

Capture any differences vs bare‑metal (latency, memory, behavior) in `vllm_container_notes.md`.

---

### 2) Record container vs bare‑metal observations

In `vllm_container_notes.md`, add a short section:

- “Bare‑metal vs Docker”:
  - Any noticeable TTFT / throughput differences at low concurrency.  
  - Any changes in GPU memory usage or logs.  
  - Any friction setting up volumes or environment variables.

Don’t over‑optimize; the goal is to **prove parity**, not squeeze perf yet.

---

### Expected Artifact

- `days/day-012-vllm-in-docker/Dockerfile.vllm-slm` (if you build your own)  
- `days/day-012-vllm-in-docker/run_vllm_container.sh`  
- `days/day-012-vllm-in-docker/vllm_container_notes.md`

