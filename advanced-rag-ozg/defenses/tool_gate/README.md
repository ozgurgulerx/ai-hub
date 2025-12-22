# Tool Gate

Goal: enforce a **hard boundary** between model text and tool execution.

Pattern:

1) Model proposes a tool call  
2) Policy engine evaluates `(tool_name, tool_args, user_context)`  
3) Execute or deny + log decision

Policy lives in `defenses/tool_gate/policy.json`.

