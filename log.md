# Log

Chronological record of vault activity. Append-only. Each entry: `## [YYYY-MM-DD] {op} | {subject}`.

`grep "^## \[" log.md | tail -10` shows the most recent activity.

---

## [2026-05-09] init | vault scaffolded

Created `AGENTS.md`, `index.md`, `log.md`, and the `raw/` and `wiki/` directory tree (`sources/`, `entities/`, `concepts/`, `syntheses/`, `journal/`). Vault is ready for first ingest.

## [2026-05-13] query | modern robotics and LeRobot study map

Created initial robotics knowledge cluster:

- `wiki/entities/LeRobot.md`
- `wiki/concepts/Robot Learning.md`
- `wiki/concepts/Imitation Learning.md`
- `wiki/concepts/Vision-Language-Action Models.md`
- `wiki/concepts/Robotics Development Stack.md`
- `wiki/syntheses/LeRobot Documentation Index.md`
- `wiki/syntheses/Modern Robotics Development - synthesis.md`

Updated `index.md` so the new pages are discoverable.

## [2026-05-14] maintenance | renamed vault to EmbodiedAILab

Updated `AGENTS.md` to describe the vault as a focused embodied AI and modern robotics research wiki instead of a general-purpose second brain. Renamed the vault folder from `llm-wiki` to `EmbodiedAILab`.

## [2026-05-14] query | ACT teaching note

Created a focused ACT knowledge cluster and saved local raw web-source snapshots:

- `raw/act-paper-arxiv-snapshot.md`
- `raw/act-lerobot-docs-snapshot.md`
- `raw/act-aloha-project-snapshot.md`
- `wiki/sources/Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware - Zhao et al.md`
- `wiki/concepts/Action Chunking Transformer.md`

Updated cross-links in `wiki/concepts/Imitation Learning.md`, `wiki/entities/LeRobot.md`, `wiki/syntheses/LeRobot Documentation Index.md`, `wiki/syntheses/Modern Robotics Development - synthesis.md`, `wiki/concepts/Vision-Language-Action Models.md`, and `index.md`.

## [2026-05-14] query | KKT, Lagrange multipliers, and pseudoinverse

Read the Heptabase AI Tutor lesson card `Deriving the Pseudoinverse: Where the Formulas Come From` through the Heptabase CLI and saved compact local source snapshots:

- `raw/heptabase-deriving-pseudoinverse-kkt-snapshot.md`
- `raw/kkt-boyd-vandenberghe-snapshot.md`
- `wiki/sources/Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor.md`
- `wiki/concepts/Karush-Kuhn-Tucker Conditions.md`
- `wiki/concepts/Lagrange Multipliers.md`
- `wiki/concepts/Moore-Penrose Pseudoinverse.md`

Updated `wiki/concepts/Robotics Development Stack.md` and `index.md` with the new optimization-math concepts.

## [2026-05-14] maintenance | Obsidian LaTeX formatting

Converted math notation in the KKT, Lagrange multipliers, pseudoinverse, and Heptabase source wiki pages from code-style formatting and `math` fences to Obsidian-supported `$...$` and `$$...$$` LaTeX syntax. Left `raw/` source snapshots unchanged per vault immutability rules.

## [2026-05-14] query | expanded KKT and pseudoinverse derivations

Expanded the teaching notes for:

- `wiki/concepts/Karush-Kuhn-Tucker Conditions.md`
- `wiki/concepts/Lagrange Multipliers.md`
- `wiki/concepts/Moore-Penrose Pseudoinverse.md`
- `wiki/sources/Deriving the Pseudoinverse Where the Formulas Come From - Heptabase AI Tutor.md`

Added step-by-step derivations, geometric intuition, a small constrained-optimization example, row-space/null-space interpretation, SVD unification, and Mecharm-specific inverse-kinematics interpretation.

## [2026-05-15] query | Lagrange multipliers geometric figures

Added visual explanations of the geometric intuition behind Lagrange multipliers:

- `wiki/concepts/Lagrange Multipliers.md`
- `wiki/assets/lagrange-line-contour-tangency.svg`
- `wiki/assets/lagrange-tangent-component-before-optimum.svg`
- `wiki/assets/lagrange-stationarity-at-optimum.svg`

Updated `index.md` to note that the concept page now includes stationarity figures.

## [2026-05-15] query | Lagrange multipliers tangent and normal figures

Added two targeted figures to the geometric-intuition section:

- `wiki/assets/lagrange-feasible-surface-no-tangent-improvement.svg`
- `wiki/assets/lagrange-objective-and-constraint-gradients-parallel.svg`

These figures illustrate why feasible motion is tangent to $h(x)=0$ and why $\nabla f(x^\star)$ and $\nabla h(x^\star)$ are parallel normals at a constrained optimum.

## [2026-05-15] query | constraint gradients and tangent spaces

Created a durable concept page for the relation between equality-constraint gradients and tangent lines/planes:

