---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["contact analogies", "functional contact transfer", "MAGIC"]
tags: [robotics, manipulation, contact, one-shot-learning, neuro-symbolic-ai]
---

# Contact Analogy

## Bridges from

- **Using a different hook to hang a bag.** If you learn that a curved coat hanger can catch a loop, you do not memorize the exact pixels of that hanger. You notice the functional contact: curved part goes through loop, gravity pulls down, object stays supported. Later, a differently shaped hook can work if it has an analogous contact region. [[Contact Analogy]] gives the robot that style of transfer.

  *Where the analogy breaks down:* humans bring rich tactile and physical priors. A robot must estimate surfaces, normals, friction, collision risk, grasp reachability, and stability from noisy perception and models.

## Definition

Contact analogy is a strategy for one-shot manipulation transfer: identify the functionally important contact points or contact mode sequence in a demonstration, find analogous contacts on a new object, and verify the resulting motion with planning and physics checks.

In [[Integrated Learning and Planning - Mao]], the hanging example transfers from placing a hanger onto a rack to placing a mug onto a mug tree. The robot uses pretrained visual features such as DINOv2 to propose corresponding functional regions, but the proposal is noisy, so motion planning, grasp analysis, and stability checks filter the candidates.

## Origins / sources

- [[Integrated Learning and Planning - Mao]] presents contact analogy as the first concrete example of learning from very little data while retaining physical checks.
- The local paper `raw/assets/papers/2025-icra-magic-one-shot-manipulation-contact-analogies.pdf` is the downloaded MAGIC reference.
- The local paper `raw/assets/papers/2023-corl-learning-reusable-manipulation-strategies.pdf` is the related mechanism-learning reference, where contact-mode sequences scaffold reusable manipulation strategies.

## Variations / debates

- Contact analogy is stronger than raw imitation because it tries to preserve *why* the demonstration worked: the contact structure.
- It is weaker than a fully general physics learner because it still relies on planners, simulators, geometric reconstruction, and object rigidity assumptions.
- Failure modes include wrong visual correspondences, noisy point clouds, missing geometry, bad friction assumptions, and physically feasible plans that fail on the real robot.

## Related concepts

- [[Task and Motion Planning]]
- [[Constraint Satisfaction]]
- [[Composable Robot Skills]]
- [[Robot Learning]]
- [[Imitation Learning]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
