# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog
## Tier 1 – Backlog Knob (`somaxconn`) + HTTP Bench

> **Goal**: Inspect and (optionally) set `net.core.somaxconn`, then reuse Day 010’s HTTP bench at modest concurrency to see if backlog tuning has any visible effect.
>
> **Outcome**: A short note that documents `somaxconn` on this node, what you changed (if anything), and whether it affected your HTTP p50/p95 under small load.

---

## Tier 1 – Must Do (Core Block)

**Title** – Backlog Knob (`somaxconn`) + HTTP Bench  
**Time Budget** – ~60–90 min

---

### 0) Capture current `somaxconn` and basic network config

Create:

- `days/day-011-network-tuning-and-irq/capture_network_config.sh`

Stub responsibilities:

- Print:
  - `sysctl net.core.somaxconn`  
  - `ss -ltn` (listen sockets)  
  - relevant interface info (`ip addr show`, `ip route show`)  

For now, you can just run commands manually and paste into `network_tuning_bench.md`; the script is a convenience for later reuse.

Record:

- Current `net.core.somaxconn` value.  
- Which interface carries vLLM traffic (e.g., `lo` vs `eth0`).

---

### 1) Decide whether you can change `somaxconn`

If you have root and this is a lab box:

- Plan to set:

  ```bash
  sudo sysctl -w net.core.somaxconn=65535
  ```

Otherwise:

- Leave the system setting as-is, but still reason about what you **would** do and how you’d measure it on a controlled node.

In either case, document current and “target” values in `network_tuning_bench.md`.

---

### 2) Reuse Day 010 HTTP bench at modest concurrency

Using `network_latency_bench.py` or your Day 010 setup:

- Pick a simple workload:
  - `concurrency=4` and/or `concurrency=8`, `n≈32–64`.  
- Run the bench **before** applying any `somaxconn` change (if you decide to change it).  
- If you change `somaxconn`, run the same bench **after**.

Record:

- median and p95 wall-time before/after.  
- Any visible changes in error behavior (connection refused, drops) if you push concurrency a bit (e.g., 16).

Don’t expect dramatic differences at small loads; the goal is to tie the knob to scenarios where it *would* matter (connection spikes, many pending accepts).

---

### 3) Interpret `somaxconn` in context

Create:

- `days/day-011-network-tuning-and-irq/network_tuning_bench.md`

Add a short section:

- Current vs target `somaxconn` values.  
- Any observed differences in your HTTP bench (even “no visible change at these loads”).  
- A **mental model** of when backlog matters:
  - high connection rates, many pending accepts, load balancer misconfiguration, etc.  
- One concrete rule of thumb, e.g.:

> “On this node, under moderate concurrency, changing `somaxconn` doesn’t move HTTP latency; it’s primarily a safety knob for high connection rates / LB storms, not a day‑to‑day latency tuner.”

---

### Expected Artifact

- `days/day-011-network-tuning-and-irq/network_tuning_bench.md`  
- `days/day-011-network-tuning-and-irq/capture_network_config.sh`

