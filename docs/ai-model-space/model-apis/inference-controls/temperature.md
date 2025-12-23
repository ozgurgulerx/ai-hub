# Temperature (Avoid < 1 for agents)

Please don’t do temperature < 1. It‘s not worth it, esp. if you‘re building an agent.

Reduces:

- function calling quality
- thought quality
- token efficiency
- error recovery in agents
- markdown consistency

… and it also does not give you more factual results.

If you need more predictability, design a good system instruction. Temp < 1 is a relic of Q&A apps.

Most $$M spend customers I have worked with: temp=0.1 -> temp=1 -> problem solved.

## Why

- most models are RL-trained at temp=1.0. At lower temperature you are modifying the model’s learned probability distribution during inference
- if you reduce temperature, you are restricting the probability space the model can explore. Frontier LLMs w/ thinking, function calling, or agent loops make full use of the flexibility to explore this space. Also for agentic error recovery, diversity in sampling is key.
- models are most likely to get stuck in thinking loops with low temperature, failing silently and/or increasing your token usage unnecessarily
- some function calling & markdown formatting (i.e. tables) require complicated nested structures with many tokens. Greedy sampling might mean that these structures are i.e. never properly closed, breaking esp. agents.
- most system prompts are not well written. Higher temperature allows to recover more easily from underspecification and subtle logical conflicts.

## Reference

- https://x.com/lkshaas/status/2001651793332236511?s=20
