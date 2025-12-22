# Supply-Chain Planner Copilot with Long-Term Memory

Demos pairing Agent Framework ChatAgent with Mem0 long-term memory backed by Azure AI Search.

![Memory Architecture](assets/memory-architecture.png)

## Architecture

- **Agent Framework ChatAgent** + **Azure OpenAI** (Responses API)
- **Mem0 Memory** with **Azure AI Search** vector store + **Azure OpenAI embeddings**
- **Custom ContextProvider** — searches Mem0 before each turn, stores summaries after

## Scripts

| Script | Description |
|--------|-------------|
| `20_agent_framework_mem0_memory policy.py` | Scripted 3-scene demo: no memory → write playbook → recall across sessions |
| `21_chat_ui_mem0_agent.py` | Interactive chat UI with basic episodic memory |
| `22_intent_aware_mem0_agent.py` | **Intent-aware** memory with category filtering |

---

## 22: Intent-Aware Memory Agent

The intent-aware agent detects whether you're asking about **OPTIMIZATION** (capacity, scheduling) or **FORECASTING** (demand, trends), then retrieves/stores memories filtered by that category.

![Intent-Aware Flow](assets/intent-aware-flow.png)

### How It Works

1. **Intent Detection** — LLM classifies each message using conversation history (short-term memory)
2. **Filtered Retrieval** — Searches Mem0 using intent-specific `user_id` segmentation (`user-optimization`, `user-forecasting`)
3. **Tagged Storage** — New memories stored with category metadata for future filtering

```
User Message → Intent Detector → OPTIMIZATION | FORECASTING | GENERAL
                                      ↓
                          Mem0 Search (filtered by intent)
                                      ↓
                          Context-Specific Memories → ChatAgent → Response
```

### Demo Flow

![Demo Example](assets/demo-example.png)

```bash
python 22_intent_aware_mem0_agent.py
```

**Example session:**
```
# Store optimization knowledge
you> For SKU 123 capacity issues at Plant A, our playbook is to shift 10% to Plant B.
[intent] Detected: OPTIMIZATION
[mem0] Stored as 'optimization'

# Store forecasting knowledge  
/new
you> Q4 demand shows 25% spike in November for Black Friday.
[intent] Detected: FORECASTING
[mem0] Stored as 'forecasting'

# Later: ask about optimization → retrieves only optimization memories
/new
you> Plant A is at 95% capacity. What should we do?
[intent] Detected: OPTIMIZATION
[mem0] Retrieved 1 optimization memories
```

---

## Prerequisites

- Python 3.10+
- Azure OpenAI: chat deployment + embedding deployment
- Azure AI Search service
- Packages: `agent-framework`, `mem0`, `azure-search-documents`, `python-dotenv`

## Setup

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `config_example.env` to `.env` and fill in Azure values

## Run

```bash
# Scripted demo
python 20_agent_framework_mem0_memory\ policy.py

# Interactive chat
python 21_chat_ui_mem0_agent.py

# Intent-aware (recommended)
python 22_intent_aware_mem0_agent.py
```
