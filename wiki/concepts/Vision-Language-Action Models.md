---
type: concept
domain: research
created: 2026-05-13
updated: 2026-05-27
aliases: ["VLA", "robot foundation models", "vision-language-action policies"]
tags: [robotics, vla, foundation-models, multimodal-ai]
---

# Vision-Language-Action Models

## Definition

Vision-language-action models are robot policies that condition on visual observations and language instructions, then output actions for a robot. They extend the vision-language model idea into physical control: the model must not only understand a scene and task, but also produce actions at the right timing, scale, and embodiment.

## Origins / sources

- Open X-Embodiment showed the value of aggregating many robots and tasks into standardized robot-learning data, with RT-X models demonstrating cross-robot transfer.
- Octo is an open-source generalist robot policy trained on Open X-Embodiment data and designed for fine-tuning to new robots and tasks.
- Pi0 and SmolVLA are representative modern VLA-style systems that connect visual-language understanding with action generation.
- LeRobot includes docs and implementation paths for policies such as ACT, SmolVLA, Pi0, Pi0-FAST, Pi0.5, X-VLA, GR00T N1.5, and WALL-OSS.
- [[Integrated Learning and Planning - Mao]] treats VLMs, LLMs, and VLA policies as components inside larger structured robot systems: models can propose spatial relations, task skeletons, segmentations, or action chunks, but planning, constraints, memory, and control still need explicit system structure.

## Variations / debates

- VLA policies can be more general than task-specific policies, but they are harder to debug because failures can come from perception, language grounding, action representation, timing, dataset mismatch, or hardware calibration.
- Fine-tuning an existing VLA is plausible for a self-researcher. Training a generalist VLA from scratch is usually not plausible without large datasets, GPUs, engineering time, and safety infrastructure.
- For many first projects, [[Action Chunking Transformer|ACT]] or another small imitation-learning policy is a better learning vehicle than a large VLA.
- A key open design question is whether a VLA should be the whole policy or a module inside a [[Closed-Loop Robot Agents|closed-loop agent]] with explicit planning, monitoring, memory, and control.

## Related concepts

- [[Robot Learning]]
- [[Imitation Learning]]
- [[Action Chunking Transformer]]
- [[Closed-Loop Robot Agents]]
- [[Neuro-Symbolic Concepts]]
- [[Robotics Development Stack]]

## Mentions

- [[LeRobot]]
- [[LeRobot Documentation Index]]
- [[Modern Robotics Development - synthesis]]
- [[Integrated Learning and Planning - Mao]]

## External sources

- Open X-Embodiment: https://arxiv.org/abs/2310.08864
- Octo: https://arxiv.org/abs/2405.12213
- SmolVLA blog: https://huggingface.co/blog/smolvla
- Pi0 blog: https://www.pi.website/blog/pi0
