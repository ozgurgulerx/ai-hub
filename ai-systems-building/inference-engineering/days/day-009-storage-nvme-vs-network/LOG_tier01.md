# Day 009 – Storage Paths: NVMe vs Network & Staging
## Tier 1 – NVMe vs Network Path Model Load

> **Goal**: Measure cold model load time from **local NVMe** vs a **network-like path**, and capture the difference in a small benchmark table.
>
> **Outcome**: A CSV + markdown note that quantify how much slower (or similar) network-backed loads are compared to NVMe for your SLM.

---

## Tier 1 – Must Do (Core Block)

**Title** – NVMe vs Network Path Model Load  
**Time Budget** – ~60–90 min

---

### 0) Identify your storage paths

Decide on:

- `MODEL_PATH_NVME` – the local NVMe-backed directory for your SLM weights (used in Day 008).  
- `MODEL_PATH_NET` – one of:
  - a real network-backed mount (NFS/EFS/SMB/FUSE), **or**  
  - a second, slower disk / path you treat as a “network stand-in”.

Record both paths in your notes.

If you currently **don’t** have a real network path, still fill in `MODEL_PATH_NET` as a placeholder and structure the experiment so you can run it later.

---

### 1) Create a storage-path comparison script

Create:

- `days/day-009-storage-nvme-vs-network/compare_storage_paths.sh`

Purpose:

- For each of `{NVME, NET}`:
  - point vLLM’s `--model` or `MODEL_PATH` at the chosen path,  
  - measure time from launch → ready (similar to Day 008),  
  - append a row to `storage_layout_bench.csv`.

Implementation sketch:

- Either:
  - extend `measure_model_load.sh` to accept a `MODEL_PATH` or `MODE` and call that from this script, **or**  
  - reimplement a minimal timing loop here (consistent with Day 008’s logic).

Target CSV header (see below) will guide which fields to record.

---

### 2) Define the CSV and markdown outputs

Create:

- `days/day-009-storage-nvme-vs-network/storage_layout_bench.csv`  
- `days/day-009-storage-nvme-vs-network/storage_layout_bench.md`

CSV header:

```text
run_id,storage_mode,model,max_model_len,load_s,gpu_mem_used_mb,notes
```

Where:

- `storage_mode` ∈ `{nvme, net}` (or similar labels).  
- `run_id` can be a simple integer or timestamp.  
- `notes` records anything non-default (e.g., “simulated net path on slower SSD”).

Markdown outline (`storage_layout_bench.md`):

- Environment summary (GPU, OS, storage devices/mounts).  
- Server config (model, flags).  
- Table summarizing cold load times for NVMe vs network.  
- Short interpretation paragraph for Tier 1 (see below).

---

### 3) Run minimal cold-load tests for each path

Procedure (for each storage mode):

1. Ensure conditions are roughly comparable (e.g., drop caches or reboot before each **pair** if safe; at minimum, avoid mixing other heavy jobs).  
2. Run your timing script pointing at `MODEL_PATH_NVME` → record `load_s_nvme`.  
3. Run your timing script pointing at `MODEL_PATH_NET` → record `load_s_net`.  
4. If possible, repeat once to gauge variance.

Goal: get at least **one good cold-load measurement** for each path, even if network path is a stand-in.

---

### 4) Interpret the difference

In `storage_layout_bench.md`, write a short, storage-focused comparison:

- Ratio: `load_s_net / load_s_nvme` (e.g., “network path is ~2.5× slower on cold load”).  
- Absolute difference: how many extra seconds does network add?  
- Whether the extra latency feels acceptable for:
  - dev / notebooks,  
  - internal services,  
  - user-facing endpoints.

Tie this back to your Day 008 numbers:

- Is the extra cost dominated by **storage pull** (I/O), or do runtime warm-up and HBM transfer still dominate?  
- Does network-backed load meaningfully change how often you’d tolerate cold starts?

---

### Expected Artifact

- `days/day-009-storage-nvme-vs-network/compare_storage_paths.sh`  
- `days/day-009-storage-nvme-vs-network/storage_layout_bench.csv`  
- `days/day-009-storage-nvme-vs-network/storage_layout_bench.md`

