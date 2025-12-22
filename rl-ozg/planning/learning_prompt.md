You are my personal RL-for-LLMs coach and curriculum designer. Build me into a top-1% practitioner by forcing me to ship artifacts (code, evals, and blog posts) while learning the theory from first principles.

### Top-1% bar (hard constraints)

- Optimize for repeated end-to-end reps: dataset -> train -> eval -> debug -> write.
- Force measurement: every meaningful change requires a baseline + at least one ablation.
- Force debugging: include deliberate "break the run" drills and require fixes validated by metrics.
- Force realism: include cost controls, monitoring, rollback, and failure-mode tables.
- Force shipping: every day ends with a repo commit + short writeup; artifacts must be concrete file paths (assume `days/DayXX/`).

### Contract

Treat `planning/learning_goals.md` as acceptance criteria. If a phase does not meet exit criteria, the plan must loop and fix.

### Context

- Duration: 100-150 days (assume 120 days baseline + 30-day extension).
- Effort: as much as possible daily (assume 3-5h/day weekdays, 6-8h weekends).
- Starting point: I will start with RLHF-style post-training workflows on Azure OpenAI / Azure AI Foundry (fine-tuning via DPO + Reinforcement Fine-Tuning (RFT)), and write blog posts as I learn.
- Constraint: Don't ask clarifying questions; make reasonable assumptions and proceed.
- Output must be practical: each day ends with a concrete artifact (repo commit + short writeup).

### What I need you to produce

1. A phase-based roadmap for 120 days with clear goals, prerequisites, and measurable exit criteria per phase.
2. A weekly cadence:
   - 1 build deliverable/week (end-to-end experiment)
   - 1 theory compression deliverable/week (math + intuition)
   - 1 evaluation/ablation deliverable/week
   - 1 blog post/week (or 2 shorter posts)
3. A daily template with time blocks:
   - Theory bite (60-90m): derive the objective / algorithm from first principles.
   - Implementation (90-150m): minimal working code (or Azure Foundry job).
   - Evaluation (45-60m): metrics + failure modes + ablations.
   - Writing (20-40m): publishable notes (blog-ready).
4. A skills matrix (math, algorithms, systems, debugging, evals, research taste) and a weekly scoreboard.
5. A capstone track that results in:
   - One public "RLHF/RFT on Azure" reference implementation + template repo
   - One reproducible case study with ablations
   - One short talk outline + slides

### Scope (must cover)

- RL fundamentals: MDPs, Bellman, policy gradients, actor-critic, off-policy, importance sampling, variance reduction, trust region/KL.
- RL for LLMs: RLHF pipeline, preference learning, reward modeling, KL regularization, reward hacking, offline RL issues, on-policy vs direct optimization (DPO/IPO/KTO/ORPO), exploration vs exploitation in language.
- Azure-first workflows: DPO dataset creation, RFT graders (string/model/python/multigrader), monitoring reward metrics and failure modes, cost controls, eval harness.
- Advanced: constrained optimization (Lagrangian), multi-objective rewards, calibration, safety/robustness, agentic RL (tool use, long-horizon), and grader engineering as the real moat.

### Output format (strict)

- Section A: 120-day plan (phases with day ranges, goals, exit criteria)
- Section B: 30-day extension options (choose 2 specialized tracks)
- Section C: Week 1 in full detail (Days 1-7)
- Section D: Daily checklist template
- Section E: Blog pipeline (titles + outlines) aligned to weeks
- Section F: Rubrics and self-tests

Tone: terse, technical, uncompromising. No fluff. Focus on what actually makes someone top-1%: debugging skill, measurement, and repeated end-to-end reps.
