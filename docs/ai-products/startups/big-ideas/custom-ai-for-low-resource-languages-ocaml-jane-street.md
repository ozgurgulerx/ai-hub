# Big Idea: Custom AI for Low-Resource Languages (Jane Street / OCaml)

Sources: none provided in prompt  
Status: **Speculative / Unverified**

- **Idea**: Organizations with niche stacks (e.g., low-resource languages like OCaml) will build custom, end-to-end AI systems (data → evals → tooling) because general-purpose models underperform when the language/tooling is underrepresented in training data.
- **Why now**: Frontier models help, but data sparsity for niche languages persists; building internal training + evaluation pipelines can close the gap.
- **What changes**: AI development becomes a workflow-specific discipline: continuous data capture from developer work, compilation/test-based evaluation, and tight IDE integration.
- **What has to be true**:
  - You can capture enough high-signal, permissioned code/workflow data (e.g., diffs, red→green transitions).
  - You can run meaningful evals at scale (compile/test) to drive iteration.
  - Tooling integration is modular so models/strategies can evolve without reworking editors.
- **Failure modes**:
  - Privacy/security/legal constraints prevent data capture.
  - Eval drift or narrow evals overfit and fail to generalize to real workflows.
  - Operational cost (build farm, storage, labeling) outweighs productivity gains.
- **Signals to watch**:
  - “Workspace snapshotting” as a standard internal data source.
  - Pre-warmed build/test evaluation services for codegen at scale.
  - Sidecar IDE tools that allow model/prompt/strategy swaps without editor plugins per model.
- **Startups**:
  - (Potential category: “niche-stack coding copilots” or “enterprise codegen infra for private languages/stacks”.)
- **References**:
  - None provided in prompt. (Add talk/article link when available.)

## Raw Notes (Preserved)

- Jane Street develops custom AI models for OCaml due to lack of pre-trained models from data scarcity.
- Training data via workspace snapshotting every ~20 seconds (build status + diffs between red/green states).
- Code evaluation service applies generated code to pre-warmed builds; checks compilation/tests over months.
- Sidecar app “Aid” integrates models with editors (VS Code, Neovim, Emacs) allowing model/strategy swaps without editor modifications.
- End-to-end loop: collect quality training data → build meaningful evals → ship workflow-fit tools.
