# Index

Content catalog for this vault. Every wiki page is listed here under its category, with a one-line summary. Updated on every ingest.

> Conventions: see [[AGENTS]].

## Profile

- [[about-me]] — user profile and teaching preferences for the AI tutor

## Sources

- [[Constraint gradient perpendicular to tangent - Claude explanation]] — Self-contained AI explanation of why $\nabla h \perp$ tangent of $h(x)=0$, contributing the chain-rule proof now merged into the concept page.
- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]] — Heptabase AI Tutor lesson deriving Jacobian pseudoinverse formulas from optimization and KKT/Lagrange stationarity.
- [[Integrated Learning and Planning - Mao]] — Stanford Robotics Seminar on neuro-symbolic concepts for data-efficient robot learning, planning, contact-rich manipulation, spatial reasoning, and closed-loop agents.
- [[Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al]] — Primary ACT/ALOHA paper introducing action chunking, temporal ensembling, and low-cost bimanual imitation learning.
- [[Modern Robotics - Lynch & Park]] — Lynch & Park textbook (Cambridge, 2017): geometric/PoE treatment of kinematics, dynamics, planning, control, grasping, and mobile robots; backbone of the foundation thread.

## Ingestion indices

- [[Modern Robotics - chapters]] — chapter-level status for the Modern Robotics textbook (13 chapters + 4 appendices).

## Entities

- [[Jiayuan Mao]] — Robotics and AI researcher focused on learning, reasoning, and planning with neuro-symbolic concepts grounded in perception and action.
- [[LeRobot]] — Hugging Face's open-source PyTorch library for robot learning, datasets, policies, hardware integration, and deployment.

## Concepts

- [[Action Chunking Transformer]] — Transformer-based imitation-learning policy that predicts chunks of future robot actions for smoother, shorter-horizon control.
- [[Closed-Loop Robot Agents]] — Robot-agent systems that continuously observe, update memory, plan, execute skills, monitor progress, and replan across mismatched module rates.
- [[Composable Robot Skills]] — Learned short-horizon skills with arguments, trajectory samplers, and effect models that planners can recombine into longer tasks.
- [[Compositional Diffusion Constraint Solvers]] — Diffusion-style learned relation models composed as constraint energies or gradients for spatial arrangement and planning.
- [[Configuration Space]] — Robot's C-space: dof, Grübler's formula, joint types, topology, holonomic vs. nonholonomic constraints, and task space vs. workspace (from [[Modern Robotics - Lynch & Park]] Ch. 2).
- [[Constraint Satisfaction]] — Finding robot poses, trajectories, contacts, task orders, or object layouts that jointly satisfy geometric, dynamic, relational, and preference constraints.
- [[Constraint Gradients and Tangent Spaces]] — Geometric relation between equality-constraint gradients, tangent directions, normal spaces, and constrained stationarity.
- [[Contact Analogy]] — One-shot manipulation transfer by matching functionally similar contact points or contact-mode sequences on novel objects, then verifying with planning and physics checks.
- [[Imitation Learning]] — Training robot policies from demonstrations, usually the most practical first method for a self-researcher.
- [[Isaac Lab]] — NVIDIA's Python framework for robot simulation, training, and teleoperation on top of Isaac Sim and USD; the scripting layer underneath LeIsaac.
- [[Karush-Kuhn-Tucker Conditions]] — First-order constrained-optimization conditions generalizing Lagrange multipliers to equality and inequality constraints.
- [[Lagrange Multipliers]] — Equality-constraint optimization method with an ELI5 bridge, gradient-stationarity geometry, pseudoinverse/IK connection, and Socratic checks.
- [[Moore-Penrose Pseudoinverse]] — Generalized matrix inverse used for minimum-norm and least-squares Jacobian inverse kinematics.
- [[Neuro-Symbolic Concepts]] — Reusable robot knowledge units with symbolic interfaces and neural grounding for perception, language, geometry, action, and planning.
- [[Numerical Inverse Kinematics]] — Newton-Raphson IK on SE(3): why the matrix logarithm produces the body-twist error vector, body Jacobian update, DLS near singularities (Modern Robotics §6.2.2).
- [[Robot Learning]] — Data-driven robotics methods that learn policies from rewards, demonstrations, or multimodal robot datasets.
- [[Robotics Development Stack]] — Layered map of robotics theory, hardware, middleware, simulation, data, learning, deployment, and safety.
- [[Sigmoid Function]] — Logistic squash $1/(1+e^{-x})$: smooth $\mathbb{R} \to (0,1)$ probability/gate, with the dimmer-switch analogy and vanishing-gradient pitfall.
- [[Singularity]] — Cross-domain concept linking linear-algebra rank loss, geometric tangent failures, coordinate singularities, and robotics Jacobian singularities.
- [[Task and Motion Planning]] — Jointly deciding symbolic robot actions and continuous feasible motions, poses, grasps, and trajectories.
- [[Training Environments and the Gymnasium API]] — Two-layer view of sim-based training: physics engine (MuJoCo / Isaac Sim / Genesis) vs. Gymnasium API contract; when a Gym env is required for RL training but unnecessary for ACT/DP training.
- [[Vision-Language-Action Models]] — Robot policies that condition on vision and language and output actions for physical control.
- [[VR Teleoperation in Simulation]] — VR-headset teleop pipeline for collecting LeRobot-format demos in sim: OpenXR, retargeting, IK, dataset writer; LeIsaac vs. scaffolding from scratch.

## Syntheses

- [[LeRobot Documentation Index]] — Searchable local map of the official LeRobot docs and a recommended reading path.
- [[Modern Robotics Development - synthesis]] — Whole-picture overview of modern robotics development, core tools, and realistic self-researcher paths.
- [[learning-tracker]] — curriculum, coverage map, recommendations, session log (agent-maintained)

## Journal

_None yet. Personal entries (`domain: personal`)._