- `wiki/concepts/Constraint Gradients and Tangent Spaces.md`
- `wiki/concepts/Lagrange Multipliers.md`

Updated `index.md` so the concept is discoverable.

## [2026-05-16] create | wiki/about-me.md — AI tutor profile per design spec

Created the user profile document with frontmatter (role, goals, horizon, learning preferences, constraints) and narrative sections: who I am, where I'm going, solid ground vs. active gaps, how I learn best (everyday analogies, tracking, project mode, Socratic follow-up), current projects, constraints, and pointers.

Updated `index.md` with a new Profile section linking to `[[about-me]]`.

## [2026-05-16] create | wiki/syntheses/learning-tracker.md — bootstrapped from existing wiki coverage

Created the learning tracker synthesis document with:

- Active focus (foundation thread: optimization math)
- Recommendations (ranked per user preference: Modern Robotics → ACT → Diffusion Policy, with Sutton & Barto as reference)
- Coverage map (concepts covered with mastery signal, resource progress table)
- Gaps detected (agent-maintained list of missing prerequisites)
- Session log (append-only entry point for tutor workflow records)

Reflects existing wiki concepts: Lagrange Multipliers, KKT, Constraint Gradients, ACT. Updated `index.md` to list tracker in Syntheses section.

## [2026-05-16] modify | AGENTS.md — added Tutor Mode, trigger phrases, ingestion-index page type, extended source frontmatter

## [2026-05-16] create | .claude/skills/tutor/SKILL.md — /tutor slash command for vault-scoped tutor mode

## [2026-05-16] ingest | Modern Robotics - Lynch & Park (textbook)

Ingested the Modern Robotics PDF (`raw/ModernRobotics-v2.pdf`, 644 pages,
Dec 2019 preprint of Cambridge 2017 first edition). Tutor-mode `ingest`
workflow:

- `wiki/sources/Modern Robotics - Lynch & Park.md` — source page with
  extended frontmatter (`source_format: pdf`, `total_pages: 644`,
  `study_status: in-progress`, `chunks_indexed: false`), per-chapter key
  claims, and a recommended reading path anchored to the foundation
  thread.
- `wiki/ingestion/Modern Robotics - chapters.md` — chapter-level index
  (13 chapters + appendices A–D) with planned concept pages per chapter
  and status column. Ch. 3 marked `next`; App. D marked `covered`
  because the optimization-math thread already produced the relevant
  pages from other sources.
- `wiki/syntheses/learning-tracker.md` — flipped Modern Robotics
  resource progress from `queued` to `in-progress (ingested)`, added
  pointer to the chapter index, refreshed the active focus and session
  log.
- `index.md` — added the source under Sources and a new "Ingestion
  indices" section linking the chapter index.

## [2026-05-16] study | Modern Robotics Ch. 2 (Configuration Space)

Tutor-mode `study Chapter 2 of Modern Robotics` workflow. Read printed
pp. 11–56 (PDF pp. 32–60) of `raw/ModernRobotics-v2.pdf`.

- `wiki/concepts/Configuration Space.md` — new concept page with
  house-address everyday analogy and explicit breakdown; covers dof
  definition, Grübler's formula with joint cheat sheet and sanity
  checks, topology ($\mathbb{R}^n$, $S^n$, $T^n$, cylinder), why
  topology matters (representation singularities, atlas vs. implicit
  representations), holonomic vs. nonholonomic constraints with the
  rolling-coin integrability test, and task-space vs. workspace vs.
  C-space distinction. Embedded inline SVG of a 2R planar arm and its
  torus C-space.
- `wiki/concepts/Constraint Gradients and Tangent Spaces.md` —
  extended with "Connection to robotics: holonomic constraints"
  section bridging the optimization-math view to the C-space view via
  the loop-closure-equation Jacobian.
- `wiki/ingestion/Modern Robotics - chapters.md` — Ch. 2 row flipped
  to `covered`; added `last_chapter_studied: 2` to frontmatter.
- `wiki/syntheses/learning-tracker.md` — added Configuration Space to
  coverage map (building); refreshed active focus; appended session
  log entry; noted manifolds/topology basics in Gaps detected.
- `index.md` — added Configuration Space under Concepts.

## [2026-05-16] ingest | Constraint gradient perpendicular to tangent - Claude explanation

Ingested `raw/Explain Why Constraint gradient is perpendicular to Tangent of h(x)=0.md`
— a short AI-generated explanation the user added. The valuable new
content is the **chain-rule proof** of $\nabla h \perp$ tangent
(differentiating $h(\gamma(t)) = 0$ along an arbitrary feasible
curve), which complements the existing first-order Taylor argument.

- `wiki/sources/Constraint gradient perpendicular to tangent - Claude explanation.md`
  — new source page with extended frontmatter, Summary, Key claims,
  Notable quotes, Connections, Open questions.
