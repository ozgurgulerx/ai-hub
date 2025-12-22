# Getting Started

Congrats for your first step into learning agent-framework. 
This section includes easy to run samples from Azure Documentation.

### Async-First API (Agent Framework vs. Semantic Kernel)

Agent Framework’s Python API is **async-first**: methods like `agent.run()` return **coroutines**. In contrast, classic Semantic Kernel patterns leaned on synchronous `Invoke`/chat-completions wrapped in a Kernel.

#### Why async by default helps
- **Non-blocking I/O:** keep notebooks, UIs, and servers responsive during model calls.  
- **Native streaming:** surface tokens/events as they arrive for real-time UX.  
- **Easy concurrency:** fan-out multiple tools/agents in parallel, then fan-in results.  
- **Clean integration:** plays nicely with existing event loops (web frameworks, UIs, **Jupyter’s** top-level `await`).  

**Result:** lower perceived latency, higher throughput under load, and sturdier multi-agent orchestration—plus you can display progress (traces/updates) **while** work continues.


