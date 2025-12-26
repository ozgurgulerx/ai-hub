# GenAI Attacks (Overview)

Agents expand the trust boundary from “model safety” to **agent-system security**: untrusted inputs can influence tool calls, memory, data access, and cross-system side effects.

## Attack Types (Quick Taxonomy)

| Attack type | What it is | Why it matters |
|------------|------------|----------------|
| **Prompt injection (direct + indirect)** | Direct: attacker writes malicious instructions into the prompt. Indirect: malicious instructions ride along inside retrieved docs/web pages/tool outputs and get treated as instructions. | The attacker can hijack the agent’s objectives, tool selection, and data access without “breaking” the model. |
| **Jailbreaks** | Techniques to bypass model safety policies and content filters. | Can unlock disallowed behaviors that then cascade into tool misuse or unsafe outputs. |
| **Tool abuse** | Abuse of an agent’s tool interface (function calls, browser, code execution, file access) to take unintended actions. | Turns prompt-level attacks into real-world side effects (exfiltration, corruption, fraud). |
| **Tool sprawl / permissioning** | Over-provisioned tool surfaces (too many tools, too-broad scopes, weak authz boundaries), and inconsistent permission checks across tools. | Increases the attack surface and makes it easy for the agent to “do the wrong thing” with legitimate access. Treat tool scopes like production IAM. |
| **Memory manipulation** | Poisoning or steering what an agent stores/retrieves as “memory” (persistent notes, long-term profiles, scratchpads, tool-derived state). | Creates long-lived compromise: the agent may repeatedly act on attacker-planted beliefs/preferences across sessions. |
| **Data exfiltration** | Coaxing the system to leak secrets/PII via outputs or via tools (email/HTTP/etc.). | The most common real-world impact: credentials, customer data, internal docs leak. |
| **Data poisoning (training/RAG)** | Injecting malicious/biased data into training sets or retrieval corpora so the model behaves incorrectly when triggered. | Produces backdoors, targeted misbehavior, or systematic bias—often hard to detect. |
| **Model extraction** | Stealing model behavior/weights via repeated queries or distillation-style attacks. | IP loss and easier downstream attacks (adversarial examples, jailbreak tuning). |
| **Membership inference** | Determining if specific data was present in training. | Privacy exposure and regulatory risk (esp. for sensitive corpora). |
| **Multi-agent attacks** | Exploiting trust relationships between agents (impersonation, message injection, cross-agent privilege escalation). | Privilege boundaries become porous when agents can “ask favors” from more-privileged agents. |

## How to Use This Folder

- Start with `index.md` for the MkDocs taxonomy.
- Use the individual pages for deeper notes per attack class.
