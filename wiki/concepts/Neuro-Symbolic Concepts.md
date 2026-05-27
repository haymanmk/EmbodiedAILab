---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["neurosymbolic concepts", "neuro-symbolic AI for robotics", "concept-centric robot agents"]
tags: [neuro-symbolic-ai, robot-learning, planning, representation]
---

# Neuro-Symbolic Concepts

## Bridges from

- **Recipe cards and kitchen skills.** A recipe does not store every muscle movement for cooking. It names reusable concepts such as "slice", "stir", "put the plate left of the fork", and "serve". A person still needs perception and motor skill to execute those steps, but the named structure lets them plan, substitute ingredients, and reuse knowledge. [[Neuro-Symbolic Concepts]] use the same split: symbolic names and composition rules on top; learned neural grounding underneath.

  *Where the analogy breaks down:* a recipe assumes a human can already ground words in rich physical experience. A robot must learn or implement grounding explicitly: visual recognition, contact geometry, motion generation, force control, collision checking, and timing.

## Definition

A neuro-symbolic concept is a reusable unit of robot knowledge with a symbolic interface and a neural or algorithmic implementation. The symbolic side gives the concept a name, type signature, arguments, and sometimes preconditions/effects; the neural side grounds it in perception, geometry, language, dynamics, or motor control.

In [[Integrated Learning and Planning - Mao]], examples include object properties such as color or shape, spatial relations such as `left-of(a,b)`, action concepts such as `pick(object, hand)`, and skill concepts such as `hang(mug, mug_tree)`. The point is not to replace neural networks with old-style logic. The point is to make the neural pieces composable, inspectable, and usable by [[Task and Motion Planning|planners]].

## Origins / sources

- [[Integrated Learning and Planning - Mao]] presents neuro-symbolic concepts as the unifying idea behind one-shot manipulation, functional object arrangement, long-horizon skill composition, and closed-loop robot-agent systems.
- The local paper `raw/assets/papers/2025-arxiv-neuro-symbolic-concepts.pdf` is the conceptual umbrella reference downloaded with the seminar.
- PDSketch, MAGIC, SetItUp, STACK, and Retriever instantiate different parts of the same program: learned concept grounding plus explicit composition.

## Variations / debates

- **Symbol-first systems** encode predicates, actions, and constraints manually, then learn only low-level parameters. They are interpretable but need expert engineering.
- **Neural-first systems** train a policy or VLA model end-to-end. They can absorb messy sensory data but are harder to debug, verify, and recombine.
- **Neuro-symbolic systems** try to get the useful part of both: neural grounding for perception/physics, symbolic structure for planning/composition. The engineering risk is that the interface between the two can become brittle or expensive to design.
- In the foundation-model era, [[Integrated Learning and Planning - Mao]] argues that symbolic structure still matters because foundation models can help propose structure but do not eliminate the need for grounding, checking, timing, and planning.

## Worked example

For a table-setting task, the symbolic level might propose:

```text
left_of(fork, plate)
right_of(knife, plate)
near(cup, plate)
reachable(left_arm, fork_pose)
collision_free(trajectory)
```

The neural level grounds these constraints: a VLM detects objects, an LLM proposes commonsense relations, a diffusion model generates likely poses, and a motion planner checks reachability and collisions. The robot does not merely "predict the next action"; it solves for a configuration and sequence that jointly satisfy the relevant concepts.

## Related concepts

- [[Task and Motion Planning]]
- [[Constraint Satisfaction]]
- [[Contact Analogy]]
- [[Compositional Diffusion Constraint Solvers]]
- [[Composable Robot Skills]]
- [[Closed-Loop Robot Agents]]
- [[Vision-Language-Action Models]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
- [[Jiayuan Mao]]
