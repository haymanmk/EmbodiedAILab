---
type: synthesis
domain: personal
created: 2026-05-16
updated: 2026-05-16
tags: [learning, tracker, curriculum]
---

# Learning Tracker

> Source of truth for what I've covered, what I'm doing now, what's queued.
> Agent updates this at the end of each tutor workflow (auto-commit).

## Active focus (this week / next 2 weeks)

- **Foundation thread**: Optimization math (KKT, Lagrange, constraint
  gradients). Currently working through [[Constraint Gradients and Tangent Spaces]].
  Next: convex analysis basics, then onward to manipulator kinematics.
- **Active project**: (none currently named)

## Recommendations (ranked, with rationale)

1. **Modern Robotics Ch. 3–5** (Rigid-Body Motions → Forward Kinematics →
   Velocity Kinematics & Jacobians) — closes the "what does a robot do"
   loop. Foundational language the IL papers assume.
2. **ACT paper deep-read** — once kinematics is in place, the action-space
   side of ACT becomes readable; transformer mechanics are the new piece.
3. **Diffusion Policy paper deep-read** — natural next step after ACT;
   contrast the two action representations head-to-head.

**Reference (not a study target)**: [[Sutton & Barto - RL]] — keep
accessible for RL theory lookups when ACT/Diffusion Policy reference
policy-gradient or behavior-cloning concepts. Not a deep-read target
unless RL becomes the primary thread later.

## Coverage map

### Concepts covered (with mastery signal)

| Concept | Source | Last studied | Mastery |
|---|---|---|---|
| [[Lagrange Multipliers]] | Modern Robotics §2 | 2026-05-14 | working |
| [[Karush-Kuhn-Tucker Conditions]] | Modern Robotics §2 | 2026-05-14 | working |
| [[Constraint Gradients and Tangent Spaces]] | Modern Robotics §2 | 2026-05-15 | building |
| [[Action Chunking Transformer]] | ACT paper | 2026-05-10 | overview-only |
| [[Vision-Language-Action Models]] | reading | 2026-05-09 | overview-only |
| [[Robot Learning]] | reading | 2026-05-09 | overview-only |
| [[Imitation Learning]] | reading | 2026-05-09 | overview-only |
| [[Moore-Penrose Pseudoinverse]] | reading | 2026-05-09 | overview-only |

Mastery levels: **overview-only** (skimmed) → **building** (working through)
→ **working** (can apply) → **fluent** (can teach/derive).

### Resource progress

| Resource | Format | Progress | Status |
|---|---|---|---|
| [[Modern Robotics - Lynch & Park]] | textbook | Not yet ingested | queued |
| [[Sutton & Barto - RL]] | textbook | Not started | reference |
| [[LeRobot Documentation Index]] | docs-site | Reference-only browsing | reference |
| ACT paper | paper | Overview read | revisit later |
| Diffusion Policy paper | paper | Not started | queued |

## Gaps detected (agent-maintained)

Things the agent has noticed are missing from coverage but are
prerequisites for queued material:

- **Convex sets & convex functions** — referenced by KKT but not yet a
  concept page. Needed before policy gradient theory.
- **Multivariate calculus refresher (Jacobians, Hessians)** — referenced
  by both optimization and ML training. Likely background but not
  explicitly indexed in the wiki.
- **SE(3) / rigid-body transforms** — prerequisite for Modern Robotics
  Ch. 3 onward; will be covered when that chapter is studied.

## Session log

Append-only. One entry per tutor workflow.

- 2026-05-16 — Bootstrapped learning tracker from existing wiki coverage.
