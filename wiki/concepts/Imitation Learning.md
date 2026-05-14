---
type: concept
domain: research
created: 2026-05-13
updated: 2026-05-13
aliases: ["behavioral cloning", "BC", "learning from demonstrations"]
tags: [robotics, imitation-learning, behavioral-cloning]
---

# Imitation Learning

## Definition

Imitation learning trains a robot policy from demonstrations. In the common behavioral cloning setup, the model sees observations from a task and learns to predict the expert action that was taken.

For a self-researcher, imitation learning is usually the first practical robot-learning method because it replaces reward design with teleoperated examples: record yourself doing the task, train a policy, evaluate, collect more data around failures, and repeat.

## Origins / sources

- LeRobot's real-world tutorial centers on recording and visualizing a dataset, training a policy, and evaluating the result on a robot.
- ACT, short for Action Chunking with Transformers, is presented in the LeRobot docs as a beginner-friendly imitation-learning policy with fast training and relatively low compute needs.
- Human-in-the-loop workflows such as DAgger-style correction can improve a policy by recording interventions when the autonomous policy starts failing.

## Variations / debates

- Pure behavioral cloning is simple but can accumulate errors when the robot drifts into states absent from the demonstrations.
- Action chunking predicts a short sequence of future actions instead of a single next action, which can make behavior smoother and easier to deploy at control rate.
- Diffusion and VLA policies can handle richer multimodal action distributions but usually need more compute and more careful inference engineering.

## Related concepts

- [[Robot Learning]]
- [[Vision-Language-Action Models]]
- [[Robotics Development Stack]]

## Mentions

- [[LeRobot]]
- [[LeRobot Documentation Index]]
- [[Modern Robotics Development - synthesis]]

## External sources

- LeRobot imitation-learning docs: https://huggingface.co/docs/lerobot/main/il_robots
- LeRobot ACT docs: https://huggingface.co/docs/lerobot/act
- Robot Learning tutorial paper: https://arxiv.org/abs/2510.12403
