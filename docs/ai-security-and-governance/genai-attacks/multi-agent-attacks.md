# Multi-Agent Attacks

Attacks that exploit trust and coordination between multiple AI agents.

## Attack Types

### Cross-Agent Privilege Escalation
Agents with different privilege levels can be manipulated to escalate access. A lower-privilege agent tricks a higher-privilege agent into performing restricted actions.

**Example**: Agent A (read-only) convinces Agent B (write access) to modify data on its behalf.

**Reference**: [Cross-Agent Privilege Escalation: When Agents Free Each Other](https://embracethered.com/blog/posts/2025/cross-agent-privilege-escalation-agents-that-free-each-other/)

### Agent Impersonation
Malicious agent pretends to be a trusted agent to gain access or influence decisions.

### Message Injection
Inject malicious messages into agent-to-agent communication channels.

### Coordination Exploitation
Exploit consensus mechanisms or voting systems in multi-agent setups.

## Mitigations

- **Zero trust between agents**: Verify every request regardless of source
- **Privilege boundaries**: Agents cannot grant permissions they don't have
- **Message authentication**: Cryptographic signing of inter-agent messages
- **Action auditing**: Log all cross-agent requests and approvals
- **Least privilege**: Each agent has minimal required permissions
- **Human oversight**: High-risk cross-agent actions require approval
