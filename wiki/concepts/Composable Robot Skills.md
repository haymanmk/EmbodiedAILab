---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["skill composition", "composable skills", "learned skill composition", "STACK"]
tags: [robot-learning, imitation-learning, manipulation, planning, foundation-models]
---

# Composable Robot Skills

## Bridges from

- **Building with reusable dance steps.** A long dance is not learned as one unbroken muscle command. It is built from shorter steps that can be practiced, named, reordered, and adapted to the floor. Robot skill composition does something similar: learn short grounded skills, predict their effects, and plan how to chain them.

  *Where the analogy breaks down:* robot skills interact with object geometry and physics. A "step" may fail because a book collides with a shelf, a mug blocks another mug, or a gripper cannot reach the pose. Skill composition therefore needs effect prediction and feasibility checking, not just sequencing.

## Definition

Composable robot skills are learned short-horizon action models that can be recombined by a planner to solve longer tasks. A composable skill usually needs four pieces: when it applies, what arguments it takes, how to generate candidate motion or action trajectories, and how it changes the world.

In [[Integrated Learning and Planning - Mao]], the STACK-style examples learn skill samplers and effect models from a small number of demonstrations. At test time, the system proposes a task skeleton, samples candidate trajectories for each skill, predicts the geometric effects, checks feasibility, and searches over possible sequences.

## Origins / sources

- [[Integrated Learning and Planning - Mao]] presents composable skills as the long-horizon extension of the earlier contact and spatial-relation examples.
- The local paper `raw/assets/papers/2026-icra-stack-learning-composable-skills.pdf` is the downloaded STACK reference.
- The local paper `raw/assets/papers/2023-corl-learning-reusable-manipulation-strategies.pdf` is a related reference for mechanism-level composition through contact-mode sequences.

## Variations / debates

- **Manual skills** are written by an engineer, then composed by a planner. They are reliable but slow to scale.
- **Learned skills** come from demonstrations and can adapt to data, but need effect models and checks to avoid compounding errors.
- **Foundation-model-discovered skills** use VLMs to segment demonstrations and identify relevant entities, reducing manual annotation but depending on model reliability.
- The important distinction from standard [[Imitation Learning]] is that composable skills are not only trained to imitate; they are represented so a planner can search over their combinations.

## Related concepts

- [[Imitation Learning]]
- [[Task and Motion Planning]]
- [[Contact Analogy]]
- [[Neuro-Symbolic Concepts]]
- [[Vision-Language-Action Models]]
- [[Closed-Loop Robot Agents]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
