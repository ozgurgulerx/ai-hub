# What Matters for Better GraphRAG (Graph Types, Operators, Cost, Retrieval Performance)

GraphRAG results are often inconsistent because “GraphRAG” is not one method—it’s a design space across:

- **Graph types** (trees, passage graphs, knowledge graphs, textual KGs, richer KGs)
- **Operators** (indexing, traversal/ranking, subgraph selection, community detection, aggregation)
- **Budgets** (token usage, latency, build-time vs query-time compute)
- **Data shape** (corpus size, chunking density, entity/relation ambiguity)
- **Question type** (specific fact lookup vs abstract synthesis)

This note distills a recurring theme from data-driven comparisons across many GraphRAG papers/implementations: **operators and budgets matter at least as much as graph schema richness**.

## 1) Richer graphs are not automatically better

Adding more node/edge attributes, longer descriptions, or complex schemas can:

- help abstract reasoning and synthesis *if* the extra semantics are clean and discriminative
- hurt retrieval *if* it introduces noise, over-merging, predicate bloat, or larger search spaces

Practical takeaway: treat “graph richness” as a hypothesis that must earn its keep in evals.

## 2) Operators often matter more than graph type

Across many systems, the performance lift typically comes from **how you retrieve**:

- **Node operators**: dense/sparse indexing, candidate generation, hybrid retrieval
- **Link-based operators**: one-hop expansion, constrained traversal, **Personalized PageRank (PPR)**-style ranking
- **Subgraph operators**: k-hop neighborhoods, path/subgraph extraction (including Steiner-style variants)
- **Community operators**: clustering, community summaries, topic routing

The same underlying graph can behave very differently depending on the operator mix.

## 3) Cost vs accuracy has a real Pareto frontier

Some GraphRAG variants deliver small accuracy gains at very high cost (tokens/latency), and some are simply dominated.

Practical process:

- Measure **token usage per query** (retrieval + reasoning + summarization) and **latency per query**
- Plot against your target metric (accuracy/hit rate/citation correctness)
- Prefer methods on the **Pareto frontier** (no other method is both cheaper and better)

## 4) Dataset scale and structure change the game

GraphRAG often shines on **mid-sized corpora** where graph construction remains tractable and structure stays meaningful.
At very large scales, you can run into:

- dense, less discriminative graphs (too many “similar” nodes/edges)
- community blow-ups
- multi-hop chains getting lost among distractors

Mitigations to consider:

- stronger entity/edge resolution + pruning
- graph partitioning / per-domain graphs
- query-time caps (hop limits, top-k limits, budgeted expansion)

## 5) Specific vs abstract QA require different retrieval stacks

- **Specific QA** (fact lookup): tends to reward strong candidate generation + lightweight expansions.
- **Abstract QA** (cross-doc synthesis): tends to reward relationship-rich structure + community operations + summary routing.

Practical takeaway: don’t ship a single fixed GraphRAG pipeline; use **routing** (query type, budget, corpus scale) to select:

- graph type (tree vs KG vs passage graph)
- operator mix (PPR vs community summaries vs path extraction)
- hop depth and expansion budget

## 6) A minimal “adaptive GraphRAG” template

- **Step 0**: instrument budgets (tokens/latency) and retrieval outcomes (hit rate, evidence quality).
- **Step 1**: classify query (specific vs abstract; multi-hop likelihood).
- **Step 2**: pick a retrieval plan (operators + limits) based on query + corpus scale.
- **Step 3**: retrieve structured context (triples/subgraphs) *and* linked grounding text.
- **Step 4**: generate with citations and run regression evals.

## Related notes in this repo

- KG evaluation (retention vs utility): `kg-evaluation-mine.md`
- Graph basics + pitfalls (overview): `../README.md` (GraphRAG section)

## References (TODO)

- Add links to the underlying paper list/survey and to key methods once pinned.
