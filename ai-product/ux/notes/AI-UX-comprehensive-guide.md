# AI UX: A Comprehensive Guide

Designing interfaces and flows that guide users and guard quality in AI-powered products.

---

## Core Principles

### Set Expectations

Users need to understand what AI can and cannot do:
- **Examples** — Show what good inputs/outputs look like
- **Limitations** — Be explicit about what the system doesn't handle well
- **Guidance** — Help users formulate effective requests

### Make Quality Visible

Build trust through transparency:
- **Citations** — Show sources for generated content
- **Controls** — Let users adjust behavior (tone, length, detail)
- **Feedback** — Make it easy to signal good/bad outputs

### Handle Failures Gracefully

AI will fail. Design for it:
- **Helpful recovery** — Guide users when things go wrong
- **Graceful degradation** — Partial results are often better than nothing
- **Clear escalation** — When to involve humans

---

## Pattern Cards

### Pattern: Abstain Behavior

**When to use:** When the model should decline to answer rather than guess.

**Architecture:**
```
Query → Confidence check → If low: "I don't have enough information to answer this"
                        → If high: Generate answer with citations
```

**Pitfalls:**
- Over-abstaining frustrates users
- Under-abstaining erodes trust

**Checklist:**
- [ ] Define confidence thresholds
- [ ] Design abstain message with next steps
- [ ] Track abstain rate as a metric

---

### Pattern: Progressive Disclosure

**When to use:** Complex AI capabilities that overwhelm new users.

**Architecture:**
```
Simple interface → User gains proficiency → Unlock advanced features
```

**Pitfalls:**
- Hiding critical features too deeply
- Assuming all users want "simple"

**Checklist:**
- [ ] Identify core vs advanced features
- [ ] Design unlock triggers (usage, explicit request)
- [ ] Provide shortcuts for power users

---

### Pattern: Confidence Indicators

**When to use:** When users need to calibrate trust in AI outputs.

**Architecture:**
```
Output → Confidence score → Visual indicator (color, badge, language)
```

**Examples:**
- "I'm confident about this" vs "This might not be accurate"
- Green/yellow/red indicators
- "Based on 15 sources" vs "Limited information available"

**Pitfalls:**
- Overconfident indicators → users stop checking
- Too many warnings → users ignore all

**Checklist:**
- [ ] Calibrate confidence to actual accuracy
- [ ] A/B test indicator designs
- [ ] Track user behavior with/without indicators

---

### Pattern: Inline Corrections

**When to use:** When users should be able to fix AI mistakes easily.

**Architecture:**
```
Output → User correction → Update model/memory → Improved future outputs
```

**Pitfalls:**
- Corrections not persisting
- No feedback that correction was received

**Checklist:**
- [ ] Design inline edit affordances
- [ ] Confirm corrections were saved
- [ ] Use corrections to improve evals

---

## Semi-Autonomous Agent UX

For agents that take actions on behalf of users:

### Capability Discovery

Itemize what the agent can reliably do. Don't oversell.

### Proactive Suggestions

Parse user context to suggest next steps. Balance helpfulness with intrusiveness.

### Observability

Stream activity logs to UI so users can see what's happening.

### Interruptibility

Pause/resume functionality. Users need to feel in control.

### Cost-Aware Delegation

Estimate action costs before execution. Delegate expensive operations to users with clear tradeoffs.

---

## Voice UI Considerations

Voice interfaces have unique requirements:

| Concern | Solution |
|---------|----------|
| **Interruptibility** | Handle mid-sentence interruptions gracefully |
| **Cadence** | Tune for natural speech rhythm |
| **Numbers/names** | Special handling for pronunciation |
| **Personality** | Match voice properties to brand |

---

## Feedback Collection

### Implicit Signals

- Time spent on output
- Copy/paste behavior
- Follow-up questions
- Task completion

### Explicit Signals

- Thumbs up/down
- Star ratings
- Free-text feedback
- Correction submissions

### Feedback Loop

```
User feedback → Eval dataset → Model/prompt improvement → Better outputs
```

---

## Design Checklist

### Before Launch

- [ ] Clear capability communication
- [ ] Abstain behavior for low-confidence cases
- [ ] Citation/source display
- [ ] Feedback mechanisms
- [ ] Error states designed

### Post-Launch

- [ ] Monitor user corrections
- [ ] Track confidence calibration
- [ ] A/B test UX variations
- [ ] Feed insights back to eval team

---

## Summary

AI UX succeeds when it:

1. **Sets realistic expectations** — Users know what to expect
2. **Makes quality visible** — Trust through transparency
3. **Handles failures gracefully** — Recovery, not frustration
4. **Keeps users in control** — Especially for autonomous agents
5. **Closes the feedback loop** — User signals improve the system
