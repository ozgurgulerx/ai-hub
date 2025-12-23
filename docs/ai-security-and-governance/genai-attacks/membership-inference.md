# Membership Inference

Attacks that determine whether specific data was used to train a model.

## How It Works

- Query model with known data points
- Analyze confidence scores or output distributions
- Higher confidence often indicates training data membership

## Privacy Risks

- Reveal sensitive training data
- Violate data protection regulations (GDPR, CCPA)
- Expose proprietary datasets

## Mitigations

- Differential privacy during training
- Output calibration
- Limit confidence score precision
- Regularization techniques
- Training data audits
