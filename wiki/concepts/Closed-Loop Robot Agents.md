---
type: concept
domain: research
created: 2026-05-27
updated: 2026-05-27
aliases: ["closed-loop robot agent", "multi-rate robot agents", "Retriever"]
tags: [robotics, systems, planning, control, vla, closed-loop]
---

# Closed-Loop Robot Agents

## Definition

A closed-loop robot agent is a robot system that continuously observes, updates memory or belief, plans, executes skills, monitors progress, and replans when the world differs from expectation. The "closed-loop" part means action is not a one-shot script: new observations flow back into planning and control.

In [[Integrated Learning and Planning - Mao]], Retriever is presented as a programming framework for closed-loop robot agents where slow VLM planning, medium-rate skill policies, monitoring, memory, teleoperation override, cameras, and fast controllers can run together with explicit timing and data handoff.

## Why this matters

Long-horizon robot tasks are not just ML inference calls. A realistic agent may need:

- cameras at roughly video rate;
- state estimation and memory updates;
- a VLM or LLM planner operating on second-scale latency;
- a learned VLA skill policy producing action chunks;
- an execution monitor checking progress;
- a high-rate joint controller;
- human teleoperation override or safety fallback.

If these modules share data through implicit queues and callbacks, the system becomes hard to replay, debug, and reason about. Retriever's key idea is to make clocks and synchronization policies part of the program rather than hidden middleware behavior.

## Origins / sources

- [[Integrated Learning and Planning - Mao]] uses Retriever in the foundation-model-era reflection section.
- The local paper `raw/assets/papers/2026-retriever-programming-closed-loop-modular-robot-agent.pdf` is the downloaded Retriever reference.
- This concept links directly to the user's automation background: it is the systems layer where planning, learned policies, and control loops must coexist.

## Variations / debates

- Open-loop execution is simpler and can work for short tasks, but it fails when perception is partial, objects move, or early actions change later feasibility.
- Closed-loop execution can recover by updating belief and replanning, but it introduces timing, synchronization, logging, and safety complexity.
- A VLA policy alone does not solve the systems problem; it still has to be embedded in a loop with perception, state, monitoring, and control.

## Related concepts

- [[Vision-Language-Action Models]]
- [[Training Environments and the Gymnasium API]]
- [[Task and Motion Planning]]
- [[Composable Robot Skills]]
- [[Robot Learning]]

## Mentions

- [[Integrated Learning and Planning - Mao]]
