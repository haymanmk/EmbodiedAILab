---
type: concept
domain: research
created: 2026-05-14
updated: 2026-05-14
aliases: ["ACT", "Action Chunking with Transformers", "action chunking"]
tags: [robotics, imitation-learning, transformers, lerobot, act]
---

# Action Chunking Transformer

## Definition

Action Chunking Transformer, usually abbreviated ACT, is an [[Imitation Learning]] policy that maps robot observations to a short sequence of future actions instead of only predicting the next immediate action. In robotics terms, it is a behavioral-cloning-style policy with a stronger temporal action representation: given images and robot state now, it predicts an action chunk for the next `k` control steps.

ACT was introduced in [[Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al]] for fine-grained bimanual manipulation on low-cost hardware. [[LeRobot Documentation Index]] recommends it as the first policy to study in LeRobot because it trains relatively quickly, is computationally modest, and gives a practical baseline before moving to larger [[Vision-Language-Action Models]].

## Core idea

Standard behavioral cloning asks: "what action should I take right now?"

ACT asks: "given what I see right now, what short motion should I execute next?"

That distinction matters because many robot tasks are high-frequency. If a task takes 800 control steps and the policy must make a fresh single-step decision at every step, small mistakes can accumulate. If the policy predicts 100 steps at a time, the decision horizon is shorter and the model can represent a coherent motion segment such as reaching, grasping, inserting, or prying.

## Architecture

ACT has four important pieces:

- Visual encoder: usually a ResNet backbone that turns one or more RGB camera views into image features.
- Transformer encoder-decoder: combines image features, proprioceptive state, and a latent variable, then decodes a sequence of future actions.
- Conditional VAE training: learns a latent "style" variable from demonstration action sequences so the model can handle variability in human demonstrations.
- Temporal ensembling: during rollout, overlapping predicted chunks can be averaged for the same future timestep to produce smoother actions.

In the original ALOHA setup, observations used multiple RGB cameras plus robot joint positions, and actions were target joint positions. LeRobot's ACT implementation generalizes this into its policy interface, with defaults such as a ResNet-18 image backbone, `chunk_size` 100, VAE enabled, and optional temporal ensembling.

## Why it helps

ACT addresses two common imitation-learning problems:

- Compounding error: a tiny wrong action can move the robot into states absent from the demonstrations. Chunking reduces the number of independent high-level policy decisions over an episode.
- Human demonstration variability: two good demonstrations may solve the same state with different micro-trajectories. The CVAE objective lets ACT model a distribution over action sequences rather than forcing one deterministic average during training.

Temporal ensembling is not just ordinary smoothing across adjacent executed actions. It averages multiple predictions for the same timestep that came from different overlapping chunks. This preserves the idea that each averaged value is a prediction for the same target time.

## When to use it

Use ACT first when:

- the task is a narrow manipulation skill with a clear start and end;
- you can collect dozens of reasonably consistent demonstrations;
- actions are continuous robot controls such as joint positions or end-effector commands;
- the task benefits from smooth short-horizon motion;
- you want a strong baseline before trying diffusion policies or VLAs.

Do not expect ACT to solve broad open-ended instruction following by itself. It is usually task-specific and demonstration-driven. For language-conditioned generalization, compare it with [[Vision-Language-Action Models]], but keep ACT as the baseline that tells you whether the data, cameras, robot interface, and evaluation loop are working.

## LeRobot workflow

In LeRobot, the loop is:

1. Record demonstrations into a LeRobot dataset.
2. Train with `--policy.type=act`.
3. Evaluate by rolling out the trained policy on the robot or simulator.
4. Inspect failures, collect more targeted demonstrations or corrections, and retrain.

The practical lesson is that ACT is less about "a transformer magic trick" and more about making behavioral cloning fit the temporal structure of robot control.

## Related concepts

- [[Imitation Learning]]
- [[Robot Learning]]
- [[Vision-Language-Action Models]]
- [[Robotics Development Stack]]

## Mentions

- [[Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al]]
- [[LeRobot]]
- [[LeRobot Documentation Index]]
- [[Modern Robotics Development - synthesis]]

## External sources

- LeRobot ACT docs: https://huggingface.co/docs/lerobot/act
- ACT/ALOHA paper: https://arxiv.org/abs/2304.13705
- ALOHA project page: https://tonyzhaozh.github.io/aloha/
- LeRobot ACT implementation: https://github.com/huggingface/lerobot/tree/main/src/lerobot/policies/act
