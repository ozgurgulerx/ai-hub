# Big Updates to Redis: Context Engine, Tools, and Memory — Notes

Summary for: https://youtu.be/qlJg-TJFEnI  
Generated from summary tooling (Noiz): https://noiz.io  
Status: **To verify**

## Unified Context Architecture (As Described)

- Redis Context Engine is described as unifying structured data, unstructured data, and memory into a schema-driven, MCP-native layer.
- It’s described as enabling agents to blend semantic search with structured filters, traverse relationships, call APIs, and maintain state via a single interface. [Unverified]

## Hybrid Query Capability (Claim)

- Redis vector database is described as supporting hybrid queries that combine geo index + vector index + text search, with benchmark claims of being the fastest vector database for retrieving relevant unstructured context for agents. [Unverified]

## Structured Data Integration Challenge

- Structured data (Postgres/Oracle) is framed as the most valuable enterprise data yet largely untouched by agents, representing major opportunity. [Unverified]
- Text-to-SQL and naive REST→MCP mapping are framed as inadequate, with risks: incorrect SQL, security vulnerabilities, and performance/auth issues for complex APIs. [Unverified]

## Semantic Schema Approach

- Writing a semantic graph describing the business model is described as enabling mapping of semantic + retrieval components and enforcing granular access control. [Unverified]
- A unified context engine is framed as enabling dynamic traversal across structured/unstructured/memory beyond one-shot RAG. [Unverified]

## Related (In This Repo)

- MCP security notes: `../../ai-security-and-governance/docs/mcp-security/README.md`
- Ontologies and semantic governance: `../../ai-security-and-governance/docs/ai-governance/ontology-epistemology-owl-shacl.md`

