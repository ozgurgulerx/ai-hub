# 100 Days of Inference Engineering

> **Dec 1, 2025 → Mar 10, 2026** | 3-4 hrs/day focused effort

**[📋 Full Roadmap & Checklist →](learning_goals.md)**

---

Throughout this 100-day journey I’m also using **NotebookLM** and **OpenAI DeepResearch** extensively—to synthesize reading, design experiments, and pressure-test my own explanations as I go.

## The 100-Day Plan

| Phase | Days | Dates | Focus |
|-------|------|-------|-------|
| **0** | 1-15 | Dec 1-15 | OS & GPU Setup |
| **1** | 16-35 | Dec 16 → Jan 4 | vLLM Mastery |
| **2** | 36-55 | Jan 5-24 | Quantization |
| **3** | 56-80 | Jan 25 → Feb 18 | Optimization |
| **4** | 81-100 | Feb 19 → Mar 10 | Ship & Share |

---

## Daily Logs

| Day | Date | Topic | Status |
|-----|------|-------|--------|
| [001](day-001-initial-setup/) | Dec 1 | Initial Setup | ✅ |
| [002](day-002-GPU-node-bring-up/) | Dec 2 | GPU Node Bring-Up | 🔄 |
| [003](day-003-vLLM-capacity-and-OOM/) | Dec 3 | vLLM Capacity & OOM | ⏳ |
| [004](day-004-quantization-vs-bf16/) | Dec 4 | Quantization vs BF16 | ⏳ |
| [005](day-005-OS-and-NUMA-node-hardening/) | Dec 5 | OS & NUMA Node Hardening | ⏳ |
| [006](day-006-slm-memory/) | Dec 6–7 | SLM + OS Memory & vLLM | ⏳ |
| [007](day-007-vllm-runtime-probes/) | Dec 8 | vLLM SLM: TTFT, Prefix Caching, KV Scaling | ⏳ |
| [008](day-008-storage-and-page-cache/) | Dec 9 | Storage, Page Cache & Cold Starts | ⏳ |
| [009](day-009-storage-nvme-vs-network/) | Dec 10 | Storage Paths: NVMe vs Network & Staging | ⏳ |
| [010](day-010-network-latency-and-endpoint/) | Dec 11 | Network Path & vLLM HTTP Latency | ⏳ |
| [011](day-011-network-tuning-and-irq/) | Dec 12 | Network Tuning: MTU, IRQ Affinity & Backlog | ⏳ |
| [012](day-012-vllm-in-docker/) | Dec 13 | vLLM in Docker (GPU Containerization) | ⏳ |
| ... | | | |

---

## Deliverables Tracker

| Deliverable | Target Day | Status |
|-------------|------------|--------|
| Bootstrap script | 3 | ⏳ |
| Grafana dashboard | 15 | ⏳ |
| HF vs vLLM comparison repo | 18 | ⏳ |
| Load test script | 30 | ⏳ |
| Quantization benchmark | 40 | ⏳ |
| Case study #1 | 72 | ⏳ |
| Case study #2 | 80 | ⏳ |
| Optimization playbook | 95 | ⏳ |
| Blog post published | 100 | ⏳ |

---

## Links

- [📋 Learning Goals](learning_goals.md) – Full 100-day checklist
- [🤖 Daily Coach Prompt](learning_prompt.md) – AI prompt for generating daily plans
- [📚 Inference Engineering Book](../books/inference-engineering/README.md)
