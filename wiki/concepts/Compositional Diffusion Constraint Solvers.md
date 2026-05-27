---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["diffusion constraint solvers", "diffusion-based constraint solver", "diffusion CCSP", "SetItUp"]
tags: [diffusion-models, constraint-satisfaction, robot-learning, spatial-reasoning, planning]
---

# Compositional Diffusion Constraint Solvers

## Bridges from

- **Magnets nudging objects into place.** Imagine each spatial rule creates a gentle invisible pull: "fork left of plate" pulls the fork leftward, "cup near plate" pulls the cup closer, and "do not overlap" pushes objects apart. If all pulls are combined, the table arrangement settles into a pose that satisfies the rules. A compositional diffusion constraint solver uses learned gradient-like signals in a similar way.

  *Where the analogy breaks down:* the learned gradients are not real forces and do not guarantee global optimality. They are model outputs used inside iterative optimization or sampling, and they still need collision, reachability, and task checks.

## Definition

A compositional diffusion constraint solver uses diffusion-style generative models to represent reusable constraints, then combines those constraints to solve a larger arrangement or planning problem. Instead of generating a single whole scene directly, the system learns separate relation models such as `left_of(a,b)`, `near_edge(a)`, or `aligned(a,b)` and composes their gradient fields or scores during inference.

In [[Integrated Learning and Planning - Mao]], this appears in the SetItUp table-arrangement example: an LLM or VLM proposes an abstract spatial relationship graph, and diffusion models ground the relations into continuous object poses that jointly satisfy the graph.

## Origins / sources

- [[Integrated Learning and Planning - Mao]] introduces this as the second major example after contact analogy.
- The local paper `raw/assets/papers/2024-rss-set-it-up-functional-object-arrangement-compositional-generative-models.pdf` is the downloaded SetItUp reference.
- The local paper `raw/assets/papers/2025-arxiv-neuro-symbolic-concepts.pdf` situates diffusion constraint solvers as one instantiation of neuro-symbolic concept grounding.

## Variations / debates

- Diffusion models are useful here because many object arrangements are valid; the model should represent a distribution or field of plausible solutions, not one deterministic answer.
- The symbolic layer provides compositionality: relations can be added or removed without retraining a monolithic generator for every task.
- The learned solver may satisfy aesthetic or commonsense relations but still needs robot feasibility constraints for execution: workspace limits, arm reach, collision-free motion, and sequencing.

## Related concepts

- [[Constraint Satisfaction]]
- [[Neuro-Symbolic Concepts]]
- [[Task and Motion Planning]]
- [[Vision-Language-Action Models]]
- [[Robot Learning]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
