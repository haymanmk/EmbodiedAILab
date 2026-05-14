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
