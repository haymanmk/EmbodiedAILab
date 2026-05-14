---
type: source
domain: research
created: 2026-05-14
updated: 2026-05-14
source_url: https://arxiv.org/abs/2304.13705
source_path: raw/act-paper-arxiv-snapshot.md
author: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn
published: 2023-04-23
tags: [robotics, imitation-learning, act, aloha, bimanual-manipulation]
---

# Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al

## Summary

Zhao et al. introduce ALOHA, a low-cost bimanual teleoperation system, and ACT, an imitation-learning algorithm for fine-grained manipulation. The central algorithmic idea is to predict short sequences of future actions rather than one next action at a time, reducing the effective horizon of high-frequency manipulation tasks. ACT combines action chunking, temporal ensembling, transformers, and a conditional VAE to learn from human demonstrations that may be noisy, multimodal, or non-stationary. The paper reports strong real-world performance on delicate bimanual tasks such as slotting a battery and opening a condiment cup from about 50 demonstrations. For this vault, the paper is the primary source for [[Action Chunking Transformer]] and an important bridge between [[Imitation Learning]] and practical low-cost robot hardware.

## Key claims

- Fine-grained bimanual manipulation is difficult because millimeter-scale errors, contact dynamics, and visual feedback matter.
- Standard behavioral cloning suffers from compounding errors when high-frequency robot actions push the system outside the demonstration distribution.
- [[Action Chunking Transformer|Action chunking]] predicts a sequence of future target joint positions, shortening the effective horizon of the task.
- Temporal ensembling smooths execution by averaging overlapping action predictions for the same future timestep.
- Training ACT as a conditional VAE helps model variability in human demonstrations.
- The paper reports that ACT learns six real-world fine-manipulation tasks with roughly 80-90% success using about 10 minutes or 50 trajectories of demonstration data.

## Notable quotes

- "Millimeters of error would lead to task failure." (Introduction)
- "This reduces the effective horizon of the task" (Introduction)
- "The CVAE encoder only serves to train the CVAE decoder (the policy) and is discarded at test time." (Action Chunking with Transformers)

## Connections

- [[Action Chunking Transformer]]
- [[Imitation Learning]]
- [[Robot Learning]]
- [[Robotics Development Stack]]
- [[LeRobot]]
- [[LeRobot Documentation Index]]

## Open questions

- How sensitive is ACT performance to camera placement, calibration quality, and teleoperation skill on low-cost arms other than ALOHA?
- When should a LeRobot user prefer temporal ensembling over simpler action queues?
- How does ACT compare with diffusion policies on the same small-data, fine-manipulation tasks?
