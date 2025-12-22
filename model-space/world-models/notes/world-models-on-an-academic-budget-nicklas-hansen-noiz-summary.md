# World Models on an Academic Budget (Nicklas Hansen) — Notes

Summary for: https://youtu.be/qDgDCUUxiKc  
Generated from transcript tooling (Noiz): https://noiz.io/tools/youtube-transcript  
Status: **To verify**

## World Models as Neural Simulators

- World models are framed as neural, simulatable worlds that enable reasoning about the physical world by predicting future states from past observations and actions for planning in embodied AI. [Unverified]
- Sampling different futures from identical initial conditions is framed as producing counterfactuals for planning by sampling trajectories and optimizing, similar to classical simulators. [Unverified]

## TD-MPC Planning (As Described)

- TD‑MPC planning is described as: encode the current observation into a latent representation, sample actions, predict future latent states, rewards, and value, then select the action that maximizes predicted return. [Unverified]

## Scaling and Accessibility

- TD‑MPC is described as scaling with data/model size, improving through interaction, training on a modest budget, and being openly available for academic research. [Unverified]
- TD‑MPC2 is described as outperforming TD‑MPC1 without requiring hyperparameter tuning and performing well across many tasks, improving approachability. [Unverified]
- Open sharing of 300+ checkpoints is described as enabling reuse without recomputation and accelerating RL research. [Unverified]
- TD‑MPC is described as applying across 100+ tasks in different simulators/domains (locomotion/manipulation) without domain knowledge. [Unverified]

## Training Strategies and Data Efficiency

- A 50/50 sampling pipeline mixing human demonstrations with RL interaction is described as improving robot policy performance by broadening state/action coverage. [Unverified]
- Learning a dense reward function from demonstrations by predicting task stages is described as speeding up RL interaction and improving manipulation benchmarks. [Unverified]
- Using human motion-capture data as a prior is described as helping humanoids learn natural motion in high-dimensional settings before downstream tasks. [Unverified]

## Online Learning and Real-World Application

- TD‑MPC is described as enabling online RL in unknown tasks: iteratively collect data, train on the growing dataset, and learn a working policy even with slow simulators on older GPUs. [Unverified]
- Combining demonstrations with online interaction is described as especially useful at small academic scale (few robots, limited demo collection). [Unverified]

## Architecture and Design Principles

- TD‑MPC2 design choices (planning, regularization, discrete reward regression) are described as enabling scaling and better performance than model-free policies in high-dimensional multi-task settings. [Unverified]
- A pre-trained tracking world model (humanoid-specific, general for tracking motion) is described as reusable as a starting point for downstream optimization. [Unverified]
- “Puppeteer” world models are described as task-specific models that use a pre-trained tracking model and online RL to optimize task rewards. [Unverified]

## Limitations and Future Directions

- Fine-tuning pre-trained multitask models on new tasks is described as improving performance but not being zero-shot; models trained on ~80 tasks are described as lacking generalization comparable to LLMs. [Unverified]
- Embodied AI is framed as becoming more accessible via cheaper hardware and policies (including large VLMs or smaller world models) solving problems with little data. [Unverified]

