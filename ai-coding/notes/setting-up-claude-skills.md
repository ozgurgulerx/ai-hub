# Setting up Claude Skills (quick checklist)

These steps reflect the common “Skills” flow in Claude’s UI. Labels/paths may change over time.

## 1) Enable Skills

- Open Claude **Settings** → **Capabilities** → **Skills**
- Ensure Skills are enabled.

## 2) Enable the “skill-creator” meta-skill

- In **Settings** → **Capabilities** → **Skills**, find **skill-creator**
- Toggle it on.

## 3) Create a new skill (in chat)

- Start a new chat
- Ask Claude to use **skill-creator** to help you create a new skill
- Describe the skill precisely:
  - Inputs (what you provide)
  - Outputs (exact format, examples)
  - Constraints (do/don’t, edge cases, failure behavior)
  - Any templates (report layout, file format, naming)

Claude may ask clarifying questions; answer them until it produces a complete skill bundle.

## 4) Review and download the generated files

- Read the generated README/instructions carefully
- Download the produced skill file/bundle

## 5) Upload the skill to Claude

- Go back to **Settings** → **Capabilities** → **Skills** → **Upload**
- Select the downloaded skill file/bundle and upload it
- Ensure the skill is toggled on (so it’s active)

## 6) Test and iterate

- In a new chat, ask Claude to use the skill **by name**
- If you need changes:
  - update the skill in the original “skill-creator” conversation
  - upload the new version
  - disable the old version to avoid confusion

## Safety / hygiene

- Don’t embed secrets or tokens in the skill.
- Keep the skill scope narrow; add capabilities only when you can test them.
- Add “stop/ask for confirmation” rules for destructive actions (deletes, emails, payments, etc.).

