---
type: concept
domain: research
created: 2026-05-13
updated: 2026-05-13
aliases: ["learning-based robotics", "data-driven robotics"]
tags: [robotics, machine-learning, robot-learning]
---

# Robot Learning

## Definition

Robot learning is the use of machine learning to map robot observations, task context, and sometimes language instructions into robot actions. In modern practice, it often shifts the hard part of robotics from hand-designing every control rule toward collecting useful data, training policies, and evaluating whether they survive contact with real-world variation.

## Origins / sources

- Classical robotics starts from geometry, kinematics, dynamics, planning, and control. This remains necessary because robots are physical machines.
- Modern robot learning adds data-driven policy learning through reinforcement learning, imitation learning, diffusion policies, transformer policies, and [[Vision-Language-Action Models]].
- The Hugging Face tutorial paper frames the modern trend as a transition from classical model-based methods toward data-driven methods enabled by large-scale robotics data and machine learning.

## Variations / debates

- Reinforcement learning learns by reward and trial-and-error, but real-world robots make sample efficiency and safety hard.
- [[Imitation Learning]] learns from demonstrations, which is practical for amateurs and labs with teleoperation hardware, but the learned policy can fail outside the demonstrated distribution.
- Generalist policies and VLA models promise cross-task and cross-robot transfer, but they require more data, compute, careful embodiment alignment, and serious evaluation.
- Open-source stacks lower the barrier, but robot learning is still constrained by hardware reliability, calibration, safety, dataset quality, and deployment latency.

## Related concepts

- [[Imitation Learning]]
- [[Vision-Language-Action Models]]
- [[Robotics Development Stack]]

## Mentions

- [[LeRobot]]
- [[LeRobot Documentation Index]]
- [[Modern Robotics Development - synthesis]]

## External sources

- Robot Learning tutorial paper: https://arxiv.org/abs/2510.12403
- LeRobot paper: https://arxiv.org/abs/2602.22818
- Open X-Embodiment paper: https://arxiv.org/abs/2310.08864
