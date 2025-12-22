# MCP mental model + minimal example

This note captures a practical “how it fits together” view of MCP and a tiny, end-to-end example you can adapt.

## What MCP standardizes

- **Discovery**: a client can ask a server what it offers (tools/resources/prompts).
- **Invocation**: a client can call a tool with structured arguments and receive a structured result.
- **Resource access**: a client can read context from the server without baking the data-source specifics into the host.

## The moving parts

- **Host**: runs the model + orchestrator (e.g., IDE, desktop app, agent runtime).
- **Client**: the host’s MCP “adapter” that manages the connection to a server.
- **Server**: exposes capabilities and safely bridges to systems like files, DBs, or APIs.

## Message shapes (JSON-RPC 2.0)

- Request → response by matching `id`.
- Notifications have no `id` (no response expected).

## Transport choices

- **stdio**: simplest local integration; client starts the server process.
- **streamable HTTP**: better for remote/multi-client use; typically POST + optional SSE for streaming.

## Minimal server sketch (Python, stdio)

This is deliberately small: one server exposing a couple of physics-related tools.

```py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Physics-Server")

@mcp.tool()
def kinetic_energy(mass_kg: float, velocity_m_s: float) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be > 0")
    return 0.5 * mass_kg * (velocity_m_s ** 2)

@mcp.tool()
def gravitational_potential_energy(mass_kg: float, height_m: float, g_m_s2: float = 9.81) -> float:
    if mass_kg <= 0:
        raise ValueError("mass_kg must be > 0")
    if height_m < 0:
        raise ValueError("height_m must be >= 0")
    if g_m_s2 <= 0:
        raise ValueError("g_m_s2 must be > 0")
    return mass_kg * g_m_s2 * height_m

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Minimal client sketch (conceptual)

Your host/framework typically:

1. Starts/connects to the server (stdio or HTTP).
2. Discovers available tools (so it can decide what to call).
3. Calls tools as needed, passing arguments and receiving results.

Pseudo-flow:

```text
connect(server)
tools = list_tools()
result = call_tool("kinetic_energy", {"mass_kg": 800, "velocity_m_s": 25})
```

## Design takeaways worth keeping

- Keep servers **small and focused** (one integration boundary per server, when possible).
- Treat tools as an **API surface**: stable names, explicit schemas, good errors.
- Put auth/rate limits/auditing in the **server boundary**, not in prompt glue.
- Prefer **idempotent** tools where you can, and design for retries/timeouts.

