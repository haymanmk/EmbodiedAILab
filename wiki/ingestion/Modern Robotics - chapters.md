---
type: ingestion-index
source: [[Modern Robotics - Lynch & Park]]
created: 2026-05-16
updated: 2026-05-16
last_chapter_studied: 2
---

# Modern Robotics — Chapter Ingestion Index

Chapter-level tracker for [[Modern Robotics - Lynch & Park]]. Trigger phrase `study Chapter N of Modern Robotics` reads that chapter from the PDF, produces/extends concept pages, flips the row to `covered`, and updates [[learning-tracker]].

PDF: `raw/ModernRobotics-v2.pdf` (644 pages, Dec 2019 preprint of 2017 Cambridge first edition). Page numbers below are the printed page numbers (which match PDF pages once the front matter is accounted for — the PDF viewer page = printed page + 19 for chapter content).

## Chapters

| #   | Title                              | Pages    | Concepts (planned / actual)                                                                                                                                       | Status      |
| --- | ---------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| 1   | Preview                            | 1–10     | book-wide roadmap; read once for orientation, no concept pages expected                                                                                           | queued      |
| 2   | Configuration Space                | 11–56    | [[Configuration Space]] (covers dof, Grübler's formula, topology, holonomic vs. nonholonomic, task space vs. workspace); extends [[Constraint Gradients and Tangent Spaces]] | covered     |
| 3   | Rigid-Body Motions                 | 57–134   | [[SO(3) Rotation Group]], [[SE(3) Rigid-Body Group]], [[Twist]], [[Wrench]], [[Exponential Coordinates of Rotation]], [[Exponential Coordinates of Rigid-Body Motion]] | next        |
| 4   | Forward Kinematics                 | 135–168  | [[Product of Exponentials Formula]], [[Screw Axis]], [[URDF]], [[Denavit-Hartenberg Parameters]] (see App. C)                                                     | queued      |
| 5   | Velocity Kinematics and Statics    | 169–216  | [[Manipulator Jacobian]], [[Space Jacobian]], [[Body Jacobian]], [[Kinematic Singularity]], [[Manipulability Ellipsoid]], [[Static Force Analysis]]               | queued      |
| 6   | Inverse Kinematics                 | 217–242  | [[Analytic Inverse Kinematics]], [[Numerical Inverse Kinematics]], [[Newton–Raphson IK]], [[Redundant Manipulator]] — extends [[Moore-Penrose Pseudoinverse]]     | queued      |
| 7   | Kinematics of Closed Chains        | 243–268  | [[Closed Kinematic Chain]], [[Stewart–Gough Platform]], [[Parallel Mechanism]], [[Closed-Chain Singularity]]                                                      | not started |
| 8   | Dynamics of Open Chains            | 269–326  | [[Lagrangian Dynamics]], [[Manipulator Equation]], [[Mass Matrix]], [[Newton–Euler Recursive Dynamics]], [[Forward Dynamics]], [[Task-Space Dynamics]]            | queued      |
| 9   | Trajectory Generation              | 327–354  | [[Time Scaling]], [[Polynomial Via-Points]], [[Time-Optimal Time Scaling]]                                                                                        | not started |
| 10  | Motion Planning                    | 355–404  | [[Motion Planning]], [[C-Space Obstacle]], [[RRT]], [[PRM]], [[Potential Fields]], [[Trajectory Optimization]]                                                    | not started |
| 11  | Robot Control                      | 405–462  | [[Error Dynamics]], [[Computed-Torque Control]], [[PID Joint Control]], [[Task-Space Control]], [[Force Control]], [[Hybrid Motion-Force Control]], [[Impedance Control]] | not started |
| 12  | Grasping and Manipulation          | 463–514  | [[Contact Kinematics]], [[Friction Cone]], [[Form Closure]], [[Force Closure]], [[Grasp Analysis]]                                                                | not started |
| 13  | Wheeled Mobile Robots              | 515–566  | [[Omnidirectional Mobile Robot]], [[Nonholonomic Mobile Robot]], [[Mobile Manipulation]], [[Odometry]]                                                            | deferred    |
| A   | Summary of Useful Formulas         | 567–576  | reference appendix; no concept pages                                                                                                                              | reference   |
| B   | Other Representations of Rotations | 577–586  | [[Euler Angles]], [[Roll-Pitch-Yaw Angles]], [[Unit Quaternions]], [[Cayley–Rodrigues Parameters]]                                                                | reference   |
| C   | Denavit–Hartenberg Parameters      | 587–598  | [[Denavit-Hartenberg Parameters]] — read alongside Ch. 4                                                                                                          | reference   |
| D   | Optimization and Lagrange Multipliers | 599–600 | already covered: [[Lagrange Multipliers]], [[Karush-Kuhn-Tucker Conditions]], [[Constraint Gradients and Tangent Spaces]]                                       | covered     |

## Status legend

- **not started** — out of scope for the current foundation thread.
- **queued** — on the recommended reading path, not yet next.
- **next** — the next chapter to study under [[learning-tracker]].
- **covered** — concept pages written / extended for this chapter.
- **deferred** — knowingly skipped for now; revisit if a project demands.
- **reference** — appendix or supplementary; consult on demand, no full read planned.

## Reading path (current)

Foundation thread per [[learning-tracker]]: **Ch. 3 → Ch. 4 → Ch. 5 → Ch. 6**, then revisit ACT / Diffusion Policy deep-reads. Ch. 2 is a brief warm-up before Ch. 3 if the manifold framing feels unfamiliar. Ch. 8 (dynamics) is queued after IK for any torque-level control or model-based RL work.

## Notes

- The wikilinks above are *aspirational* — most are red links until the corresponding chapter is studied. They are listed so the `study Chapter N` workflow has unambiguous targets to create/extend.
- App. D is marked `covered` because the optimization-math thread already produced the relevant pages from other sources (Boyd & Vandenberghe snapshot, Heptabase pseudoinverse lesson). Re-reading App. D when Ch. 8 is studied may still surface refinements.
