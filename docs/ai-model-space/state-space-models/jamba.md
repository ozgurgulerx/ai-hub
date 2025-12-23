# Jamba

Jamba is a **hybrid** architecture that combines transformer **attention** with Mamba-style **SSM** layers (often described as “attention + Mamba blocks”).

## What it is

- Interleaves attention layers (global interactions) with SSM layers (efficient long-sequence processing).
- Aims to reduce overall compute/memory on long contexts while keeping attention where it matters.

## When it’s useful

- You want transformer-like behavior but need better long-context efficiency
- You need a practical hybrid for tasks that benefit from some global attention

## Major vendor

- **AI21 Labs** is the primary vendor associated with the Jamba model family.

