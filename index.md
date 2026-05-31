# Index

Content catalog for this vault. Every wiki page is listed here under its category, with a one-line summary. Updated on every ingest.

> Conventions: see [[AGENTS]].

## Profile

- [[about-me]] — user profile and teaching preferences for the AI tutor

## Sources

- [[Bishop and Bishop - Deep Learning Foundations and Concepts]] — Springer 2024 textbook (656 pages): probability fundamentals, regression, classification, deep nets, transformers, generative models, RL; top deep-learning reference for the foundation thread.
- [[Constraint gradient perpendicular to tangent - Claude explanation]] — Self-contained AI explanation of why $\nabla h \perp$ tangent of $h(x)=0$, contributing the chain-rule proof now merged into the concept page.
- [[Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor]] — Heptabase AI Tutor lesson deriving Jacobian pseudoinverse formulas from optimization and KKT/Lagrange stationarity.
- [[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]] — Yang Song's blog: score-first treatment of diffusion (score matching → Langevin → NCSN → SDE → probability-flow ODE → Bayes-on-scores for inverse problems); explicit DDPM ↔ score-based unification.
- [[Integrated Learning and Planning - Mao]] — Stanford Robotics Seminar on neuro-symbolic concepts for data-efficient robot learning, planning, contact-rich manipulation, spatial reasoning, and closed-loop agents.
- [[Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al]] — Primary ACT/ALOHA paper introducing action chunking, temporal ensembling, and low-cost bimanual imitation learning.
- [[Modern Robotics - Lynch & Park]] — Lynch & Park textbook (Cambridge, 2017): geometric/PoE treatment of kinematics, dynamics, planning, control, grasping, and mobile robots; backbone of the foundation thread.
- [[Normalizing Flows Tutorial Part 1 - Eric Jang]] — Eric Jang's intuition-first NF tutorial: 1D → multivariate change of variables, Jacobian determinant as local volume distortion, TensorFlow `TransformedDistribution` / `Bijector` API, toy 2D MLP-bijector training example.
- [[Normalizing Flows Tutorial Part 2 - Eric Jang]] — Eric Jang's NF architecture menu: MAF (fast train / slow sample), IAF (fast sample / slow train), Real-NVP (fast both ways, less expressive), Parallel WaveNet (MAF teacher → IAF student distillation, deployed in Google Assistant), BatchNorm bijector.
- [[What are Diffusion Models - Lilian Weng]] — Lilian Weng's blog: DDPM-first survey of diffusion (forward kernel → ELBO → ε-loss → guidance → DDIM → distillation/consistency → LDM → unCLIP/Imagen → U-Net/ControlNet/DiT).

## Ingestion indices

- [[Bishop and Bishop - chapters]] — chapter-level status for the Bishop & Bishop *Deep Learning* (2024) textbook (20+ chapters; Ch 4 + Ch 5 covered).
- [[Modern Robotics - chapters]] — chapter-level status for the Modern Robotics textbook (13 chapters + 4 appendices).

## Entities

- [[Jiayuan Mao]] — Robotics and AI researcher focused on learning, reasoning, and planning with neuro-symbolic concepts grounded in perception and action.
- [[LeRobot]] — Hugging Face's open-source PyTorch library for robot learning, datasets, policies, hardware integration, and deployment.

## Concepts

