---
type: synthesis
domain: personal
created: 2026-05-16
updated: 2026-05-18
tags: [learning, tracker, curriculum]
---

# Learning Tracker

> Source of truth for what I've covered, what I'm doing now, what's queued. Agent updates this at the end of each tutor workflow (auto-commit).

## Active focus (this week / next 2 weeks)

- **Foundation thread**: Working through manipulator kinematics in [[Modern Robotics - Lynch & Park]]. Ch. 2 ([[Configuration Space]]) is covered. Next chapter to study: **Ch. 3 — Rigid-Body Motions** ($SO(3)$, $SE(3)$, twists, exponential coordinates). Chapter-level status lives in [[Modern Robotics - chapters]].
- **Optimization math** stays in working state — [[Lagrange Multipliers]], [[Karush-Kuhn-Tucker Conditions]], [[Constraint Gradients and Tangent Spaces]] are accessible references; revisit when Ch. 6 (IK) and Ch. 8 (Lagrangian dynamics) come up.
- **Active project**: (none currently named)

## Recommendations (ranked, with rationale)

1. **Modern Robotics Ch. 3–5** (Rigid-Body Motions → Forward Kinematics → Velocity Kinematics & Jacobians) — closes the "what does a robot do" loop. Foundational language the IL papers assume.
2. **ACT paper deep-read** — once kinematics is in place, the action-space side of ACT becomes readable; transformer mechanics are the new piece.
3. **Diffusion Policy paper deep-read** — natural next step after ACT; contrast the two action representations head-to-head.

**Reference (not a study target)**: [[Sutton & Barto - RL]] — keep accessible for RL theory lookups when ACT/Diffusion Policy reference policy-gradient or behavior-cloning concepts. Not a deep-read target unless RL becomes the primary thread later.

## Coverage map

### Concepts covered (with mastery signal)

| Concept | Source | Last studied | Mastery |
|---|---|---|---|
| [[Configuration Space]] | Modern Robotics Ch. 2 | 2026-05-16 | building |
| [[Sigmoid Function]] | /tutor explain (dimmer-switch analogy) | 2026-05-16 | working |
| [[Lagrange Multipliers]] | Modern Robotics App. D | 2026-05-14 | working |
| [[Karush-Kuhn-Tucker Conditions]] | Modern Robotics App. D | 2026-05-14 | working |
| [[Constraint Gradients and Tangent Spaces]] | Modern Robotics §2.4 + App. D | 2026-05-17 | working |
| [[Singularity]] | Modern Robotics Ch. 2/5 + pseudoinverse notes | 2026-05-18 | building |
| [[Action Chunking Transformer]] | ACT paper | 2026-05-10 | overview-only |
| [[Vision-Language-Action Models]] | reading | 2026-05-09 | overview-only |
| [[Robot Learning]] | reading | 2026-05-09 | overview-only |
| [[Imitation Learning]] | reading | 2026-05-09 | overview-only |
| [[Moore-Penrose Pseudoinverse]] | reading | 2026-05-09 | overview-only |

Mastery levels: **overview-only** (skimmed) → **building** (working through) → **working** (can apply) → **fluent** (can teach/derive).

### Resource progress

| Resource | Format | Progress | Status |
|---|---|---|---|
| [[Modern Robotics - Lynch & Park]] | textbook | Ingested 2026-05-16; chapter index at [[Modern Robotics - chapters]]; Ch. 3 = next | in-progress |
| [[Sutton & Barto - RL]] | textbook | Not started | reference |
| [[LeRobot Documentation Index]] | docs-site | Reference-only browsing | reference |
| ACT paper | paper | Overview read | revisit later |
| Diffusion Policy paper | paper | Not started | queued |

## Gaps detected (agent-maintained)

Things the agent has noticed are missing from coverage but are prerequisites for queued material:

- **Convex sets & convex functions** — referenced by KKT but not yet a concept page. Needed before policy gradient theory.
- **Multivariate calculus refresher (Jacobians, Hessians)** — referenced by both optimization and ML training. Likely background but not explicitly indexed in the wiki.
- **SE(3) / rigid-body transforms** — prerequisite for Modern Robotics Ch. 3 onward; will be covered when that chapter is studied.
- **Manifolds / topology basics** — Ch. 2 introduced topology of C-space ($S^1$, $T^n$, $S^n$) at a level the user could absorb. A dedicated page on topological equivalence / charts / atlas would help if Ch. 3 pushes deeper into $SO(3)$'s manifold structure.

## Session log

Append-only. One entry per tutor workflow.

