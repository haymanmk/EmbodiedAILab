---
type: source
domain: research
created: 2026-05-16
updated: 2026-05-16
source_url: http://modernrobotics.org
source_path: raw/ModernRobotics-v2.pdf
source_format: pdf
total_pages: 644
author: Kevin M. Lynch, Frank C. Park
published: 2017
edition: Updated first edition (Dec 2019 preprint)
publisher: Cambridge University Press
chunks_indexed: false
indexed_at:
study_status: in-progress
tags: [robotics, kinematics, dynamics, motion-planning, control, manipulation, textbook]
---

# Modern Robotics - Lynch & Park

> Full title: *Modern Robotics: Mechanics, Planning, and Control*.
> The PDF at `raw/ModernRobotics-v2.pdf` is the Dec 2019 preprint of the
> updated first edition; cite the printed 2017 Cambridge edition.

## Summary

Lynch & Park is an undergraduate textbook that unifies robot mechanics,
planning, and control around a *geometric* treatment of rigid-body motion.
The defining choice is to represent configurations of rigid bodies as
elements of the Lie groups $SO(3)$ and $SE(3)$, and joint motions as
matrix exponentials of twists / screw axes — the **product of exponentials
(PoE)** formula. From that foundation, the book builds forward and inverse
kinematics, the Jacobian and singularities, open- and closed-chain
dynamics (Lagrangian and Newton–Euler), trajectory generation, motion
planning, robot control (motion, force, hybrid, impedance), grasping with
contact mechanics and form/force closure, and wheeled mobile robots.
Appendices cover alternative rotation representations (Euler angles, RPY,
quaternions, Cayley–Rodrigues), Denavit–Hartenberg parameters with their
relation to PoE, and a short optimization / Lagrange-multipliers refresher.
The book assumes only freshman-level physics, ODEs, linear algebra, and
some programming, and is the queued backbone of the **foundation thread**
in [[learning-tracker]] — its kinematics chapters supply the language ACT,
Diffusion Policy, and the broader robot-learning literature assume.

## Why this book for this vault

- **Closes the "what does a robot do" loop** before policy-learning theory
  layers on top: $SE(3)$, twists/wrenches, Jacobians, and singularities
  are the action-space and observation-space vocabulary of [[Action
  Chunking Transformer]] and [[Imitation Learning]] more broadly.
- **Geometric, not D–H first.** Joint motion as $e^{[\mathcal{S}]\theta}$
  is reusable: the same machinery shows up in IK damped least squares,
  trajectory optimization, and policy parameterizations on $SE(3)$.
- **Self-contained derivations.** Useful for the user's active gaps —
  optimization math, constrained motion, statics — without forcing a
  detour through a separate math methods book.

## Key claims (chapter-anchored)

- **Configuration space (Ch. 2)** — A robot's configuration is a point in
  a manifold whose dimension equals its degrees of freedom; topology
  (cylinder vs. sphere vs. torus) matters for choosing representations.
  Grübler's formula computes dof for general mechanisms.
- **Rigid-body motions (Ch. 3)** — Orientation lives in $SO(3)$, full
  pose in $SE(3)$. Angular velocities are skew-symmetric matrices, twists
  are 6-vectors $(\omega, v)$, and the **exponential map** $e^{[\mathcal{S}]\theta}$
  reproduces rotations and rigid-body motions from screw axes.
- **Forward kinematics (Ch. 4)** — The **product of exponentials**
  $T(\theta) = e^{[\mathcal{S}_1]\theta_1} \cdots e^{[\mathcal{S}_n]\theta_n} M$
  gives end-effector pose without per-link frames. Two formulations:
  screws in the base frame (space form) and in the end-effector frame
  (body form). D–H parameters covered in Appendix C as the older
  alternative.
- **Velocity kinematics & statics (Ch. 5)** — Joint velocities map to
  end-effector twists through the **Jacobian** $J(\theta)$. Singularities
  are configurations where $J$ loses rank. The same Jacobian, transposed,
  maps end-effector wrenches to joint torques: $\tau = J^\top \mathcal{F}$.
  Manipulability ellipsoid characterizes directional ease of motion.
- **Inverse kinematics (Ch. 6)** — Closed-form solutions exist for special
  6R structures (PUMA, Stanford). General case is solved iteratively via
  Newton–Raphson on the FK map; redundant arms use the Jacobian
  pseudoinverse — connects directly to [[Moore-Penrose Pseudoinverse]]
  and the constrained-optimization view in [[Karush-Kuhn-Tucker Conditions]].
- **Closed chains (Ch. 7)** — Stewart–Gough platforms and parallel
  mechanisms have multi-valued FK and additional singularity types
  (actuator, configuration, end-effector) absent in serial arms.
- **Dynamics of open chains (Ch. 8)** — Lagrangian formulation builds the
  manipulator equation $M(\theta)\ddot\theta + C(\theta,\dot\theta)\dot\theta + g(\theta) = \tau$;
  Newton–Euler gives a recursive inverse-dynamics algorithm with
  $O(n)$ complexity. Friction, gearing, and joint flexibility are treated
  as modular add-ons.
