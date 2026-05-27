---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["constraint satisfaction problem", "CSP", "constraint optimization"]
tags: [optimization, planning, robotics, constraints]
---

# Constraint Satisfaction

## Bridges from

- **Arranging furniture in a room.** A couch must fit through the door, face the TV, leave walking space, avoid blocking outlets, and look reasonable. Each rule removes some possible placements. A good arrangement is one that satisfies all important rules at once. In robotics, constraints play the same role for poses, trajectories, contacts, timing, and object relations.

  *Where the analogy breaks down:* furniture planning is usually slow and forgiving. Robot constraints can be continuous, high-dimensional, time-varying, noisy, and safety-critical; satisfying them may require numerical optimization or sampling-based search.

## Definition

Constraint satisfaction is the problem of finding variable values that satisfy a set of constraints. In robotics, variables may be object poses, robot configurations, trajectories, grasp points, contact points, task orders, or skill parameters. Constraints may encode geometry, dynamics, reachability, collision avoidance, object relations, preferences, and task goals.

In [[Integrated Learning and Planning - Mao]], a manipulation action can be represented as a constrained optimization problem: find trajectories and intermediate states that obey path constraints such as joint limits and collision avoidance while achieving subgoal constraints such as holding an object or placing it on a rack.

## Origins / sources

- [[Lagrange Multipliers]], [[Karush-Kuhn-Tucker Conditions]], and [[Constraint Gradients and Tangent Spaces]] cover the continuous-optimization side of constraints.
- [[Task and Motion Planning]] uses constraints to connect symbolic task choices to continuous robot feasibility.
- [[Compositional Diffusion Constraint Solvers]] use learned gradient fields to solve spatial arrangement constraints such as `left_of`, `near`, and `aligned`.

## Variations / debates

- **Hard constraints** must be satisfied, such as no collision or within joint limits.
- **Soft constraints** are preferences or costs, such as "books should be grouped together" or "use a short trajectory".
- **Analytic constraints** are hand-written, such as distance-to-obstacle $\ge 0$.
- **Learned constraints** are represented by a neural model, such as a diffusion model that scores whether an object pose satisfies a spatial relation.
- Constraint systems are interpretable, but the hard part is deciding which constraints matter and ensuring learned constraints do not hallucinate feasibility.

## Related concepts

- [[Lagrange Multipliers]]
- [[Karush-Kuhn-Tucker Conditions]]
- [[Constraint Gradients and Tangent Spaces]]
- [[Task and Motion Planning]]
- [[Compositional Diffusion Constraint Solvers]]
- [[Neuro-Symbolic Concepts]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
