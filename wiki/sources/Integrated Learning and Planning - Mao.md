---
type: source
domain: research
created: 2026-05-27
updated: 2026-05-27
source_url: https://www.youtube.com/watch?v=3W36pd50Wqw
source_path: raw/stanford-robotics-seminar-integrated-learning-and-planning.md
source_format: video
author: Jiayuan Mao
published: 2026-05-20
chunks_indexed: false
indexed_at:
study_status: covered
tags: [robotics, neuro-symbolic-ai, planning, robot-learning, manipulation, foundation-models]
---

# Integrated Learning and Planning - Mao

## Summary

Jiayuan Mao's Stanford Robotics Seminar argues that general-purpose physical intelligence should not be framed only as fitting a giant observation-to-action function from robot data. The talk proposes a concept-centric alternative: represent robot behavior using compositional neuro-symbolic concepts for states, relations, actions, constraints, skills, and effects, then use learned neural modules to ground those concepts in perception, geometry, contact, language, and motion. The examples move from one-shot manipulation strategy transfer, to functional object arrangement with diffusion-based constraint solvers, to long-horizon manipulation where foundation models discover spatial/temporal structure and planners compose learned skills. For this vault, the talk is a bridge between [[Robot Learning]], [[Imitation Learning]], [[Vision-Language-Action Models]], and the user's active robotics-foundations thread: it shows why kinematics, contact, planning, and constraint reasoning still matter in the foundation-model era. The central practical message is that learned robot policies become more data-efficient and more debuggable when embedded in explicit structure rather than treated as one opaque policy.

## Key claims

- End-to-end policy learning can work for narrow tasks, but it tends to require large demonstration datasets and has weak human-like few-shot generalization to novel objects, goals, and compositions (per [[Integrated Learning and Planning - Mao]]).
- [[Neuro-Symbolic Concepts]] combine a symbolic interface — names, types, arguments, preconditions, effects, and composition rules — with neural implementations that ground those concepts in perception, geometry, language, and physical action (per [[Integrated Learning and Planning - Mao]]).
- Many robot manipulation tasks can be usefully written as [[Constraint Satisfaction|constraint satisfaction]] or optimization problems over poses, trajectories, contacts, and relational goals rather than as direct action prediction (per [[Integrated Learning and Planning - Mao]]).
- [[Contact Analogy]] is a one-shot transfer strategy: extract the functionally important contact structure from a demonstration, propose analogous contacts on a new object, then verify with motion planning and physics checks (per [[Integrated Learning and Planning - Mao]]).
- [[Compositional Diffusion Constraint Solvers]] treat learned spatial-relation models as reusable constraint energies or gradients, so relationships such as "left of", "near the edge", or "horizontally aligned" can be added together during object arrangement (per [[Integrated Learning and Planning - Mao]]).
- [[Composable Robot Skills]] separate temporal structure, spatial grounding, trajectory sampling, and effect prediction, allowing a planner to recombine short learned skills into longer-horizon task skeletons (per [[Integrated Learning and Planning - Mao]]).
- [[Closed-Loop Robot Agents]] need explicit systems structure because slow planners, medium-rate learned skill policies, cameras, memory, monitors, and fast controllers operate on different clocks (per [[Integrated Learning and Planning - Mao]]).
- Foundation models are useful in this framework less as a total replacement for robotics and more as structure providers: they can propose task skeletons, spatial relationships, language meanings, object segmentations, and commonsense constraints that classical planning and learned low-level modules can then ground and verify (per [[Integrated Learning and Planning - Mao]]).

## Notable quotes

- "How can we build general purpose physical intelligence?" (00:00:31)
- "Plan with such kind of compositional abstraction of states and actions." (00:06:33)
- "Robotics is not just a learning problem." (00:41:44)
- "Neural networks do not operate on themselves." (Q&A, 00:57:00)

## Referenced local papers

- `raw/assets/papers/2025-arxiv-neuro-symbolic-concepts.pdf` — conceptual umbrella paper for [[Neuro-Symbolic Concepts]].
- `raw/assets/papers/2022-neurips-pdsketch-integrated-domain-programming-learning-and-planning.pdf` — PDSketch, an integrated domain programming, learning, and planning language.
- `raw/assets/papers/2025-icra-magic-one-shot-manipulation-contact-analogies.pdf` — MAGIC, the one-shot contact-analogy system.
- `raw/assets/papers/2024-rss-set-it-up-functional-object-arrangement-compositional-generative-models.pdf` — SetItUp, functional object arrangement via abstract spatial relationship graphs and diffusion-model composition.
- `raw/assets/papers/2023-corl-learning-reusable-manipulation-strategies.pdf` — mechanism learning from contact-mode sequences and self-play.
- `raw/assets/papers/2026-icra-stack-learning-composable-skills.pdf` — STACK, learning composable skills by discovering spatial and temporal structure with foundation models.
- `raw/assets/papers/2026-retriever-programming-closed-loop-modular-robot-agent.pdf` — Retriever, a programming framework for multi-rate closed-loop robot agents.

## Connections

- [[Jiayuan Mao]]
- [[Neuro-Symbolic Concepts]]
- [[Task and Motion Planning]]
- [[Constraint Satisfaction]]
- [[Contact Analogy]]
- [[Compositional Diffusion Constraint Solvers]]
- [[Composable Robot Skills]]
- [[Closed-Loop Robot Agents]]
- [[Robot Learning]]
- [[Imitation Learning]]
- [[Vision-Language-Action Models]]
- [[Training Environments and the Gymnasium API]]

## Open questions

- Which subset of this neuro-symbolic stack is realistic to reproduce in the user's current LeIsaac/LeRobot path: contact analogies, diffusion constraint solvers, or only the high-level planning decomposition?
- How much of the demonstrated structure can be recovered from raw teleoperation logs without manual segmentation or object annotation?
- When should a self-researcher prefer simple DAgger-style data aggregation over adding explicit planning and learned effect models?
- Which prerequisite should come first for this thread: classical [[Task and Motion Planning]], diffusion-policy internals, or Modern Robotics Ch. 3-5?
