# Tool Abuse

Attacks that exploit agent tool access for malicious purposes.

## Attack Vectors

- **Prompt injection → tool execution**: Injected prompts trigger dangerous tool calls
- **Overprivileged tools**: Tools with excessive permissions
- **Tool output manipulation**: Malicious data returned by tools influences agent behavior
- **Chained tool attacks**: Combine multiple tools to achieve malicious goals

## Examples

- File system access → data exfiltration
- Code execution → arbitrary command injection
- API access → unauthorized actions
- Database access → data theft or corruption

## Mitigations

- Least privilege for tools
- Tool allowlists and denylists
- Human-in-the-loop for high-risk actions
- Input/output validation
- Sandboxing and isolation
- Audit logging
