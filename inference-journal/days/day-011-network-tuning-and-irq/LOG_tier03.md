# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog
## Tier 3 – NIC IRQ Affinity & Network Tuning Story

> **Goal**: Map NIC interrupts to CPUs, sketch a sane IRQ affinity plan, and fold `somaxconn`, MTU, and IRQ tuning into a concise network-tuning story for inference nodes.
>
> **Outcome**: A short note that describes how you’d treat network tuning on a production vLLM box, with concrete references to this node’s layout.

---

## Tier 3 – Stretch (Optional / Ambitious)

**Title** – NIC IRQ Affinity & Network Tuning Story  
**Time Budget** – ~60–90 min

---

### 0) Map NIC IRQs

Commands:

- `grep -iE "eth0|ens|eno" /proc/interrupts` (adjust regex for your NIC names)  
- `lscpu` or `numactl --hardware` to see CPU and NUMA layout  
- `ethtool -l <iface>` (if available) to see queue/channels info

In `network_tuning_bench.md`, capture:

- Which IRQ lines correspond to your NIC queues,  
- Which CPUs they currently land on (from `/proc/interrupts`).

---

### 1) Sketch an IRQ affinity plan (even if you don’t apply it)

For a GPU inference node, a common pattern is:

- Bind NIC IRQs to CPU cores **local to the NIC’s NUMA node** (and ideally near the GPU’s NUMA node if possible).  
- Avoid blasting interrupts across all cores if unnecessary.

In your notes:

- Identify which CPU cores would be reasonable targets for NIC IRQs (e.g., a small subset near the GPU).  
- Draft how you’d use `irqbalance` settings or write to `/proc/irq/<N>/smp_affinity` to achieve that on a lab box.

If you’re not going to change anything on this host, keep this at the “plan” level.

---

### 2) Fold everything into a network-tuning “playbook snippet”

Add a final section to `network_tuning_bench.md` (or a new `network_tuning_notes.md`) titled, e.g., **“Network Tuning Baseline for vLLM Nodes”** with:

- `somaxconn` recommendation and why.  
- MTU / jumbo frames recommendation and under what conditions.  
- IRQ affinity recommendation (or “leave as default” if that’s your conclusion).  
- A reminder that **Day 010 HTTP latency** is your baseline and how you’d check if tuning helped or hurt.

Make it something you could drop into a larger “node bootstrap” or SRE runbook later.

---

### Expected Artifact

- Updated `network_tuning_bench.md` (or new `network_tuning_notes.md`) with:
  - NIC IRQ mapping,  
  - an affinity plan sketch,  
  - a 4–6 bullet “network tuning baseline” for vLLM inference nodes.

