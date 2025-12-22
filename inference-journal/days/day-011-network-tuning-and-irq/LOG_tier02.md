# Day 011 – Network Tuning: MTU, IRQ Affinity & Backlog
## Tier 2 – MTU / Jumbo Frames Introspection & Ping Tests

> **Goal**: Inspect MTU on relevant interfaces, understand whether jumbo frames (MTU 9000) are even viable on this path, and run a couple of ping tests to see latency/variance effects.
>
> **Outcome**: A clear, environment-specific note about whether you *should* enable jumbo frames for this node’s traffic paths, and how you’d verify it.

---

## Tier 2 – Deepen (If Time/Energy Allow)

**Title** – MTU / Jumbo Frames Introspection & Ping Tests  
**Time Budget** – ~75–120 min

---

### 0) Inspect current MTU values

Commands:

- `ip link show`  
- `ip -d link show <iface>` (for more detailed info)  

Record in `network_tuning_bench.md`:

- The interface(s) that matter for vLLM traffic (e.g., `eth0`, `ens3`),  
- Their current MTU values (likely 1500 by default).

---

### 1) Check whether jumbo frames are viable

Jumbo frames (MTU 9000) only help if the **end-to-end path** supports them.

If you have:

- A known peer host (e.g., another node in the same rack),  
- Or a loopback test for your lab,

Design a simple ping test:

```bash
ping -c 5 -s 1472 <peer>         # near 1500 MTU
ping -c 5 -s 8972 <peer>         # near 9000 MTU (if you enable it)
```

You may or may not actually change MTU today; the key is to:

- understand whether jumbo frames are **possible**,  
- and what the failure modes look like (e.g., drops, “Message too long”).

---

### 2) (Optional, if safe) Temporarily enable MTU 9000

Only if you own this node and path:

1. Note current MTU for the interface.  
2. Temporarily set:

   ```bash
   sudo ip link set dev <iface> mtu 9000
   ```

3. Re-run the ping tests and a quick HTTP bench (from Day 010) to see if:
   - packets get through without fragmentation/drops,  
   - latency/variance change at all for your small payloads.

Revert MTU after your experiment:

```bash
sudo ip link set dev <iface> mtu 1500
```

If you can’t change MTU here, treat this as a design exercise and write down what you *would* do on a dedicated lab cluster.

---

### 3) Capture a pragmatic conclusion

In `network_tuning_bench.md`, add a “MTU / Jumbo Frames” section:

- Is jumbo MTU 9000 **end-to-end viable** in your environment?  
- For a vLLM SLM endpoint with relatively small request/response bodies, do you expect jumbo frames to materially impact latency?  
- In which scenarios would you argue for/against enabling jumbo frames (e.g., cross-rack bulk transfers vs small chat payloads)?

Try to keep this grounded in **your actual observations**, not just folklore.

---

### Expected Artifact

- Updated `network_tuning_bench.md` with an MTU / jumbo-frames section and a clear “should I care here?” answer.

