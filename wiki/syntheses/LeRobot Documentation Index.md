---
type: synthesis
domain: research
created: 2026-05-13
updated: 2026-05-13
aliases: ["LeRobot docs index", "LeRobot study index"]
tags: [robotics, lerobot, documentation, study-plan]
---

# LeRobot Documentation Index

## Thesis

Yes: the LeRobot documentation should have a local wiki index. The docs are broad enough that future searching will be much easier if the vault keeps a conceptual map: what each docs section is for, when to read it, and how it connects to [[Robot Learning]], [[Imitation Learning]], [[Vision-Language-Action Models]], and the broader [[Robotics Development Stack]].

Snapshot checked: 2026-05-13. Official docs: https://huggingface.co/docs/lerobot/index

## How to read the docs

1. Start with "LeRobot" and "Installation" to understand the project scope and environment.
2. Read "Imitation Learning for Robots" before policy pages, because it explains the core record-train-evaluate loop.
3. Read "Using LeRobotDataset" early; dataset shape is the backbone of the whole stack.
4. Use "ACT" as the first policy page unless there is a specific reason to start with a VLA.
5. Read "Bring Your Own Hardware" only after the basic loop is clear.
6. Read simulation, benchmark, and VLA pages when you want to compare methods or avoid buying hardware too early.

## Official docs map

| Docs area | What it is for | Study priority |
|---|---|---|
| Get started | Project overview and installation | First |
| Tutorials | End-to-end workflows: imitation learning, custom policies, custom hardware, RL, simulation RL, multi-GPU, human-in-the-loop data, PEFT, camera edge cases | First to second |
| Datasets | LeRobotDataset, large dataset porting, dataset tools, subtasks, video streaming | First |
| Policies | ACT, SmolVLA, Pi0, Pi0-FAST, Pi0.5, GR00T N1.5, X-VLA, Multitask DiT, WALL-OSS | Second |
| Reward models | SARM and reward-learning-related tools | Later |
| Inference | Policy deployment, async inference, real-time chunking | Second, before real robot rollout |
| Simulation | Environments from Hub and LeIsaac | Second, useful before hardware |
| Benchmarks | LIBERO, Meta-World, IsaacLab arenas, RoboTwin, RoboCasa, RoboCerebra, RoboMME, VLABench | Later, for evaluation literacy |
| Robot processors | Observation/action processing, debugging processor pipelines, custom processors | Later, but important for custom robots |
| Robots | Supported hardware pages such as SO-101, SO-100, Koch, LeKiwi, Reachy 2, Unitree G1, Earth Rover Mini, OMX, OpenArm | Read when selecting hardware |
| Teleoperators | Phone and supported teleoperation devices | Read before data collection |
| Sensors | Cameras and sensor setup | Read before recording |
| Supported hardware | PyTorch accelerators and hardware support notes | Read before buying compute |
| Resources | Notebooks, firmware, motor/CAN notes | Use as needed |
| About | Contribution and compatibility notes | Later |

## Key pages to bookmark

- Docs home: https://huggingface.co/docs/lerobot/index
- Installation: https://huggingface.co/docs/lerobot/main/installation
- Imitation learning tutorial: https://huggingface.co/docs/lerobot/main/il_robots
- LeRobotDataset v3.0: https://huggingface.co/docs/lerobot/lerobot-dataset-v3
- Bring your own hardware: https://huggingface.co/docs/lerobot/main/integrate_hardware
- ACT policy: https://huggingface.co/docs/lerobot/act
- SmolVLA policy/blog: https://huggingface.co/blog/smolvla
- Policy deployment: https://huggingface.co/docs/lerobot/main/inference
- LeRobot GitHub: https://github.com/huggingface/lerobot
- Robot Learning tutorial paper: https://arxiv.org/abs/2510.12403
- LeRobot library paper: https://arxiv.org/abs/2602.22818

## Reading path for this vault

Phase 1 - Foundations:

- [[Robotics Development Stack]]
- [[Robot Learning]]
- [[Imitation Learning]]
- LeRobot installation and imitation-learning tutorial

Phase 2 - First project:

- LeRobotDataset
- ACT policy
- One supported robot or one simulation environment
- Policy deployment and evaluation

Phase 3 - Generalization:

- [[Vision-Language-Action Models]]
- SmolVLA, Pi0, Pi0-FAST, Pi0.5
- Open X-Embodiment and Octo
- Benchmarks such as LIBERO and Meta-World

## Open questions

- Which hardware path is most realistic: SO-101/SO-100, OpenArm, a mobile robot, or simulation-only first?
- What is the first task: pick-and-place, drawer opening, shirt folding, mobile navigation, or pure simulation benchmark?
- What compute is available locally, and is cloud GPU acceptable?
- Should this vault later ingest the full tutorial paper as a proper source page with detailed chapter notes?

## Last revised

2026-05-13 - Created as the initial local search index for LeRobot study.
