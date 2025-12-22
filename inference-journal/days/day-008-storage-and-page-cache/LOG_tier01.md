# Day 008 – Storage & Cold Starts
## Tier 1 – NVMe Cold/Warm Model Load Probe

> **Goal**: Measure how long a cold model load takes from NVMe vs warm (page-cache) loads, and capture the numbers in a reusable benchmark note.
>
> **Outcome**: A small shell script + CSV/markdown that quantify cold vs warm model load times for your SLM on this GPU.

---

## Tier 1 – Must Do (Core Block)

**Title** – NVMe Cold/Warm Model Load Probe  
**Time Budget** – ~60–90 min

---

### 0) Pick the SLM and model path

Reuse the same small model from Day 006/007:

- `microsoft/Phi-3-mini-4k-instruct` or  
- `Qwen/Qwen2.5-1.5B-Instruct`

Record:

- `MODEL = ...`  
- `MODEL_PATH = ...` (if you have a local clone/weight directory)

Assumption: weights reside on a local NVMe-backed filesystem (e.g., `/mnt/nvme0/models/...`).

---

### 1) Create a simple model-load timing script

Create:

- `days/day-008-storage-and-page-cache/measure_model_load.sh`

Purpose:

- Start vLLM with your SLM,  
- time from “server start” → “ready to serve” (or first successful `/v1/models` call),  
- record the timing and GPU memory usage to a CSV.

Suggested structure (pseudo-steps):

1. Accept `MAX_MODEL_LEN` (or other flags) as env/args if needed.  
2. `t0 = now`.  
3. Launch `python -m vllm.entrypoints.openai.api_server ...` (similar to Day 007 `serve_slm_vllm.sh`).  
4. Poll `http://127.0.0.1:8000/v1/models` until it responds.  
5. `t1 = now`; record `load_s = t1 - t0`.  
6. Snapshot GPU memory via `nvidia-smi --query-gpu=memory.used`.  
7. Append a row to `storage_load_bench.csv`.

You can start with `time` plus manual measurements if you like, but aim for a small script that’s re-runnable.

---

### 2) Define the CSV + markdown outputs

Create (initial, empty files):

- `days/day-008-storage-and-page-cache/storage_load_bench.csv`  
- `days/day-008-storage-and-page-cache/storage_load_bench.md`

CSV header:

```text
run_id,mode,model,max_model_len,load_s,gpu_mem_used_mb,notes
```

Where:

- `mode` ∈ `{cold, warm}`,  
- `run_id` is a simple index or timestamp,  
- `notes` can capture minor config changes.

Markdown outline (`storage_load_bench.md`):

- Server config (model, flags, GPU, storage path).  
- Table summarizing cold vs warm runs.  
- Short interpretation paragraph (see below).

---

### 3) Run cold vs warm sequences (NVMe)

Procedure (example):

1. Ensure page cache is as cold as is safe on this box (e.g., reboot, or use `echo 3 > /proc/sys/vm/drop_caches` only if you understand the impact).  
2. Run the timing script once → `cold_1`.  
3. Stop the server, wait a bit, then run again without dropping caches → `warm_1`.  
4. Optionally run `warm_2`, `warm_3` to see variance.

Record at minimum:

- `cold_1` load time,  
- `warm_1` load time,  
- GPU memory used at ready state.

---

### 4) Interpret the numbers (storage slice)

In `storage_load_bench.md`, write a short, storage-focused interpretation:

- How much slower is `cold_1` vs `warm_1`? (factor and absolute difference.)  
- Does the difference roughly match what you’d expect from “page cache fill” from Day 006/007’s mental models?  
- For your SLM and NVMe, is cold-start load time acceptable for:
  - a demo environment,  
  - a small internal service,  
  - or a latency-sensitive external endpoint?

Try to frame it in SRE terms:

> “On this node, cold model load (~X s) is acceptable only if we reboot rarely and pre-warm on deploy; warm reloads (~Y s) are fine for rolling restarts.”

---

### Expected Artifact

- `days/day-008-storage-and-page-cache/measure_model_load.sh`  
- `days/day-008-storage-and-page-cache/storage_load_bench.csv`  
- `days/day-008-storage-and-page-cache/storage_load_bench.md`

