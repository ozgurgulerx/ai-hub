# Day 012 – vLLM in Docker (GPU Containerization)
## Tier 1 – NVIDIA Container Toolkit & GPU Smoke Test

> **Goal**: Install or verify NVIDIA Container Toolkit and run a simple `nvidia-smi` container to prove the container runtime can see the GPU.
>
> **Outcome**: A short note + helper script showing a working GPU test container on this node.

---

## Tier 1 – Must Do (Core Block)

**Title** – NVIDIA Container Toolkit & GPU Smoke Test  
**Time Budget** – ~60–90 min

---

### 0) Capture current Docker / runtime state

Commands (run manually and paste outputs into notes):

- `docker --version` (or `podman --version` if applicable)  
- `docker info` (check for `nvidia` runtime / GPU plugin hints)  

Create:

- `days/day-012-vllm-in-docker/docker_gpu_smoke_test.md`

Record:

- Docker version, storage driver, and any GPU/runtime hints from `docker info`.

---

### 1) Install or verify NVIDIA Container Toolkit

Follow NVIDIA’s docs for your distro (Ubuntu/RHEL, etc.). High‑level steps:

- Add NVIDIA Container Toolkit repo.  
- Install `nvidia-container-toolkit`.  
- Configure the container runtime (e.g., update `/etc/docker/daemon.json` to use the NVIDIA runtime).  
- Restart Docker.

Document **exact commands** in `docker_gpu_smoke_test.md` (even if you ran them earlier on this node).

If Toolkit is already installed, just confirm its version and note that here.

---

### 2) Run a GPU test container

Create:

- `days/day-012-vllm-in-docker/run_nvidia_smi_container.sh`

Stub responsibilities:

- Run something like:

  ```bash
  docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
  ```

- Exit non‑zero if it fails.

Run the script and capture:

- `nvidia-smi` output inside the container,  
- any errors or warnings (e.g., missing drivers or runtime misconfig).

Add a short conclusion to `docker_gpu_smoke_test.md`:

- “GPU in container: OK / not OK, with reasons.”

---

### Expected Artifact

- `days/day-012-vllm-in-docker/docker_gpu_smoke_test.md`  
- `days/day-012-vllm-in-docker/run_nvidia_smi_container.sh`