- [[Action Chunking Transformer]] — Transformer-based imitation-learning policy that predicts chunks of future robot actions for smoother, shorter-horizon control.
- [[Basis Functions]] — Fixed feature functions $\phi_j(x)$ a linear-in-$w$ model sums over; the conceptual seed Ch 6 generalizes by *learning* the $\phi_j$ as hidden units. Piano-key analogy + the three standard families (polynomial / Gaussian / sigmoidal).
- [[Closed-Loop Robot Agents]] — Robot-agent systems that continuously observe, update memory, plan, execute skills, monitor progress, and replan across mismatched module rates.
- [[Composable Robot Skills]] — Learned short-horizon skills with arguments, trajectory samplers, and effect models that planners can recombine into longer tasks.
- [[Compositional Diffusion Constraint Solvers]] — Diffusion-style learned relation models composed as constraint energies or gradients for spatial arrangement and planning.
- [[Configuration Space]] — Robot's C-space: dof, Grübler's formula, joint types, topology, holonomic vs. nonholonomic constraints, and task space vs. workspace (from [[Modern Robotics - Lynch & Park]] Ch. 2).
- [[Constraint Satisfaction]] — Finding robot poses, trajectories, contacts, task orders, or object layouts that jointly satisfy geometric, dynamic, relational, and preference constraints.
- [[Constraint Gradients and Tangent Spaces]] — Geometric relation between equality-constraint gradients, tangent directions, normal spaces, and constrained stationarity.
- [[Cross-Entropy Loss]] — Negative log-likelihood under Bernoulli/multinomial targets; "surprise meter" analogy; binary + multi-class formulas; canonical-link pairing with sigmoid/softmax that gives the clean $(y-t)\phi$ gradient.
- [[Contact Analogy]] — One-shot manipulation transfer by matching functionally similar contact points or contact-mode sequences on novel objects, then verifying with planning and physics checks.
- [[Generalized Linear Models]] — The $y = f(w^T \phi(x))$ template (activation + link function); explains the canonical-link pairing rule (regression/MSE, binary/BCE+sigmoid, multi-class/CCE+softmax) that gives the clean $(y-t)\phi$ gradient and prevents vanishing-gradient training stalls.
- [[Imitation Learning]] — Training robot policies from demonstrations, usually the most practical first method for a self-researcher.
- [[Isaac Lab]] — NVIDIA's Python framework for robot simulation, training, and teleoperation on top of Isaac Sim and USD; the scripting layer underneath LeIsaac.
- [[Karush-Kuhn-Tucker Conditions]] — First-order constrained-optimization conditions generalizing Lagrange multipliers to equality and inequality constraints.
- [[Lagrange Multipliers]] — Equality-constraint optimization method with an ELI5 bridge, gradient-stationarity geometry, pseudoinverse/IK connection, and Socratic checks.
- [[Linear Regression]] — MLE under Gaussian noise → sum-of-squares loss; closed-form via [[Moore-Penrose Pseudoinverse]]; orthogonal-projection geometry; SGD/LMS; weight decay; bias-variance trade-off.
- [[Logistic Regression]] — Binary classifier with sigmoid output + cross-entropy loss; sigmoid derived as log-odds → probability; convex loss + clean $(y-t)\phi$ gradient; PyTorch `BCEWithLogitsLoss` idiom and the linearly-separable weight-blowup gotcha.
- [[Moore-Penrose Pseudoinverse]] — Generalized matrix inverse used for minimum-norm and least-squares Jacobian inverse kinematics.
- [[Neuro-Symbolic Concepts]] — Reusable robot knowledge units with symbolic interfaces and neural grounding for perception, language, geometry, action, and planning.
- [[Normalizing Constant]] — $Z = \int \tilde p(x)\,dx$ that turns "unnormalized shape" into a probability density; the cake-fraction analogy, why $Z_\theta$ is intractable for general neural-net energies, and why the score gradient makes it vanish.
- [[Numerical Inverse Kinematics]] — Newton-Raphson IK on SE(3): why the matrix logarithm produces the body-twist error vector, body Jacobian update, DLS near singularities (Modern Robotics §6.2.2).
- [[Robot Learning]] — Data-driven robotics methods that learn policies from rewards, demonstrations, or multimodal robot datasets.
- [[Robotics Development Stack]] — Layered map of robotics theory, hardware, middleware, simulation, data, learning, deployment, and safety.
- [[Sigmoid Function]] — Logistic squash $1/(1+e^{-x})$: smooth $\mathbb{R} \to (0,1)$ probability/gate, with the dimmer-switch analogy, log-odds derivation, vanishing-gradient pitfall, and canonical-link pairing with binary cross-entropy.
- [[Softmax]] — Normalized exponential $e^{a_k}/\sum_j e^{a_j}$ as the $K$-class log-odds → probability formula; multi-class generalization of sigmoid; canonical-link partner of categorical cross-entropy; denominator is a [[Normalizing Constant]]; PyTorch `CrossEntropyLoss` numerical-stability idiom.
- [[Singularity]] — Cross-domain concept linking linear-algebra rank loss, geometric tangent failures, coordinate singularities, and robotics Jacobian singularities.
- [[Task and Motion Planning]] — Jointly deciding symbolic robot actions and continuous feasible motions, poses, grasps, and trajectories.
- [[Training Environments and the Gymnasium API]] — Two-layer view of sim-based training: physics engine (MuJoCo / Isaac Sim / Genesis) vs. Gymnasium API contract; when a Gym env is required for RL training but unnecessary for ACT/DP training.
- [[Vision-Language-Action Models]] — Robot policies that condition on vision and language and output actions for physical control.
- [[VR Teleoperation in Simulation]] — VR-headset teleop pipeline for collecting LeRobot-format demos in sim: OpenXR, retargeting, IK, dataset writer; LeIsaac vs. scaffolding from scratch.

## Syntheses

- [[Diffusion Crash Course - synthesis]] — Weekend (~12–16h) curriculum to acquire the diffusion-models map: probability fundamentals → score matching → DDPM derivation → modern variations (DDIM/CFG/LDM/DiT) → Diffusion Policy; with textbook chapters, papers, and a depth-dive matrix for after the weekend.
- [[LeRobot Documentation Index]] — Searchable local map of the official LeRobot docs and a recommended reading path.
- [[Modern Robotics Development - synthesis]] — Whole-picture overview of modern robotics development, core tools, and realistic self-researcher paths.
- [[learning-tracker]] — curriculum, coverage map, recommendations, session log (agent-maintained)

## Journal

_None yet. Personal entries (`domain: personal`)._
