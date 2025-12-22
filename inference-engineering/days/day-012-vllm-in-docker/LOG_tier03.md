# Day 012 – vLLM in Docker (GPU Containerization)
## Tier 3 – docker-compose Baseline for vLLM Node

> **Goal**: Sketch a `docker-compose.yml` that captures your containerized vLLM SLM service in a way you’d actually reuse on a lab node.
>
> **Outcome**: A minimal but realistic Compose file + a few notes on how it would evolve in Phase 1.

---

## Tier 3 – Stretch (Optional / Ambitious)

**Title** – docker-compose Baseline for vLLM Node  
**Time Budget** – ~60–90 min

---

### 0) Create a minimal `docker-compose.yml`

Create:

- `days/day-012-vllm-in-docker/docker-compose.yml`

Target structure:

```yaml
version: "3.9"
services:
  vllm-slm:
    image: <your-vllm-image>
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: ["gpu"]
    ports:
      - "8000:8000"
    environment:
      MODEL: "microsoft/Phi-3-mini-4k-instruct"
    volumes:
      - /path/to/models:/models:ro
    command: >
      python -m vllm.entrypoints.openai.api_server
      --model ${MODEL}
      --dtype auto
      --max-model-len 4096
      --gpu-memory-utilization 0.92
      --port 8000
```

Leave placeholders (`<your-vllm-image>`, `/path/to/models`) and note them clearly.

---

### 1) Capture how this ties into Phase 0/Phase 1

In `vllm_container_notes.md` (or a new `compose_notes.md`), add:

- How this Compose file maps to your bare‑metal launch scripts and tunings (e.g., same flags, ports).  
- What you would add later:
  - healthchecks,  
  - resource limits,  
  - logging volumes,  
  - maybe a small client container.

Keep this focused on **structure**, not Kubernetes yet.

---

### 2) Three bullets you’d tell a teammate

End with three bullets along the lines of:

- “This Compose file gives us a reproducible vLLM SLM service on a tuned GPU node.”  
- “GPU visibility is handled via the NVIDIA runtime / device reservations; model weights are mounted read‑only from host.”  
- “Phase 1 will likely split this into separate Compose stacks (chat vs batch) or move to Kubernetes, but this is a solid lab baseline.”

---

### Expected Artifact

- `days/day-012-vllm-in-docker/docker-compose.yml`  
- Updated `vllm_container_notes.md` (or `compose_notes.md`) with notes on how you’d evolve this into a more complete platform config.

