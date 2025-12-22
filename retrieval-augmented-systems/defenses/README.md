# Defenses

Day001 defenses are intentionally small and testable:

- `tool_gate/`: explicit authorization for tool calls (deny by default)
- `retrieval_firewall/`: strip instruction-like content from retrieved documents before prompt injection

Run the harness to see the delta: `python3 eval/harness/run_attack_pack.py --compare`.

