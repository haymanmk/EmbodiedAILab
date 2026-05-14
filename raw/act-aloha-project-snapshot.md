---
title: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware project page
source_url: https://tonyzhaozh.github.io/aloha/
paper_url: https://arxiv.org/abs/2304.13705
saved: 2026-05-14
---

# ALOHA project page snapshot

Local research snapshot for the EmbodiedAILab vault.

## Project framing

- The project introduces ALOHA, a low-cost open-source bimanual teleoperation system.
- The project page states that ALOHA was built around a budget of about $20k.
- The system is designed for precise, contact-rich, and dynamic manipulation tasks.
- It pairs the hardware system with ACT, the Action Chunking with Transformers learning algorithm.

## Learning algorithm notes

- ACT predicts an action chunk instead of a single next action.
- The ACT policy is trained as the decoder of a conditional VAE.
- The policy combines images from multiple viewpoints, joint positions, and a style variable with a transformer encoder, then predicts a sequence of actions with a transformer decoder.
- At test time the CVAE encoder is removed and the latent style variable is set to zero.

## Demonstration notes

- The project page describes real-time rollouts trained from 50 demonstrations per task.
- The original ACT setup predicts joint positions at 50 Hz with a fixed chunk size of 90.
- The page reports strong success rates on four highlighted tasks and includes videos for reactivity and robustness.

## Observation setup

- Evaluation observations include four RGB cameras at 480x640 resolution.
- Two cameras are static and two are mounted on robot wrists.

## Saved links

- Paper: https://arxiv.org/abs/2304.13705
- Project page: https://tonyzhaozh.github.io/aloha/
- ACT + simulation codebase: https://github.com/tonyzhaozh/act