- **Trajectory generation (Ch. 9)** — Point-to-point time scalings,
  polynomial via-points, and time-optimal time scaling via the
  $(s, \dot s)$ phase plane.
- **Motion planning (Ch. 10)** — Grid methods, sampling planners (RRT,
  PRM), potential fields, and nonlinear-optimization planners, all built
  on the configuration-space-obstacle abstraction.
- **Robot control (Ch. 11)** — Velocity-input and torque-input motion
  control of single and multi-joint robots; force control; hybrid
  motion–force control via natural/artificial constraints; impedance and
  admittance control for compliant interaction.
- **Grasping & manipulation (Ch. 12)** — Contact kinematics (rolling,
  sliding, breaking free), friction cones, form closure and force
  closure, and the duality between force and motion freedoms.
- **Wheeled mobile robots (Ch. 13)** — Omnidirectional and nonholonomic
  bases, controllability (the Lie-bracket / accessibility story), motion
  planning under nonholonomic constraints, odometry, and mobile
  manipulation.
- **Appendix D** is a compact reference for Lagrange multipliers — already
  the entry point used in [[Lagrange Multipliers]] and [[Karush-Kuhn-Tucker Conditions]].

## How to read this (for me)

Per [[learning-tracker]] recommendation #1, the immediate plan is:

1. **Ch. 3 — Rigid-Body Motions** (p. 57). Trigger phrase:
   `study Chapter 3 of Modern Robotics`. Establishes $SO(3)$, $SE(3)$,
   twists/wrenches — prerequisite for everything that follows and a
   listed gap in [[learning-tracker]] (SE(3) / rigid-body transforms).
2. **Ch. 4 — Forward Kinematics** (p. 135). PoE formula.
3. **Ch. 5 — Velocity Kinematics & Jacobians** (p. 169). Connects back
   to [[Moore-Penrose Pseudoinverse]] (IK uses $J^+$) and to the action
   space of imitation-learning policies.
4. **Ch. 6 — Inverse Kinematics** (p. 217). Numerical IK and redundancy.

Ch. 2 (configuration space) is a foundational reader-warmup — skim unless
the topology/manifold framing is unfamiliar. Ch. 7 (closed chains) can be
deferred unless a parallel mechanism shows up in a project. Ch. 8
(dynamics) is needed for torque-level control and any model-based RL.
Ch. 10–11 are revisitable as references when planning/control questions
come up; Ch. 12 (grasping) is highly relevant for [[Imitation Learning]]
manipulation tasks. Ch. 13 only if mobile bases enter scope.

Chapter index and per-chapter status are tracked in
[[Modern Robotics - chapters]].

## Software & companion resources

- Library code, videos, simulator (CoppeliaSim/V-REP scenes), and
  practice problems live at <http://modernrobotics.org>.
- Each chapter has a §X.6 / §X.11 "Software" subsection listing the
  reference implementations (`ModernRoboticsCpp`, `ModernRobotics`
  Python/MATLAB packages).
- The book is the upstream of the Coursera *Modern Robotics
  Specialization* taught by Lynch.

## Connections

- [[Modern Robotics - chapters]] — chapter-level ingestion index (status,
  concepts touched, page refs).
- [[Modern Robotics Development - synthesis]] — the higher-level "modern
  robotics development" thesis page; this book grounds the *kinematics &
  control* layer of that map.
- [[Lagrange Multipliers]] — Appendix D and Ch. 8 (Lagrangian dynamics).
- [[Karush-Kuhn-Tucker Conditions]] — relevant for §6.2 / §11.6 / Ch. 12
  contact-force constrained optimization.
- [[Constraint Gradients and Tangent Spaces]] — the geometric story
  recurs in §2.4 (configuration / velocity constraints) and §13.3
  (nonholonomic constraints).
- [[Moore-Penrose Pseudoinverse]] — §6.2 redundant IK.
- [[Robotics Development Stack]] — locates this book in the broader stack.
- [[Action Chunking Transformer]] — IL action spaces use the joint /
  end-effector vocabulary defined in Ch. 3–5.
- [[Imitation Learning]] — same.
- [[learning-tracker]] — curriculum bookkeeping for chapter progress.

## Open questions

- How directly does the PoE formula translate into the action-space
  parameterization choices in [[Action Chunking Transformer]] and
  Diffusion Policy (joint vs. end-effector vs. delta-pose actions)?
- Is the Jacobian-pseudoinverse IK loop in §6.2 the cleanest reference
  for the residual-loss derivation in [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]]?
- For learned policies that violate the manipulator equation
  assumptions (e.g., underactuation, contact-rich tasks), which chapters
  remain authoritative and which need to be supplemented by
  contact-mechanics or RL references?
- How much of Ch. 13 (nonholonomic systems) is needed for embodied-AI
  work on legged or wheeled platforms vs. delegating to MuJoCo / Isaac
  built-in dynamics?
