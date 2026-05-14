---
type: entity
domain: research
created: 2026-05-13
updated: 2026-05-13
aliases: ["Hugging Face LeRobot", "lerobot"]
tags: [robotics, robot-learning, open-source, hugging-face]
---

# LeRobot

## Overview

LeRobot is Hugging Face's open-source PyTorch library for real-world [[Robot Learning]]. Its role is to make the learning loop easier to reproduce: connect or integrate robot hardware, record teleoperated demonstrations, store them in a standard dataset format, train policies, evaluate them, and deploy policies back onto real robots.

LeRobot is best understood as a robot-learning stack, not as a full replacement for [[Robotics Development Stack|robot middleware]], simulation, mechanical design, or safety engineering. It complements tools such as ROS 2, MoveIt, Gazebo, Isaac Sim, PyTorch, and the Hugging Face Hub.

## Key facts

- Official docs describe LeRobot as providing models, datasets, and tools for real-world robotics in PyTorch, with a focus on imitation learning and reinforcement learning.
- The project includes robot interfaces, teleoperation workflows, dataset tools, training scripts, policy implementations, benchmarks, simulation integration, and deployment tooling.
- Current docs emphasize accessible hardware such as SO-100/SO-101, Koch, LeKiwi, Reachy 2, Unitree G1, OpenArm, and other supported platforms.
- The LeRobot paper frames the project as a response to fragmented robotics tooling across motor control, data collection, dataset storage, model training, and inference.
- LeRobot's most useful entry path for a self-researcher is usually: install LeRobot, use a supported robot or simulation, collect a small dataset, train ACT or fine-tune a compact VLA policy, then iterate.

## Mentions

- [[LeRobot Documentation Index]]
- [[Modern Robotics Development - synthesis]]
- [[Robot Learning]]
- [[Vision-Language-Action Models]]

## Related

- [[Robotics Development Stack]]
- [[Imitation Learning]]
- [[Robot Learning]]
- [[Vision-Language-Action Models]]

## External sources

- Hugging Face LeRobot docs: https://huggingface.co/docs/lerobot/index
- LeRobot GitHub repository: https://github.com/huggingface/lerobot
- LeRobot paper: https://arxiv.org/abs/2602.22818
- Robot Learning tutorial paper: https://arxiv.org/abs/2510.12403
