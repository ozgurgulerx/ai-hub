# Day 009 – Storage Paths: NVMe vs Network & Staging
## Tier 3 – Storage Layout & Bootstrap Story

> **Goal**: Turn your NVMe vs network vs staged measurements into a **storage layout and bootstrap recommendation** for a real vLLM service.
>
> **Outcome**: A short, consulting-ready note you can reuse when designing inference nodes and bootstrap scripts.

---

## Tier 3 – Stretch (Optional / Ambitious)

**Title** – Storage Layout & Bootstrap Story  
**Time Budget** – ~60–90 min

---

### 0) Summarize storage options for this node

In `storage_layout_bench.md` (or a new `storage_layout_notes.md`), add a section that:

- Lists available storage types (NVMe, network, any other local disks).  
- Summarizes measured cold-load times for:
  - NVMe,  
  - network-like path,  
  - staged path (network → NVMe).

Keep it concrete and specific to this machine + SLM.

---

### 1) Draft a storage layout recommendation

Write 4–6 bullets that answer:

- **Where should model weights live in steady state?** (NVMe, network, both?)  
- **When, if ever, should you stage from network to NVMe?** (e.g., at deploy time only.)  
- **What’s acceptable for:**
  - dev/test nodes,  
  - internal services,  
  - user-facing endpoints.

Anchor each bullet in numbers from `storage_layout_bench.csv` (even if approximate).

---

### 2) Connect to a future “bootstrap script”

Using the deliverable idea from `learning_goals.md` (bootstrap script around Day 3) and your storage insights:

- Sketch, in prose or pseudo-shell, what a **node bootstrap script** might do for storage:
  - ensure NVMe mount is present and has space,  
  - optionally stage models from network to NVMe,  
  - optionally pre-warm page cache (Day 008 script),  
  - then start vLLM with your chosen flags.

Capture this as a small section like:

> **“If I owned this node’s bootstrap”**, I would:
> - …

This doesn’t need to be fully implemented yet, but it sets you up for a concrete script later in Phase 0.

---

### 3) Three production-minded takeaways

End with three opinionated bullets such as:

- “For this GPU + SLM, running directly from network is only acceptable for dev; production should stage to NVMe first.”  
- “Cold-start time from NVMe is ~X s; from network it’s ~Y s. For user-facing services, we should hide cold starts behind pre-warm and/or warm pools.”  
- “Bootstrap scripts should treat NVMe space and model placement as first-class, not an afterthought.”

---

### Expected Artifact

- Updated `storage_layout_bench.md` (or new `storage_layout_notes.md`) with:
  - storage layout summary,  
  - recommendation bullets,  
  - a bootstrap-script sketch,  
  - three production takeaways.