- `wiki/concepts/Constraint Gradients and Tangent Spaces.md` —
  restructured "Why the gradient is normal" into two parallel
  arguments (Taylor + chain rule), with a closing paragraph on why
  both finish via the same "arbitrary" step. Added a Sources section
  and a `sources:` frontmatter list.
- `index.md` — added source under Sources.

## [2026-05-16] query | /tutor explain the sigmoid function

Tutor-mode end-to-end run validating the formula-driven visual path
(matplotlib convention) and the everyday-analogy + bridges protocol.

- `wiki/assets/sigmoid/sigmoid.py` — small numpy + matplotlib script
  producing the plot. Runs via `cd wiki/assets/sigmoid && python3 sigmoid.py`;
  saves `sigmoid.png` next to itself (relative path per convention).
- `wiki/assets/sigmoid/sigmoid.png` — generated plot: sigmoid curve,
  its derivative, σ(0)=½ marked, saturation labels at ±8.
- `wiki/concepts/Sigmoid Function.md` — new concept page with
  dimmer-switch analogy and explicit breakdown (linear dial vs.
  saturating sigmoid → foreshadows vanishing gradients), embedded PNG,
  closed-form derivative, symmetry, $\tanh$ relation, practical
  pitfalls (vanishing gradients, overflow, BCE-with-logits), and
  context for ACT / VLA models.
- `wiki/syntheses/learning-tracker.md` — added Sigmoid Function to
  coverage map (working); appended session log.
- `index.md` — added Sigmoid Function under Concepts.

## [2026-05-17] query | vanishing correction in constraint tangent spaces

Clarified the phrase "vanishing correction" inside the existing
[[Constraint Gradients and Tangent Spaces]] concept page.

- `wiki/concepts/Constraint Gradients and Tangent Spaces.md` —
  added a unit-circle example showing that a tangent step from
  $(1,0)$ to $(1,\epsilon)$ violates $h(x,y)=x^2+y^2-1=0$ by
  $\epsilon^2$, so the exact projection back to the constraint needs
  only a higher-order inward correction.
- `wiki/syntheses/learning-tracker.md` — bumped the concept's last
  studied date and appended the tutor session note.

## [2026-05-24] query | Genesis physics simulator — deep web research

Tutor-mode deep-research workflow to capture raw materials on the Genesis
(`genesis-world` / Genesis-Embodied-AI) physics simulator. Extends the
existing Genesis-vs-Isaac evaluation thread.

