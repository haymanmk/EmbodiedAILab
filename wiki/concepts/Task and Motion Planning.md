---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["TAMP", "task-motion planning", "integrated task and motion planning"]
tags: [robotics, planning, motion-planning, manipulation, neuro-symbolic-ai]
---

# Task and Motion Planning

## Bridges from

- **Planning errands with parking constraints.** "Buy groceries, pick up medicine, then visit a friend" is the task plan. But each stop also needs physical feasibility: roads exist, parking is available, the store is open, and your car can fit. If the pharmacy parking lot is blocked, the high-level order may need to change. [[Task and Motion Planning]] has the same two-level flavor: symbolic task choices plus continuous geometric feasibility.

  *Where the analogy breaks down:* robot motion feasibility is not just route availability. It includes joint limits, kinematic reachability, collision checking, contact stability, dynamics, uncertainty, and sometimes force closure.

## Definition

Task and Motion Planning is the robotics problem of jointly deciding *what discrete actions to take* and *which continuous motions/poses make those actions physically feasible*. A task planner reasons over objects, symbolic actions, preconditions, and goals; a motion planner reasons over robot configuration, trajectories, collisions, constraints, and dynamics.

In [[Integrated Learning and Planning - Mao]], TAMP is the background shape behind many examples: the robot does not only learn a policy, it searches over action skeletons such as `pick -> place -> adjust -> insert` and fills in continuous parameters such as grasps, contacts, trajectories, and object poses.

## Origins / sources

- Classical robotics supplies configuration spaces, kinematics, collision checking, and motion planning; see [[Configuration Space]] and the current Modern Robotics foundation thread.
- [[Integrated Learning and Planning - Mao]] shows learning-based variants where neural modules propose or score contacts, poses, trajectories, effects, or high-level task skeletons that a planner then composes.
- The PDSketch and mechanism-learning papers downloaded with the seminar are local references for integrating learned models into planning domains.

## Variations / debates

- **Classical TAMP** usually assumes symbolic predicates and geometric models are hand-coded.
- **Learning-augmented TAMP** uses learned samplers, learned transition/effect models, learned heuristics, or LLM/VLM-generated domain structure.
- **End-to-end policy learning** avoids explicit planning, but often pays in data requirements and limited compositional generalization.
- A major tradeoff is where to put abstraction boundaries: too symbolic and the system is brittle/manual; too neural and it becomes opaque and data-hungry.

## Related concepts

- [[Configuration Space]]
- [[Constraint Satisfaction]]
- [[Neuro-Symbolic Concepts]]
- [[Composable Robot Skills]]
- [[Robot Learning]]
- [[Vision-Language-Action Models]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
- [[Jiayuan Mao]]
