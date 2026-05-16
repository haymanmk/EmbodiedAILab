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