- 2026-05-16 — Bootstrapped learning tracker from existing wiki coverage.
- 2026-05-16 — `ingest Modern Robotics`: created source page [[Modern Robotics - Lynch & Park]] and chapter index [[Modern Robotics - chapters]] (13 chapters + appendices A–D, App. D marked covered, Ch. 3 marked next). Updated resource progress to `in-progress` and pivoted active focus from optimization math to manipulator kinematics.
- 2026-05-16 — `study Chapter 2 of Modern Robotics` (Configuration Space): created [[Configuration Space]] concept page with house-address everyday analogy + breakdown, covering dof, Grübler's formula, joint types, topology ($S^1$, $T^n$, $S^n$, atlas vs. implicit representations), holonomic vs. nonholonomic constraints, and task space vs. workspace. Embedded inline SVG of 2R arm and its torus C-space. Extended [[Constraint Gradients and Tangent Spaces]] with a "Connection to robotics: holonomic constraints" section bridging the optimization-math view to the C-space view. Flipped Ch. 2 status to `covered` in [[Modern Robotics - chapters]].
- 2026-05-16 — `/tutor explain the sigmoid function`: created [[Sigmoid Function]] with dimmer-switch analogy and explicit breakdown (linear-dial vs. saturating-output asymmetry, foreshadowing vanishing gradients). Matplotlib plot at `wiki/assets/sigmoid/sigmoid.py` → `sigmoid.png` (sigmoid + its derivative, σ(0)=1/2 marked, saturation labels) embedded in the concept page. Validates the matplotlib convention end-to-end.
- 2026-05-16 — Re-taught $\nabla h(x) \perp$ tangent of $h(x)=0$ via the hiker-on-contour-line analogy with breakdown (regular points only; $n$-dim hyperplane vs. 2D picture). Folded the analogy into [[Constraint Gradients and Tangent Spaces]] as a `## Bridges from` section so future sessions reuse it. Mastery on Constraint Gradients bumped to working.
- 2026-05-16 — Added three visual aids to [[Constraint Gradients and Tangent Spaces]]: (1) matplotlib contour field of an elliptical bowl with $\nabla h$ arrows perpendicular to the $h=1$ level set at multiple sample points; (2) side-by-side matplotlib panels contrasting a tangent step (h: 1.000→1.047, second-order drift) with a normal step of equal Euclidean length (h: 1.000→1.270, first-order drift), making the "perpendicular to first order" statement concrete; (3) inline SVG of two constraint surfaces $h_1=h_2=0$ intersecting in $\mathbb{R}^3$, with tangent in $\operatorname{null}(J_h)$ and normal space as $\operatorname{span}(\nabla h_1, \nabla h_2)$.
- 2026-05-16 — `ingest` of `raw/Explain Why Constraint gradient is perpendicular to Tangent of h(x)=0.md`: created [[Constraint gradient perpendicular to tangent - Claude explanation]] source page and merged the **chain-rule proof** into [[Constraint Gradients and Tangent Spaces]] alongside the existing Taylor argument. Both proofs end at $\nabla h^\top v = 0$ through different formalism — added a "Why both arguments agree" closer.
- 2026-05-17 — `/tutor` clarified "vanishing correction" in [[Constraint Gradients and Tangent Spaces]]: added the unit-circle example $h(x,y)=x^2+y^2-1$, showing that a tangent step from $(1,0)$ to $(1,\epsilon)$ violates the constraint by $\epsilon^2$ and needs only a second-order inward correction. Reinforces that tangent spaces describe feasible velocities, while exact finite motion on a curved constraint may need a higher-order correction.
- 2026-05-17 — `/tutor` created [[Singularity]] as a cross-domain concept page connecting linear-algebra rank loss, geometric failures of a clean tangent model, representation singularities in coordinates, and robotics Jacobian singularities. Backlinked it from [[Constraint Gradients and Tangent Spaces]], [[Configuration Space]], and [[Moore-Penrose Pseudoinverse]].
- 2026-05-18 — `/tutor` amended [[Singularity]] with an `## Explain like I'm 5` section at the top: room-map analogy ("a bad spot where the map stops being helpful") followed by four kid-language one-liners covering the number-machine, shape, Earth-map, and robot-arm cases — each one previewing the corresponding domain section below. Sits before "Bridges from" so the simplest framing is the reader's first contact.
- 2026-05-18 — `/tutor` added `## Reading the analogy across domains` section to [[Singularity]] after a comprehension check from the user. Clarifies that "map" is being used in the *mathematical* (function-between-spaces) sense, not lookup-table sense, and gives a per-domain "room vs. map" table (input vector space ↔ matrix; curve ↔ parametrization; sphere ↔ lat/long; reachable poses ↔ forward kinematics). Closes with an Obsidian `[!question]` Socratic callout asking which row is map-only-broken vs. room-broken — pointing the reader at the geometric-vs.-representation distinction.
