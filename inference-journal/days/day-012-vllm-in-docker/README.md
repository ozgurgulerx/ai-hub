# Day 012 – vLLM in Docker (GPU Containerization)

**Phase:** 0 – OS & GPU Setup (Days 1–15)  
**Theme:** Take your tuned bare‑metal node and **containerize** vLLM: install NVIDIA Container Toolkit, run a GPU‑enabled vLLM SLM container, and sketch a `docker-compose.yml` you’d actually keep.

**Layers**

- **Platform** → Docker + NVIDIA Container Toolkit on a GPU node  
- **Inference Runtime** → vLLM SLM running inside a container, with GPU and volumes  
- **Product / SLO** → how containerization interacts with your existing OS/network/storage tuning

---

## Snapshot (Today’s Focus)

By Day 011 you have:

- A tuned bare‑metal node: GPU drivers, NUMA/CPU settings, THP/hugepages, storage, and basic network tuning.  
- vLLM SLM running directly on the host, with good TTFT, storage, and HTTP baselines.

Day 012 is about **bridging into the Platform layer**:

- Prove that Docker + NVIDIA Container Toolkit see the GPU correctly.  
- Run the same SLM vLLM server in a container, with equivalent flags and volumes.  
- Start a simple `docker-compose.yml` that reflects how you’d deploy this in a lab or small service.

Assumptions:

- Docker (or compatible container runtime) is installed or can be installed.  
- You either have, or can choose, a base image for vLLM (official image or a Python base + `pip install vllm`).

---

## Tier Breakdown

| Tier  | Time        | Scope |
|------:|------------:|-------|
| Tier 1| ~60–90 min  | Install/verify NVIDIA Container Toolkit; run GPU `nvidia-smi` test container |
| Tier 2| ~75–120 min | Run vLLM SLM in a GPU‑enabled container (host‑equivalent config) |
| Tier 3| ~60–90 min  | Sketch a `docker-compose.yml` and capture a “containerized vLLM node” baseline |

---

## Navigation

- **[Tier 1 – NVIDIA Container Toolkit & GPU Smoke Test](./LOG_tier01.md)**  
- **[Tier 2 – vLLM SLM Server in Docker](./LOG_tier02.md)**  
- **[Tier 3 – docker-compose Baseline for vLLM Node](./LOG_tier03.md)**

---

## Cross-Day Context

- **Days 001–011** gave you a tuned host: OS, CPU/NUMA, memory, storage, and networking, plus detailed TTFT and capacity behavior for an SLM vLLM server.  
- **Day 012** starts the **Platform** layer by making sure your container runtime can inherit (or at least not fight) those host‑level decisions.

This day should answer:

- “How do I run the same vLLM config inside Docker with GPU support?”  
- “What volumes/env do I need for models and configs?”  
- “What would a realistic `docker-compose.yml` look like for this node?”

---

## Logging Template (Day 012)

Use this at the end of the day to summarize.

```markdown
# Day 012 – vLLM in Docker (GPU Containerization)

## Environment
- GPU:
- OS / kernel:
- Docker / container runtime versions:
- NVIDIA Container Toolkit version:

## Commands Run
- Toolkit install commands
- docker run / docker compose commands

## Key Numbers / Checks
- `docker run` GPU test output (nvidia-smi OK?):
- vLLM container health (can you hit /v1/models?):

## Artifacts Created/Updated
- day-012-vllm-in-docker/docker_gpu_smoke_test.md
- day-012-vllm-in-docker/run_nvidia_smi_container.sh
- day-012-vllm-in-docker/Dockerfile.vllm-slm (optional)
- day-012-vllm-in-docker/run_vllm_container.sh
- day-012-vllm-in-docker/docker-compose.yml

## Observations / Surprises
- Any differences vs bare‑metal vLLM behavior?
- Volumes/env or permissions that were tricky?
- How ready does this feel as a building block for Phase 1?
```

