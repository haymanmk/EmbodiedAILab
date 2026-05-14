---
title: Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware
source_url: https://arxiv.org/abs/2304.13705
html_url: https://ar5iv.labs.arxiv.org/html/2304.13705
project_url: https://tonyzhaozh.github.io/aloha/
authors: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn
saved: 2026-05-14
---

# Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware

Local research snapshot for the EmbodiedAILab vault.

## Bibliographic metadata

- arXiv: 2304.13705
- Submitted: 2023-04-23
- Authors: Tony Z. Zhao, Vikash Kumar, Sergey Levine, Chelsea Finn
- Venue shown on project page: RSS 2023
- Subject areas: Robotics; Machine Learning

## Abstract-level claims

- Fine manipulation tasks are hard because they require precision, contact handling, and closed-loop visual feedback.
- The work combines a low-cost bimanual teleoperation system, ALOHA, with an imitation-learning algorithm, Action Chunking with Transformers.
- ACT learns a generative model over action sequences rather than only a single next action.
- The paper reports that ACT learns six difficult real-world fine-manipulation tasks, including opening a condiment cup and slotting a battery, with roughly 80-90% success from about 10 minutes or 50 demonstration trajectories.

## ACT mechanism notes

- ACT predicts a future action sequence, or action chunk, conditioned on the current observation.
- The paper argues that action chunking reduces the effective task horizon and therefore mitigates compounding errors in behavioral cloning.
- Temporal ensembling queries the policy frequently and averages overlapping predictions for the same execution timestep, improving smoothness without extra training cost.
- ACT is trained as a conditional variational autoencoder. The encoder compresses the current robot state and demonstration action sequence into a latent style variable; at test time the encoder is discarded and the latent is set to zero.
- The policy uses camera images and joint positions as observations and outputs target joint positions.
- The implementation uses ResNet image encoders plus transformer encoder-decoder modules and L1 reconstruction loss.

## Experimental setup notes

- ALOHA uses low-cost leader and follower arms with joint-space teleoperation.
- The system uses four RGB cameras: two static views and two wrist-mounted cameras.
- Data recording and teleoperation run at 50 Hz in the original setup.
- The paper compares ACT against behavioral cloning and other imitation-learning baselines on simulated and real bimanual manipulation tasks.

## Why this matters for LeRobot study

ACT is a practical first policy to study because it sits between plain behavioral cloning and larger generalist robot policies. It keeps the supervised learning loop simple, but adds sequence prediction, temporal smoothing, and a latent variable to handle human demonstration variability.
