# Google “Ironwood” TPU (Noiz summary notes)

Source video (YouTube): `https://www.youtube.com/watch?v=IiItHlD6-WI`

This note is distilled from a **Noiz** transcript summary provided in the prompt. The original summary is highly promotional; treat all specifics below as **claims to verify** until confirmed via primary sources (Google documentation/blogs, TPU architecture papers, or reputable reporting).

## Cloud-scale AI infrastructure (claims)

- “Ironwood TPU” is described as scaling from **256 to 9,016 chips per pod**.
- It is described as chaining **43 pods** into a **400,000-chip** cluster.
- The interconnect is described as a **3D torus fabric** plus **optical circuit switching**.
- The claim is that this outpaces NVIDIA’s “traditional rack architecture” for training frontier models at hyperscale.

## Ecosystem / market positioning (claims)

- Anthropic is described as committing to **one million TPUs** for Claude, framed as evidence that TPUs are now competitive enough (performance, reliability, economics) to support frontier training stacks.
- Google’s TPU program is framed as a “complete stack” (silicon + compiler ecosystem + fabric) that threatens NVIDIA’s dominance in training.

## Verification checklist (what to pin down)

- Whether “Ironwood” is an official TPU generation name, and its generation relative to public TPU v4/v5e/v5p/etc.
- The exact scaling numbers (pod sizes, max pod size) and whether the “400,000-chip cluster” claim is literal (vs total fleet capacity).
- Fabric details: what “3D torus” and “optical circuit switching” refer to in TPU networking, and how they are deployed.
- The Anthropic “one million TPUs” claim: scope (chips vs chip-hours), timeframe, and what workloads it covers.
- Comparative claims vs NVIDIA: which benchmarks, models, and cost/throughput metrics are being compared.

## Appendix: Raw Notes (Preserved)

- “Google's Ironwood TPU scales from 256 to 9,016 chips per pod and chains 43 pods into a 400,000-chip cluster using 3D torus fabric and optical circuit switching…”
- “Anthropic's commitment to one million TPUs for Claude…”
- “Google's decade-long TPU development combines competitive chip performance, mature compiler ecosystem, and scalable fabric…”
