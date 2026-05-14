---
title: ACT (Action Chunking with Transformers)
source_url: https://huggingface.co/docs/lerobot/act
source_repo: https://github.com/huggingface/lerobot
saved: 2026-05-14
---

# ACT (Action Chunking with Transformers) - LeRobot docs snapshot

Local research snapshot for the EmbodiedAILab vault.

## Main LeRobot framing

- LeRobot describes ACT as a lightweight and efficient policy for imitation learning.
- It is recommended as the first model to try when starting with LeRobot because of fast training, low compute requirements, and strong performance.
- The docs connect ACT to the paper "Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware" by Zhao et al.

## Architecture summary

- Vision backbone: ResNet-18 processes images from multiple camera views.
- Transformer encoder: combines camera features, joint positions, and a learned latent variable.
- Transformer decoder: generates coherent action sequences through cross-attention.
- Inputs: multiple RGB images, current robot joint positions, and a latent style variable.
- Output: a chunk of future actions.

## Practical defaults and training notes

- ACT is included in the base LeRobot installation.
- Training uses the standard `lerobot-train` pipeline with `--policy.type=act`.
- The docs suggest starting with default hyperparameters.
- The docs describe a typical expectation of a few hours for 100k training steps on a single GPU.
- A starting batch size of 8 is recommended, adjusted for GPU memory.

## Code-level notes from LeRobot configuration

- Default `chunk_size`: 100 environment steps.
- Default `n_action_steps`: 100 environment steps.
- Default vision backbone: `resnet18`.
- Default transformer hidden size: 512.
- Default attention heads: 8.
- Default encoder layers: 4.
- Default decoder layers: 1 in LeRobot, matching behavior of the original implementation.
- VAE is enabled by default, with latent dimension 32 and KL weight 10.0.
- Temporal ensembling is optional in LeRobot and requires querying the policy every step.

## Commands from docs

```bash
lerobot-train \
  --dataset.repo_id=${HF_USER}/your_dataset \
  --policy.type=act \
  --output_dir=outputs/train/act_your_dataset \
  --job_name=act_your_dataset \
  --policy.device=cuda \
  --wandb.enable=true \
  --policy.repo_id=${HF_USER}/act_policy
```

```bash
lerobot-record \
  --robot.type=so100_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.id=my_robot \
  --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}}" \
  --display_data=true \
  --dataset.repo_id=${HF_USER}/eval_act_your_dataset \
  --dataset.num_episodes=10 \
  --dataset.single_task="Your task description" \
  --dataset.streaming_encoding=true \
  --dataset.encoder_threads=2 \
  --policy.path=${HF_USER}/act_policy
```
