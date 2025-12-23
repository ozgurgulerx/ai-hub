# RL Environments

Simulation environments for training and evaluating reinforcement learning agents.

## Classic Control & Games

| Environment | Description |
|-------------|-------------|
| **OpenAI Gym / Gymnasium** | Standard API for RL environments (CartPole, MountainCar, Atari, MuJoCo) |
| **Atari (ALE)** | Arcade games; pixel-based observations, discrete actions |
| **MuJoCo** | Physics simulation for continuous control (HalfCheetah, Ant, Humanoid) |

## Robotics & Embodied AI

| Environment | Description |
|-------------|-------------|
| **Isaac Gym / Isaac Lab** | NVIDIA GPU-accelerated physics for massively parallel robot training |
| **MuJoCo Menagerie** | Collection of robot models (arms, hands, quadrupeds) |
| **PyBullet** | Open-source physics engine, robotics benchmarks |
| **RoboSuite** | Manipulation tasks with Sawyer/Panda arms |

## Multi-Agent & Strategy

| Environment | Description |
|-------------|-------------|
| **PettingZoo** | Multi-agent extension of Gymnasium API |
| **Melting Pot** | Social dilemmas, cooperation/competition |
| **StarCraft II (PySC2)** | Complex strategy, partial observability |
| **Hanabi** | Cooperative card game, theory of mind |

## LLM & Language Agents

| Environment | Description |
|-------------|-------------|
| **WebArena / VisualWebArena** | Web browsing tasks for language agents |
| **SWE-Bench** | Software engineering tasks (code editing, bug fixing) |
| **InterCode** | Interactive coding environments |
| **AgentBench** | Multi-domain agent evaluation |

## Procedural & Open-Ended

| Environment | Description |
|-------------|-------------|
| **Procgen** | Procedurally generated games for generalization |
| **NetHack (NLE)** | Roguelike with extreme complexity |
| **Minecraft (MineRL)** | Open-ended, hierarchical tasks |
| **Crafter** | Lightweight Minecraft-like for research |

## Key Considerations

- **Sim-to-real gap**: physics fidelity, domain randomization
- **Reward shaping**: sparse vs dense, intrinsic motivation
- **Parallelization**: vectorized envs, GPU-accelerated simulation
- **Reproducibility**: seeding, determinism
