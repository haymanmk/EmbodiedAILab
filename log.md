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