- `raw/genesis-world-research-snapshot.md` — new 333-line raw-materials
  capture with frontmatter; covers what Genesis is, the headline speed
  claims and their independent pushback (Stone Tao / ManiSkill, MuJoCo
  team), v0.4.7 architecture (in-house Quadrants compiler since v0.4.0),
  generative-framework status (still closed, spun out to Genesis AI;
  $105M seed July 2025; GENE-26.5 robotics foundation model May 2026),
  VR/teleop status (confirmed no first-party support, issue #1626),
  comparison table vs Isaac Lab / MuJoCo MJX / Brax / SAPIEN, adoption
  signals, known limitations, and a numbered references list. No wiki
  pages yet — ingestion deferred until user runs `ingest`.

Headline correction: the "43M FPS / 10–80× faster" claim collapsed ~150×
under realistic settings in Stone Tao's independent benchmark; Genesis
is at parity with Isaac Lab on locomotion and 3–10× slower than
ManiSkill on manipulation. Real differentiator is multi-physics breadth
(rigid + MPM + SPH + FEM + PBD + Stable Fluid in one engine), not
throughput.

## [2026-05-17] query | singularity across domains

Created a cross-domain concept page explaining how "singularity" is used
in linear algebra, geometry, coordinate representations, and robotics.

- `wiki/concepts/Singularity.md` — new concept page with analogy,
  domain comparison table, examples, robotics Jacobian interpretation,
  and distinctions between geometric vs. representation singularities.
- `wiki/concepts/Constraint Gradients and Tangent Spaces.md` —
  linked feasible-set singularities to [[Singularity]].
- `wiki/concepts/Configuration Space.md` — linked representation
  singularities to [[Singularity]].
- `wiki/concepts/Moore-Penrose Pseudoinverse.md` — linked
  near-singular Jacobian behavior to [[Singularity]].
- `index.md` — added [[Singularity]] under Concepts.
- `wiki/syntheses/learning-tracker.md` — added [[Singularity]] to the
  coverage map and appended the tutor session note.

## [2026-05-25] query | revise Lagrange Multipliers for tutor rules

Updated the existing concept page to match the current tutor-mode explanation pattern.

- `wiki/concepts/Lagrange Multipliers.md` — added ELI5 framing, everyday painted-path analogy with explicit breakdown, tightened stationarity geometry, preserved existing diagrams, reframed the pseudoinverse example as the robotics connection, added origins/variations sections, and closed with Socratic-check questions.
- `wiki/syntheses/learning-tracker.md` — updated the concept's last-studied date and appended the tutor session note.
- `index.md` — refreshed the one-line concept summary.

Follow-up correction: revised the same concept page to replace misleading "push back" phrasing with "balance" phrasing, and explicitly distinguished $h(x)=0$ as the constraint, $\nabla h(x)$ as the constraint normal, and $\lambda \nabla h(x)$ as the stationarity balancing term.

## [2026-05-27] ingest | Integrated Learning and Planning

Ingested Jiayuan Mao's Stanford Robotics Seminar on integrated learning and planning with neuro-symbolic concepts.

- `raw/stanford-robotics-seminar-integrated-learning-and-planning.md` — raw manifest created for the YouTube seminar, auto-caption transcript, and downloaded reference PDFs.
- `raw/assets/stanford-robotics-seminar-integrated-learning-and-planning-3W36pd50Wqw.en.vtt` — YouTube auto-caption transcript.
- `raw/assets/papers/2025-arxiv-neuro-symbolic-concepts.pdf` — local reference PDF.
- `raw/assets/papers/2022-neurips-pdsketch-integrated-domain-programming-learning-and-planning.pdf` — local reference PDF.
- `raw/assets/papers/2025-icra-magic-one-shot-manipulation-contact-analogies.pdf` — local reference PDF.
- `raw/assets/papers/2024-rss-set-it-up-functional-object-arrangement-compositional-generative-models.pdf` — local reference PDF.
- `raw/assets/papers/2023-corl-learning-reusable-manipulation-strategies.pdf` — local reference PDF.
- `raw/assets/papers/2026-icra-stack-learning-composable-skills.pdf` — local reference PDF.
- `raw/assets/papers/2026-retriever-programming-closed-loop-modular-robot-agent.pdf` — local reference PDF.
- `wiki/sources/Integrated Learning and Planning - Mao.md` — new source page summarizing the seminar and linking the local reference papers.
- `wiki/entities/Jiayuan Mao.md` — new entity page.
- `wiki/concepts/Neuro-Symbolic Concepts.md` — new concept page.
- `wiki/concepts/Task and Motion Planning.md` — new concept page.
- `wiki/concepts/Constraint Satisfaction.md` — new concept page connecting the seminar to existing optimization pages.
- `wiki/concepts/Contact Analogy.md` — new concept page for one-shot contact-based manipulation transfer.
- `wiki/concepts/Compositional Diffusion Constraint Solvers.md` — new concept page for SetItUp-style spatial-relation composition.
- `wiki/concepts/Composable Robot Skills.md` — new concept page for STACK-style learned skill samplers and effect models.
- `wiki/concepts/Closed-Loop Robot Agents.md` — new concept page for Retriever-style multi-rate agent systems.
- `wiki/concepts/Robot Learning.md`, `wiki/concepts/Imitation Learning.md`, `wiki/concepts/Vision-Language-Action Models.md`, `wiki/concepts/Training Environments and the Gymnasium API.md` — updated with cross-links to the seminar thread.
- `wiki/syntheses/learning-tracker.md` — added coverage rows, resource progress, gaps, and recommendation update.
- `index.md` — added new source, entity, and concept pages.

Main knowledge change: this seminar reframes the user's IL/VLA path as part of a larger structured robot-learning stack where foundation models provide perception/language structure, while planning, constraints, learned skill effects, and closed-loop systems engineering remain explicit.

## [2026-05-28] query | /tutor — why the matrix log appears in Modern Robotics §6.2.2 numerical IK

Tutor-mode explainer triggered by the user reading ahead from the queued Ch. 3 thread into Ch. 6.2.2 (Numerical Inverse Kinematics Algorithm). User asked specifically why the body twist $\mathcal{V}_b$ is determined via the matrix logarithm in the SE(3) extension of the iteration.

- `wiki/concepts/Numerical Inverse Kinematics.md` — new concept page. ELI5 + everyday analogy (globe + tangent arrow ≡ log map) with explicit breakdown (Chasles' screw structure; SE(3) log ambiguity near $\pi$-rotations as the sphere-antipode analog). Side-by-side derivation: simplified Newton-Raphson with $e = x_d - f(\theta) \in \mathbb{R}^m$ → SE(3) version with $T_{bd} = T_{sb}^{-1}T_{sd} \to \log \to \mathcal{V}_b \in \mathbb{R}^6$. Explicit "why body twist matches the body Jacobian" framing; full update $\theta^{i+1} = \theta^i + J_b^\dagger \log(T_{sb}^{-1}T_{sd})$; DLS callout linking to [[Singularity]]; common-confusions block (incl. the "$\log$ of a $4\times4$ → why a 6-vector" Lie-algebra-dimension question). Visuals: Mermaid side-by-side flow + inline SVG of sphere with great-circle and tangent arrow representing the log map. Three Socratic questions posed at the bottom.
- `wiki/ingestion/Modern Robotics - chapters.md` — Ch. 6 row flipped from `queued` to `partial` with a §6.2.2 note; added `partial` to the status legend.
- `wiki/syntheses/learning-tracker.md` — added Numerical Inverse Kinematics to coverage map (`building`); refreshed the "Inverse kinematics methods" gap-detected entry to record partial coverage; appended session log entry.
- `index.md` — added [[Numerical Inverse Kinematics]] under Concepts.

Curriculum note: Ch. 3 ([[Twist]], [[Exponential Coordinates of Rigid-Body Motion]]) and Ch. 5 ([[Body Jacobian]]) remain the rigorous prerequisites for the matrix-log derivation; this page covers enough for the user to follow §6.2.2 without first finishing Ch. 3, but Ch. 3 is still the recommended next chapter under [[learning-tracker]].

## [2026-05-28] query | /tutor — Socratic follow-up on numerical IK

User answered the three Socratic questions on [[Numerical Inverse Kinematics]]:

1. *Why direct $T_{sd} - T_{sb}$ fails* — correct on the main point (SE(3) not a vector space, $R^TR=I$ destroyed). Asked for clarification on "units and frames wouldn't match": concrete explanation given (mixed-units 12-vector, unit-dependent pseudoinverse step, no natural frame on $R - R'$, contrasted with twist's frame-consistent body-Jacobian mapping).
2. *Where the 6-vector comes from* — got angular R³ + linear R³ = R⁶, but the deeper question they raised was why the log produces $[\mathcal{V}]$ rather than $[\mathcal{S}]\theta$. Clarified that these are the **same matrix** in two factorings: Ch. 3 PoE uses normalized $\mathcal{S}$ + scalar magnitude $\theta$ because each joint has a fixed screw axis and a variable joint coordinate; §6.2.2 uses the lumped $\mathcal{V}_b$ because the IK iteration just needs a tangent-space error vector. Also noted the convergence-test caveat ($\|\mathcal{V}_b\|$ goes to zero, but $\mathcal{S} = \mathcal{V}_b/\theta$ can swing wildly).
3. *Space twist equivalence* — correct intuition; gave the explicit formula $[\mathcal{V}_s] = \log(T_{sd}\,T_{sb}^{-1})$, $\theta^{i+1} = \theta^i + J_s^\dagger\,\mathcal{V}_s$, with the adjoint equivalence $J_s = \mathrm{Ad}_{T_{sb}} J_b$.

- `wiki/concepts/Numerical Inverse Kinematics.md` — added the $[\mathcal{V}]$ vs $[\mathcal{S}]\theta$ clarification to Common Confusions (with the convergence-test caveat), and a new "Space-frame equivalent (via adjoint)" section after the body-frame derivation.
- `wiki/syntheses/learning-tracker.md` — appended session log entry recording the Socratic outcome and the refinement.

## [2026-05-28] query | /tutor — three uses of $\theta$ in Modern Robotics

User remembered "$\mathcal{V} = \mathcal{S}\dot\theta$" (from Ch. 5 velocity kinematics) and asked whether IK needed $\dot\theta$ to recover the twist from the screw axis. The underlying intuition (unit screw × scalar = full twist) was correct, but Modern Robotics overloads "$\theta$" in three roles and the IK context uses the magnitude-not-rate variant.

Distinguished:
1. **Magnitude $\theta$ (scalar)** — exp-coord scalar, units radians or meters, in $T = e^{[\mathcal{S}]\theta}$ and matrix-log output. *This is the one §6.2.2 uses.*
2. **Joint rate $\dot\theta$ (scalar)** — rate along one screw axis, units rad/s or m/s, in Ch. 5 single-joint velocity formula $\mathcal{V} = \mathcal{S}\dot\theta$.
3. **Joint vector / joint-rate vector $\theta, \dot\theta \in \mathbb{R}^n$** — whole-arm coordinates, in $T_{sb}(\theta)$ and $\mathcal{V}_b = J_b\dot\theta$.

The two scalar contexts reconcile via $\int_0^1 \mathcal{S}\dot\theta\,dt = \mathcal{S}\theta(1)$ — rate × unit duration = magnitude, which is why MR's "apply $\mathcal{V}$ for unit time" convention is internally consistent.

- `wiki/concepts/Numerical Inverse Kinematics.md` — added a new Common Confusions entry untangling the three $\theta$ roles with a small table-style breakdown and the reconciling integral.
- `wiki/syntheses/learning-tracker.md` — appended session log entry.

## [2026-05-28] query | /tutor — Example 6.1 walkthrough: why $v_{xb}$ is positive at iteration 0

User studying Modern Robotics Example 6.1 (planar 2R, p. 229–230) noticed that the printed iteration-0 table reports $v_{xb} = +0.498$ even though the goal origin in body coords is at $(-0.866, +1.5)$, i.e. in the $-\hat{x}_b$ direction. Asked for an unpacking of Lynch & Park's one-sentence resolution ("the constant body velocity that takes the initial guess to {goal} in one second is a rotation about the screw axis").

Resolution: $v_b$ is not a displacement vector — it is the tangent to a screw-motion arc at $t=0$. The ICR (instantaneous center of rotation, same as the planar screw axis) sits at $(-v_{yb}/\omega_{zb}, v_{xb}/\omega_{zb}) = (-1.183, 0.317)$ in body coords, *behind and slightly above* the EE. CCW rotation about that point gives a forward-and-up tangent at the body origin — hence $v_{xb} > 0$. Reproduced the textbook numbers exactly via $\omega_z \hat z \times \vec r$.

Everyday analogy: a satellite in orbit has velocity always tangent to its orbit, never toward the planet center or the destination point on the orbit. Breakdown: gravity sets orbit curvature, whereas the screw arc curvature here is set by the rotation magnitude $\omega_{zb}$ and where the goal pose lies.

- `wiki/concepts/Numerical Inverse Kinematics.md` — new "Worked example — Example 6.1: why $v_{xb} > 0$ at iteration 0" section with the body-frame coordinate table, ICR derivation, tangent calculation matching the textbook numbers, embedded matplotlib figure, satellite analogy with breakdown, decoded textbook quote, and the pure-translation degenerate case ($\omega_b = 0$ → $v_b$ equals straight-line displacement).
- `wiki/assets/numerical-ik/example-6-1-screw-axis.py` and `.png` — matplotlib script and rendered figure showing body origin, goal origin, ICR, the arc trajectory, the $v_b$ tangent arrow, and the naive straight-line displacement line for contrast (rendered with `genesis_env` Python, which has matplotlib 3.10.9; base `miniforge3` does not).
- `wiki/syntheses/learning-tracker.md` — appended session log entry.

Also captured a feedback memory at `/home/hayman/.claude/projects/-home-hayman-Workspace-EmbodiedAILab/memory/feedback_mermaid_short_labels.md` (indexed in `MEMORY.md`): Mermaid block labels should be short plain text; put formulas in display-math blocks outside the diagram. Reason: long math-in-label nodes overflow horizontally and become unreadable. This caused the user to rewrite the "Side-by-side flow" section of [[Numerical Inverse Kinematics]] manually after the original tutor commit; the rule is now persisted.

## [2026-05-28] query | /tutor — Example 6.1 frame-convention follow-up

User followed up on the Example 6.1 walkthrough: they had been assuming $\mathcal{V}_b$ was expressed in the base/space frame, so when they applied the body-frame ICR formula $\text{ICR}_b = (-v_{yb}/\omega_{zb}, v_{xb}/\omega_{zb}) = (-1.183, 0.317)$ and plotted the result on a space-frame diagram, it landed on the wrong side of the robot and didn't match the screw axis drawn in Fig. 6.8.

Root cause: the subscript $b$ in MR's $\mathcal{V}_b = (\omega_b, v_b)$ does double duty — it identifies the body twist (as opposed to the space twist $\mathcal{V}_s$) *and* says the components are expressed in body-frame coordinates ($\hat{x}_b, \hat{y}_b, \hat{z}_b$), not space-frame coordinates. At $\theta^0 = (0°, 30°)$, the body frame is rotated $30°$ from the space frame, so body-frame numbers can't be plotted on a space-frame diagram without first transforming.

Resolution: the ICR is one physical point with two coordinate descriptions — space coords $(0.683, 0.184)$ vs. body coords $(-1.183, 0.317)$ at $\theta^0$. The transformation $\text{ICR}_s = p_{sb} + r_x \hat{x}_b^{(s)} + r_y \hat{y}_b^{(s)}$ reconciles them. Alternative route: compute $\mathcal{V}_s = \mathrm{Ad}_{T_{sb}}\mathcal{V}_b = (1.571, 0.288, -1.073)$ via adjoint and apply the ICR formula to *that*; same physical ICR comes out in space coords directly.

- `wiki/concepts/Numerical Inverse Kinematics.md` — added three subsections to the worked example: "Frame convention reminder" (subscript $b$ does double duty, body axes in space coords at $\theta^0$), "Same physical scene in two frames" (with table of ICR in both coordinate descriptions and the transformation that reconciles them, plus a common-pitfall callout), and "If you'd rather work entirely in the space frame" (deriving $\mathcal{V}_s$ via adjoint and confirming ICR location).
- `wiki/assets/numerical-ik/example-6-1-frames.py` and `.png` — new dual-panel matplotlib figure. Left panel: physical space-frame view with the 2R arm at $\theta^0$, the body frame $\{b\}$ drawn at the EE (axes rotated $30°$), the goal pose, the ICR at space coords $(0.683, 0.184)$, the arc, and the $v_b$ direction arrow in space coords. Right panel: body-frame view of the same scene with body origin at $(0,0)$, goal at $(-0.866, 1.5)$, ICR at $(-1.183, 0.317)$, and $v_b = (0.498, 1.858)$ now coordinate-aligned with the axes. Caption emphasizes ICR is one physical point with two descriptions.
- `wiki/syntheses/learning-tracker.md` — appended session log entry.

## [2026-05-28] query | /tutor — Example 6.1 ICR sign-error follow-up

User shared a photo of their manual derivation. They started from $\vec v = \vec\omega \times \vec r$, expanded the cross product correctly, and got $\vec r = (+1.183, -0.317)$ — the **negative** of the ICR position. Not a calc error: a setup error. The equation $\vec v = \vec\omega \times \vec r$ assumes the *origin* is fixed and $\vec r$ is the position of a moving point. In the IK problem the body origin is itself moving (with velocity $\vec v_b$) and the ICR is what's fixed, so the correct relation is $\vec v_b = -\vec\omega \times \vec p_{\text{ICR}}$. Their $\vec r$ has a valid alternative interpretation: it's the radial vector from the ICR to the body origin ($\vec r = \text{body origin} - \vec p_{\text{ICR}}$), so $\vec p_{\text{ICR}} = -\vec r$ recovers $(-1.183, 0.317)$.

- `wiki/concepts/Numerical Inverse Kinematics.md` — added "Pitfall: deriving the ICR from $\vec v = \vec\omega \times \vec r$ gives the wrong sign" subsection with the correct setup, the expansion that produces $\vec p_{\text{ICR}}$ directly without a sign flip, and the "your $\vec r$ is the radial-from-ICR" alternative interpretation.
- `wiki/syntheses/learning-tracker.md` — appended session log entry.

## [2026-05-28] query | /tutor — weave task-space-guidance reading into Numerical IK page

User articulated a unifying reading of the IK iteration: "$e^{[\mathcal{V}_b]}$ / $e^{[\mathcal{V}_s]}$ is the guidance for the transition from current pose (from FK) to desired pose; the body twist represents the rate and direction that guides the EE toward the target." Affirmed with one refinement — the body twist is *task-space* guidance (describes EE motion, not joint angles), and the Jacobian pseudoinverse $J_b^\dagger$ is what translates that task-space guidance into the joint-space correction $\Delta\theta$.

Wove the framing into [[Numerical Inverse Kinematics]]:

- Added "Reading angle" callout to the opening tagline naming the *task-space guidance signal → joint-space correction* chain.
- Expanded ELI5 to call the globe arrow a "guidance signal."
- Added a "Guidance reading" bullet under "The fix — matrix log gives you the body twist."
- Rewrote the "Why body twist, not space twist" intro to lead with "EE-centered guidance" vs space twist as "world-fixed-observer's view of the same guidance"; emphasized $J_b^\dagger$ as the "translator" from task-space guidance to joint-space correction.
- Annotated the boxed update equation with `translator` and `task-space guidance` underbraces.
- Updated the second flow-chart node label "body-twist error" → "body-twist guidance" and added underbraces to the post-flow equations.
- Added a "guidance signal interpretation" bullet to "Connection to current learning thread" tying Whitney's resolved motion rate control and Isaac Lab/cuRobo teleop IK to the same task-space-guidance → joint-space-correction chain (real-time vs iterative streaming of the same translation).

## [2026-05-30] ingest | What are Diffusion Models? (Lilian Weng) + Generative Modeling by Estimating Gradients of the Data Distribution (Yang Song)

Batch-ingested both canonical secondary diffusion surveys in one session per user request. The two pieces are deliberately complementary — Weng's is DDPM-first, Song's is score-first, and Song's piece explicitly bridges them ("wave mechanics and matrix mechanics in quantum mechanics"). Both back the existing [[Diffusion Models]] concept page with no contradictions; the page already covered ε-loss, the score identity $s_\theta = -\epsilon_\theta/\sqrt{1-\bar\alpha_t}$, score additivity, and the DDPM-vs-score-vs-SDE umbrella distinction.

- `wiki/sources/What are Diffusion Models - Lilian Weng.md` — new source page with extended frontmatter (`source_format: web`, `study_status: covered`), Summary covering the DDPM derivation spine through DDIM / progressive distillation / consistency models / LDM / cascaded SR / unCLIP / Imagen / U-Net / ControlNet / DiT, ~20 key claims, four notable quotes, Connections, and Open questions (NCSN-bridge exactness, DDIM-vs-consistency-models for Diffusion Policy, dynamic-thresholding-for-actions, ControlNet-style embodiment adaptation).
- `wiki/sources/Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song.md` — new source page with extended frontmatter, Summary covering score function → Langevin → NCSN → annealed Langevin → SDE generalization (VE/VP/sub-VP) → probability-flow ODE → Bayes-on-scores for inverse problems → DDPM unification, ~15 key claims, five notable quotes including the wave-mechanics quote, Connections, and Open questions (which SDE family Diffusion Policy uses, probability-flow ODE for OOD detection in deployment, Bayes-on-scores in closed-loop control, discrete-data handling in 2026).
- `wiki/concepts/Diffusion Models.md` — added `sources:` frontmatter pointing to both new source pages; bumped `updated:` to 2026-05-30; extended the "DDPM vs. score-based SDE vs. diffusion" common-confusion entry with Song's wave/matrix-mechanics unification quote and the explicit $\epsilon_\theta \leftrightarrow s_\theta$ scalar relationship; reorganized "Origins / sources" into a Primary papers list (adding Progressive Distillation, Consistency Models, LDM, DiT to the existing references) plus a new "Canonical secondary surveys" subsection citing both blogs with one-line "what each is the reference for" descriptions; replaced the placeholder Mentions block with inbound entries for both source pages.
- `index.md` — added both source pages under Sources with one-line summaries.
- `wiki/syntheses/learning-tracker.md` — bumped [[Diffusion Models]] last-studied date to 2026-05-30 (mastery still `building` — Socratic check from 2026-05-27 remains unanswered); added a Resource progress row for both blogs; appended this session log entry.

Mastery position: the user's [[Diffusion Models]] page was already well-developed before this ingest (built from /tutor explain on 2026-05-27); these two sources back it canonically and add depth without forcing a rewrite. The genuine knowledge addition is the explicit DDPM ↔ score-based unification framing (Song's "wave/matrix mechanics" quote), which sharpens the existing common-confusion entry from "they converge to the same algorithms" to "they are formally the same loss in two parameterizations." Diffusion Policy deep-read is now even better-prepared — every design choice in Chi et al. 2023 (cosine schedule, DDIM sampler, ε-prediction, U-Net-1D-conv, CFG) sits on a menu Weng catalogs and Song unifies.

## [2026-05-30] query | /tutor — what is "a tractable normalizing constant"?

User reading Yang Song's blog ([[Generative Modeling by Estimating Gradients of the Data Distribution - Yang Song]]) asked what "a tractable normalizing constant" means. Created a standalone concept page; this is foundational ML theory that comes up everywhere (EBMs, Bayesian inference, softmax, statistical physics) so it earned its own page rather than being folded into [[Diffusion Models]].

- `wiki/concepts/Normalizing Constant.md` — new concept page. ELI5 cake-fraction analogy with breakdown (continuous high-dim integral vs. discrete weighable cake; well-defined ≠ computable). Sand-grains-on-Earth analogy for the intractable-denominator point. Formal definition $Z = \int \tilde p(x)\,dx$ with the Boltzmann form $p_\theta(x) = e^{-f_\theta(x)}/Z_\theta$. Inline SVG comparing "unnormalized shape: area = $Z_\theta$" vs "normalized density: area = 1" side-by-side with a `÷ Z_θ` arrow between. Explicit "tractable = computable in reasonable time" definition with the 256×256 image / $\mathbb{R}^{196608}$ example. Six-row escape-routes table (autoregressive, normalizing flows, VAEs, EBMs, GANs, diffusion) framing all of generative modeling as "tractability strategies." Worked derivation of the score-vanishing trick: $\nabla_x \log Z_\theta = 0$ because $Z_\theta$ has $x$ integrated out → quoted Song's "score-based model is independent of $Z_\theta$" line as the unlock. "Where else you'll meet $Z$" survey (Bayesian evidence, softmax, partition function, CRFs, MRFs/Boltzmann/Ising). Common-confusions block: tractable ≠ small, shape vs. normalizer carry different information, gradient trick works for $\nabla_x \log p$ but not for $\nabla_\theta \log p$ during max-likelihood, two senses of "tractable."
- `wiki/concepts/Diffusion Models.md` — wove in cross-link in two places: added "Sidesteps the [[Normalizing Constant]] problem that hobbles direct density modeling" to the diffusion row of the "Where this sits among generative models" table; added [[Normalizing Constant]] to Related concepts with one-line gloss "why noise-predictor parameterizations exist at all."
- `index.md` — added [[Normalizing Constant]] under Concepts with a one-line summary.
- `wiki/syntheses/learning-tracker.md` — added Normalizing Constant to coverage map (`working` — the cake analogy + the $\nabla_x \log Z_\theta = 0$ derivation are at the level the user can apply); bumped updated date; appended session log entry.

No matplotlib figure: matplotlib isn't installed in any available Python on this macOS box (prior tutor sessions ran on the Linux machine with `genesis_env`). Inline SVG was the right call anyway — the unnormalized-vs-normalized comparison is schematic (no formula-driven pixel positions needed).

Genuine knowledge addition: the user now has a *named* mental model for $Z_\theta$ that unifies what looks like a zoo of unrelated tricks (autoregressive factorization, invertible flows, ELBO, score matching, denoising) into one frame: "different ways to dodge the same intractable integral." This makes future ML reading parse cleaner — any "intractable" complaint about a likelihood-based model is almost certainly about a normalizing constant in disguise.
