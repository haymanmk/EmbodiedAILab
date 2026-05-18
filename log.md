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
