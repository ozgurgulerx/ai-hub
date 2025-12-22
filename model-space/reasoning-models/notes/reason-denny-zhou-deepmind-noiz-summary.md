# Reason (Large Language Model Reasoning, Denny Zhou, Google DeepMind) — Notes

Summary for: https://youtu.be/-Srfmszcz2A  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-video-transcript  
Status: **To verify**

## Revealing vs. Adding Reasoning (Prompting)

- Reasoning is framed as being **revealed, not added**, by techniques like chain-of-thought prompting: prompting reshapes output probabilities to surface a step-by-step path that already exists in the model’s learned patterns. [Unverified]

## “Self-Teaching” via IO Fine-Tuning (As Described)

- IO fine-tuning (training on the model’s own correct answers) is claimed to outperform supervised fine-tuning because it trains on examples in the model’s “native” expression patterns rather than human-written explanations. [Unverified]
- Letting the model teach itself is framed as more effective than using human-generated reasoning data because the model learns from its own successful approaches. [Unverified]

## Consensus-Based Accuracy (Self-Consistency)

- Self-consistency (sample multiple answers and majority vote) is described as dramatically improving accuracy and providing a confidence signal.
- A specific claim: >80% agreement across samples correlates with near-100% final-answer accuracy. [Unverified]

## Current Limitations (Verification-Dependent)

- The hard case is framed as creative tasks without clear right answers where verification cannot definitively determine correctness, limiting self-improvement loops. [Unverified]
- Robust verification is framed as the crucial ingredient for effective reasoning/self-improvement during training and inference. [Unverified]

