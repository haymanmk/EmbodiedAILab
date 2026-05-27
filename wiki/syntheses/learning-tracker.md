---
type: synthesis
domain: personal
created: 2026-05-16
updated: 2026-05-27
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
4. **Task and motion planning overview** — now adjacent because [[Integrated Learning and Planning - Mao]] leans heavily on [[Task and Motion Planning]], [[Constraint Satisfaction]], learned samplers, and effect models. Keep it as a short conceptual onramp after Ch. 3–5, not a detour before kinematics.

**Reference (not a study target)**: [[Sutton & Barto - RL]] — keep accessible for RL theory lookups when ACT/Diffusion Policy reference policy-gradient or behavior-cloning concepts. Not a deep-read target unless RL becomes the primary thread later.

## Coverage map

### Concepts covered (with mastery signal)

| Concept | Source | Last studied | Mastery |
|---|---|---|---|
| [[Configuration Space]] | Modern Robotics Ch. 2 | 2026-05-16 | building |
| [[Sigmoid Function]] | /tutor explain (dimmer-switch analogy) | 2026-05-16 | working |
| [[Lagrange Multipliers]] | Modern Robotics App. D + /tutor page revision | 2026-05-25 | working |
| [[Karush-Kuhn-Tucker Conditions]] | Modern Robotics App. D | 2026-05-14 | working |
| [[Constraint Gradients and Tangent Spaces]] | Modern Robotics §2.4 + App. D | 2026-05-17 | working |
| [[Singularity]] | Modern Robotics Ch. 2/5 + pseudoinverse notes | 2026-05-18 | building |
| [[Action Chunking Transformer]] | ACT paper | 2026-05-10 | overview-only |
| [[Vision-Language-Action Models]] | reading | 2026-05-09 | overview-only |
| [[Robot Learning]] | reading | 2026-05-09 | overview-only |
| [[Imitation Learning]] | reading + /tutor (DAgger vs HIL-SERL correction patterns) | 2026-05-24 | building |
| [[Moore-Penrose Pseudoinverse]] | reading | 2026-05-09 | overview-only |
| [[VR Teleoperation in Simulation]] | /tutor deep-research (LeIsaac vs scratch, prereqs, core tech) | 2026-05-18 | overview-only |
| [[Training Environments and the Gymnasium API]] | /tutor explain (power-outlet analogy; RL vs IL pipeline mapping) | 2026-05-24 | working |
| [[Neuro-Symbolic Concepts]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |
| [[Task and Motion Planning]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |
| [[Constraint Satisfaction]] | [[Integrated Learning and Planning - Mao]] + optimization pages | 2026-05-27 | building |
| [[Contact Analogy]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |
| [[Compositional Diffusion Constraint Solvers]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |
| [[Composable Robot Skills]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |
| [[Closed-Loop Robot Agents]] | [[Integrated Learning and Planning - Mao]] | 2026-05-27 | overview-only |

Mastery levels: **overview-only** (skimmed) → **building** (working through) → **working** (can apply) → **fluent** (can teach/derive).

### Resource progress

| Resource | Format | Progress | Status |
|---|---|---|---|
| [[Modern Robotics - Lynch & Park]] | textbook | Ingested 2026-05-16; chapter index at [[Modern Robotics - chapters]]; Ch. 3 = next | in-progress |
| [[Sutton & Barto - RL]] | textbook | Not started | reference |
| [[LeRobot Documentation Index]] | docs-site | Reference-only browsing | reference |
| [[Integrated Learning and Planning - Mao]] | video + papers | Ingested 2026-05-27; source page plus 7 concept/entity pages | covered |
| ACT paper | paper | Overview read | revisit later |
| Diffusion Policy paper | paper | Not started | queued |

## Gaps detected (agent-maintained)

Things the agent has noticed are missing from coverage but are prerequisites for queued material:

- **Convex sets & convex functions** — referenced by KKT but not yet a concept page. Needed before policy gradient theory.
- **Multivariate calculus refresher (Jacobians, Hessians)** — referenced by both optimization and ML training. Likely background but not explicitly indexed in the wiki.
- **SE(3) / rigid-body transforms** — prerequisite for Modern Robotics Ch. 3 onward; will be covered when that chapter is studied.
- **Manifolds / topology basics** — Ch. 2 introduced topology of C-space ($S^1$, $T^n$, $S^n$) at a level the user could absorb. A dedicated page on topological equivalence / charts / atlas would help if Ch. 3 pushes deeper into $SO(3)$'s manifold structure.
- **Quaternions + SLERP** — surfaced by [[VR Teleoperation in Simulation]] (orientation smoothing in the teleop loop). Will be covered as part of Ch. 3 ($SO(3)$ representations) — confirm Lynch & Park's coverage is sufficient, supplement otherwise.
- **Inverse kinematics methods** — Modern Robotics Ch. 6 is the primary source; DLS + analytic IK are the two flavors that show up in real teleop loops.
- **Diffusion model internals** — [[Compositional Diffusion Constraint Solvers]] and Diffusion Policy both rely on denoising/score-style generation; this should be taught before a serious Diffusion Policy or SetItUp deep-read.
- **TAMP basics** — [[Task and Motion Planning]] is now indexed, but only at overview level. A deeper pass should cover symbolic action schemas, motion planning, feasibility checking, samplers, and task skeletons.

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
- 2026-05-24 — `/tutor` follow-up: user asked whether HIL-SERL can "correct" an IL policy. Expanded [[Imitation Learning]] with a new `## Correcting an IL policy with human interventions` section covering the **two flavors** (DAgger / HG-DAgger stays in supervised IL; HIL-SERL switches to RL with reward + interventions), the **architectural friction** that ACT (action chunks) and Diffusion Policy (implicit log-prob via denoising) have with RL fine-tuning, a Mermaid **decision flow** (reward feasible? policy RL-friendly?), and the **deeper insight** that distribution shift has exactly two fixes (expand demonstrated distribution OR add reward signal). Practical recommendation for LeIsaac: prefer DAgger-style corrective demos over standing up an RL pipeline. Added DAgger / HG-DAgger / HIL-SERL / RLPD paper links to external sources. Cross-linked from [[Training Environments and the Gymnasium API]]. Bumped Imitation Learning mastery from `overview-only` to `building`.
- 2026-05-24 — `/tutor` created [[Training Environments and the Gymnasium API]] after the user asked how `gym_hil` relates to physics simulators and whether HIL-SERL's training paradigm transfers to ACT/DP. Verified via WebFetch that `gym_hil` is a thin MuJoCo wrapper. Page leads with the power-outlet/appliance analogy + breakdown (interface portability vs. physics fidelity), Mermaid layer diagram (algorithm → wrapper → engine), the "what `gym.make(...)` does and does not tell you" enumeration, and the **RL-vs-IL stage table** showing when a Gym env is required (RL training), useful (eval, RL collection), or unnecessary (IL training). Closes with ACT's loss form, the distribution-shift / compounding-error motivation for action chunking, and the practical mapping that LeIsaac's IL pipeline rightly bypasses the Gymnasium API during teleop collection. Socratic check covered three questions; user answered Q1 fully, Q2 mostly (corrected: rewards not used by IL even at collection; teleop typically bypasses the Gym API), Q3 in spirit (sharpened: ACT compares predicted *action chunks* to demonstrated actions via L1, not state-trajectory distance). Cross-links to [[Isaac Lab]], [[VR Teleoperation in Simulation]], [[Action Chunking Transformer]], [[Imitation Learning]], [[Robot Learning]].
- 2026-05-24 — `/tutor` deep-research on **Genesis physics simulator** (`genesis-world`, Genesis-Embodied-AI). Created `raw/genesis-world-research-snapshot.md` (333 lines) — critical, evidence-based capture of speed/fidelity claims and independent pushback. Key findings: the headline "43M FPS / 10–80× faster" claim does not survive Stone Tao's independent benchmark (Genesis at parity with Isaac Lab on locomotion, 3–10× slower than ManiSkill on manipulation); generative framework still closed and effectively spun out into for-profit **Genesis AI** ($105M seed July 2025, GENE-26.5 model May 2026); **no first-party VR/XR** confirmed in issue #1626 — Isaac Lab 2.3.2 (Jan 2026) ships Meta Quest VR teleop, so the LeIsaac onramp track is unaffected. Real differentiator is multi-physics breadth (rigid + MPM + SPH + FEM + PBD + Stable Fluid in one engine). Current version v0.4.7 (2026-05-16) uses in-house Quadrants compiler since v0.4.0. Raw file only; no wiki page yet — ingestion deferred. No coverage-map row (not a covered concept).
- 2026-05-18 — `/tutor` deep-research on **VR teleoperation in simulation for policy training**. Created [[VR Teleoperation in Simulation]] concept page with puppeteer-on-video-call analogy + breakdown (no force feedback), full data-flow Mermaid diagram, layered "use the stack vs. scaffold from scratch" decision matrix, hardware/skills prerequisites table (with bridges to user's active Ch. 3 gap), and per-technology deep-dives: OpenXR, CloudXR, frame conversion, retargeting (Gram-Schmidt hand frame, BEAVR-style), IK (analytic vs DLS vs GPU/cuRobo), smoothing (SLERP + moving-average), Isaac Sim vs MuJoCo, LeRobot dataset schema. Pulled live docs from `/lightwheelai/leisaac` and `/isaac-sim/isaaclab` via context7. Flagged **quaternions+SLERP** and **IK methods** as gaps now adjacent to active Ch. 3 work.
- 2026-05-25 — `/tutor` revised [[Lagrange Multipliers]] to comply with the current tutoring rule: added an ELI5 opening, painted-path everyday analogy with explicit breakdown, clearer definition/intuition split, preserved existing visual sequence, moved pseudoinverse material into a robotics connection, added origins/variations sections, and closed with an Obsidian Socratic-check callout. Follow-up clarified the notation trap: the rule is $h(x)=0$, the normal direction is $\nabla h(x)$, and the balancing term is $\lambda \nabla h(x)$; revised "push back" wording to "balance" to avoid implying trajectory correction. Kept mastery at `working`; this is a reference-page cleanup rather than new coverage.
- 2026-05-27 — `ingest Integrated Learning and Planning`: created [[Integrated Learning and Planning - Mao]] plus [[Jiayuan Mao]], [[Neuro-Symbolic Concepts]], [[Task and Motion Planning]], [[Constraint Satisfaction]], [[Contact Analogy]], [[Compositional Diffusion Constraint Solvers]], [[Composable Robot Skills]], and [[Closed-Loop Robot Agents]]. Downloaded and linked local PDFs for Neuro-Symbolic Concepts, PDSketch, MAGIC, SetItUp, Learning Reusable Manipulation Strategies, STACK, and Retriever. Positioned the seminar as a bridge from IL/VLA policy learning to structured planning and learned skill composition; kept mastery overview-only except [[Constraint Satisfaction]] at building because it reinforces existing optimization pages.
