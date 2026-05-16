# AI Tutor & Learning Companion — Design

**Status**: Draft, awaiting user review
**Date**: 2026-05-16
**Vault**: EmbodiedAILab
**Author**: User + Claude (brainstorming session 2026-05-16)

---

## 1. Context

The EmbodiedAILab vault is the user's research notebook for modern robotics and embodied AI, built on the LLM-wiki pattern (raw sources in `raw/`, curated wiki in `wiki/`, schema in `AGENTS.md`). The user wants to layer on top of this an **AI tutor and learning companion** that:

- Knows the user's role, goals, background, and teaching preferences well enough to teach in their voice and at their level — *without* the user re-explaining themselves each session, in *any* AI tool they use.
- Can ingest and reason over the user's growing library of resources (textbooks, papers, docs, eventually more) with a structure that scales from a handful of resources today to many later.
- Maintains a *living* curriculum tracker — what's been covered, what's queued, what prerequisites are missing — so the agent can recommend what to study next rather than wait to be asked.
- Provides predictable, named workflows for common tasks (ingest a resource, study a chapter, deep-read a paper) so the user doesn't have to spell them out each time.

## 2. Goals

- **Profile layer** that captures *who the user is* in a single portable markdown file readable by Claude Code, Cursor, ChatGPT, Obsidian AI, and any future tool.
- **Knowledge layer** that extends the existing `wiki/` pattern with structured frontmatter, chapter-level indices for textbooks, and consistent ingestion workflows.
- **Tracker layer** that the agent maintains automatically — coverage map, recommendations, gaps detected, session log.
- **Tutor invocation** that is frictionless for common workflows (auto-activate from trigger phrases) and explicit for everything else (`/tutor`).
- **Phase 2 readiness**: source-page frontmatter conventions designed so a future vector-index layer slots in without re-touching wiki content.

## 3. Non-Goals (Phase 1)

- Vector embeddings, chunked search, RAG infrastructure — deferred to Phase 2; design must accommodate but not implement.
- **Agent-generated binary images** (matplotlib PNG plots requiring a Python process) — deferred to Phase 1b, triggered by first need. Phase 1 uses text-authored visuals only: Mermaid, hand-written SVG (inline or as files in `wiki/assets/`), JSON Canvas (via the `json-canvas` skill), Obsidian callouts, ASCII art, and textbook figure citations (Option B+ from brainstorm).
- MCP server / cross-tool native integration — deferred indefinitely; copy-paste for non-Claude tools is acceptable for now.
- Audio/video resource ingestion (lectures, podcasts).
- Multi-user or sharing features — single-user.
- Spaced repetition / quizzing / flashcard generation.
- A web UI or Obsidian plugin — everything is markdown + native AI tool features.

## 4. User Context (from brainstorming)

| Dimension | Answer |
|---|---|
| Goals | **Researcher + builder + career** (1–2 year horizon) |
| Background | Automation engineer with fundamental programming; building modern ML and learning-based robotics from scratch on top of strong control-systems foundation |
| Solid ground | Classical control, kinematics intuition, sensor integration, real-time/deterministic systems, SWE fundamentals |
| Active gaps | Optimization math (KKT, Lagrange, constraint gradients, convex analysis), deep learning internals, PyTorch, training pipelines, IL details (ACT, Diffusion Policy), RL, VLA models, modern simulation |
| Teaching style | Default direct & explanatory; always-on curriculum tracking; project mode on explicit mention; Socratic follow-up after explaining |
| AI tools used | Claude Code (primary), Cursor, ChatGPT, Obsidian AI plugins |
| Seed resources | Modern Robotics (Lynch & Park), Sutton & Barto, LeRobot docs, ACT + Diffusion Policy papers |

## 5. Architecture

Four layers, all inside the existing vault. No new top-level directories; no external services in Phase 1.

```
EmbodiedAILab/
├── AGENTS.md                              # extended: Tutor Mode section + trigger phrases + ingestion conventions
├── wiki/
│   ├── about-me.md                        # NEW: profile (portable, tool-agnostic)
│   ├── sources/                           # EXISTING: per-resource summary pages (extended frontmatter)
│   ├── concepts/                          # EXISTING: per-concept pages
│   ├── syntheses/
│   │   └── learning-tracker.md            # NEW: curriculum + progress, agent-maintained
│   ├── ingestion/                         # NEW: chapter-level indices for textbooks only
│   ├── assets/                            # EXISTING: SVG/PNG/image storage (reusable diagrams)
│   └── canvases/                          # NEW (optional): JSON Canvas (.canvas) whiteboard files
├── raw/                                   # EXISTING: user-owned, immutable
├── .claude/
│   └── skills/
│       └── tutor/
│           └── SKILL.md                   # NEW: /tutor skill (project-local)
└── docs/superpowers/specs/                # this directory
    └── 2026-05-16-ai-tutor-companion-design.md
```

### Layer responsibilities

| Layer | Artifact | Owner | Updated when |
|---|---|---|---|
| Profile | `wiki/about-me.md` | User (with agent help) | Manually, as goals/projects evolve |
| Knowledge | `wiki/sources/`, `wiki/concepts/`, `wiki/ingestion/` | Agent (user reviews) | When user ingests or studies a resource |
| Tracker | `wiki/syntheses/learning-tracker.md` | Agent (auto-update) | End of each tutor workflow (auto-commit) |
| Invocation | `AGENTS.md` + `.claude/skills/tutor/SKILL.md` | User | Rarely (when conventions change) |

### Key design choices

1. **Profile is a *wiki page*, not a hidden config.** Lives at `wiki/about-me.md` so it's discoverable, searchable, and copy-pasteable into any tool.
2. **No new top-level directories** — everything fits the existing vault schema. The new `wiki/ingestion/` subdirectory has one narrow role: chapter-level indices for large multi-chapter resources.
3. **Phase 2 affordances baked into frontmatter** — `chunks_indexed`, `indexed_at`, `source_path`, `source_format`, `total_pages` fields exist from day one so a future ingestion script can find unindexed pages and process them without touching wiki content.

## 6. Component: Profile (`wiki/about-me.md`)

```markdown
---
type: profile
domain: personal
created: 2026-05-16
updated: 2026-05-16
role: Automation engineer
goals: [researcher, builder, career]
goal_horizon: 1-2 years
hours_per_week: TBD
primary_ai_tools: [Claude Code, Cursor, ChatGPT, Obsidian]
tags: [profile, learning, ai-tutor]
---

## Who I am

I'm an automation engineer with fundamental programming background. My
strengths are in control loops, sensors/actuators, real-time/deterministic
systems, and debugging physical hardware. I'm building modern ML and
learning-based robotics from scratch on top of that foundation.

## Where I'm going (1–2 year horizon)

Hybrid trajectory:
- **Research**: read, replicate, and eventually contribute to papers in
  embodied AI.
- **Build**: get real robots doing useful things end-to-end.
- **Career**: be employable as a robotics/ML engineer doing this work.

## What I know vs. what's new

**Solid ground** (lean on, don't re-derive): classical control, kinematics
intuition from automation, sensor integration, real-time systems, software
engineering fundamentals.

**Active gaps** (teach explicitly, ground from first principles):
optimization math (KKT, Lagrange, constraint gradients, convex analysis),
deep learning internals, PyTorch ecosystem, training pipelines, imitation
learning details (ACT, Diffusion Policy), reinforcement learning,
vision-language-action models, modern simulation (MuJoCo, Isaac).

## How I learn best

- **Default**: direct explanation with concrete examples and runnable code.
- **Tracking** (always on): maintain a running record of what I've covered
  and recommend what's next — see [[learning-tracker]].
- **Project mode**: when I name a project I'm working on, anchor concepts to
  that project. Don't volunteer this — wait for me to invoke it.
- **Socratic follow-up**: after explaining a concept, push me with 1–3
  questions that test whether I've internalized it.

## Current projects

(User-maintained. Empty until I name one.)

## Constraints / preferences

- Don't restate things I clearly already know — leverage the wiki.
- Cite back to source pages (wiki) or page numbers (PDFs) when possible.
- Code examples in Python by default; specify when else.

## Pointers

- Covered material & curriculum: [[learning-tracker]]
- Schema for this vault: [[AGENTS]]
```

## 7. Component: Knowledge Layer

### Extended source-page frontmatter

```yaml
---
type: source
domain: research
created: YYYY-MM-DD
updated: YYYY-MM-DD
source_path: raw/<filename>            # NEW: relative path to raw asset
source_format: pdf                     # NEW: pdf | paper | docs-site | web | video
source_url:                            # for web/docs
total_pages: 615                       # NEW: for PDFs
author:
published:
chunks_indexed: false                  # NEW (Phase 2 hook)
indexed_at:                            # NEW (Phase 2 hook)
study_status: not-started              # NEW: not-started | in-progress | covered | reference-only
tags: []
---
```

The `chunks_indexed` / `indexed_at` fields do nothing in Phase 1 — they exist so the Phase 2 ingestion script can walk `wiki/sources/`, find unindexed pages, chunk and embed them, and update these flags without ever touching wiki content.

`study_status` is a **denormalized** at-a-glance summary. The tracker (`learning-tracker.md`) is authoritative on conflicts; `study_status` is refreshed by the agent when chapters are studied.

### The `wiki/ingestion/` subdirectory

Used **only** for resources too large to summarize on a single page (textbooks). Each gets one chapter index file:

```markdown
---
type: ingestion-index
source: [[<Source Page>]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# <Resource> — Chapter Index

| # | Title | Pages | Concepts | Status |
|---|---|---|---|---|
| 2 | Configuration Space | 17–42 | [[C-Space]], [[Constraint Gradients and Tangent Spaces]] | covered |
| 3 | Rigid-Body Motions | 43–95 | [[SE(3)]], [[Twist]] | queued |
| 4 | Forward Kinematics | 97–141 | — | not started |
```

Why a separate subdirectory: chapter indices are *living working documents* the agent updates as study progresses. Putting them in `wiki/sources/` would conflict with the "one summary per source" convention. Papers and docs sites do not get an ingestion index — source page is sufficient.

### Ingestion workflows

**(a) PDF textbook** (Modern Robotics, Sutton & Barto):
1. User drops PDF in `raw/`.
2. User says `ingest <resource>`.
3. Agent reads ToC + first/last chapters, produces:
   - `wiki/sources/<resource>.md` (summary + structure, extended frontmatter)
   - `wiki/ingestion/<resource> - chapters.md` (chapter index, all `not started`)
   - Appends entry to `index.md` and `log.md`
   - Adds resource row to `learning-tracker.md` resource progress table
4. Per-chapter study happens later via `study Chapter N of <resource>`.

**(b) Research paper** (ACT, Diffusion Policy):
1. User drops PDF in `raw/`.
2. User says `ingest <paper>`.
3. Agent reads paper end-to-end, produces `wiki/sources/<paper>.md`, extends/creates concept pages, updates tracker.
4. No chapter index needed.

**(c) Web docs / docs site** (LeRobot):
1. Existing `wiki/syntheses/LeRobot Documentation Index.md` is **promoted** to `wiki/sources/` with `source_format: docs-site` frontmatter.
2. Updates happen on demand: when user asks about a topic, agent fetches relevant doc pages and extends concept pages accordingly.

## 8. Component: Tracker (`wiki/syntheses/learning-tracker.md`)

Single file. Authoritative source of truth for coverage and curriculum state.

```markdown
---
type: synthesis
domain: personal
created: 2026-05-16
updated: 2026-05-16
tags: [learning, tracker, curriculum]
---

# Learning Tracker

> Source of truth for what I've covered, what I'm doing now, what's queued.
> Agent updates this at the end of each tutor workflow (auto-commit).

## Active focus (this week / next 2 weeks)

- **Foundation thread**: Optimization math (KKT, Lagrange, constraint
  gradients). Currently working through [[Constraint Gradients and Tangent
  Spaces]]. Next: convex analysis basics, then Sutton & Barto policy
  gradient math.
- **Active project**: (none currently named)

## Recommendations (ranked, with rationale)

1. **Modern Robotics Ch. 3–5** (Rigid-Body Motions → Forward Kinematics →
   Velocity Kinematics & Jacobians) — closes the "what does a robot do"
   loop. Foundational language the IL papers assume.
2. **ACT paper deep-read** — once kinematics is in place, the action-space
   side of ACT becomes readable; transformer mechanics are the new piece.
3. **Diffusion Policy paper deep-read** — natural next step after ACT;
   contrast the two action representations head-to-head.

**Reference (not a study target)**: [[Sutton & Barto - RL]] — keep
accessible for RL theory lookups when ACT/Diffusion Policy reference
policy-gradient or behavior-cloning concepts. Not a deep-read target
unless RL becomes the primary thread later.

## Coverage map

### Concepts covered (with mastery signal)

| Concept | Source | Last studied | Mastery |
|---|---|---|---|
| [[Lagrange Multipliers]] | Modern Robotics §2 | 2026-05-14 | working |
| [[Karush-Kuhn-Tucker Conditions]] | Modern Robotics §2 | 2026-05-14 | working |
| [[Constraint Gradients and Tangent Spaces]] | Modern Robotics §2 | 2026-05-15 | building |
| [[Action Chunking Transformer]] | ACT paper | 2026-05-10 | overview-only |
| [[Vision-Language-Action Models]] | reading | 2026-05-09 | overview-only |

Mastery levels: **overview-only** (skimmed) → **building** (working through)
→ **working** (can apply) → **fluent** (can teach/derive).

### Resource progress

| Resource | Format | Progress | Status |
|---|---|---|---|
| [[Modern Robotics - Lynch & Park]] | textbook | Ch. 2 covered, Ch. 3 next | in-progress |
| [[Sutton & Barto - RL]] | textbook | Not started | queued |
| [[LeRobot Documentation Index]] | docs-site | Reference-only browsing | reference |
| [[ACT - Zhao et al]] | paper | Overview read | revisit later |

## Gaps detected (agent-maintained)

Things the agent has noticed are missing from coverage but are
prerequisites for queued material:

- **Convex sets & convex functions** — referenced by KKT but not yet a
  concept page. Needed before policy gradient theory.
- **Multivariate calculus refresher (Jacobians, Hessians)** — referenced by
  both optimization and ML training. Likely background but not explicitly
  indexed in the wiki.

## Session log

Append-only. One entry per tutor workflow.

- 2026-05-15 — extended [[Constraint Gradients and Tangent Spaces]];
  deferred worked examples; flagged convex sets gap.
- 2026-05-14 — created [[Karush-Kuhn-Tucker Conditions]] concept page; light
  Socratic follow-up on inequality constraints.
```

## 9. Component: Tutor Invocation

### Invocation table

| Input | Behavior |
|---|---|
| `study Chapter N of <resource>` | Auto-activates tutor mode for this workflow → loads profile + tracker, reads chapter, produces concept pages, commits, exits |
| `ingest <resource>` | Auto-activates for the ingestion workflow |
| `deep-read <paper>` | Auto-activates for paper deep-reads |
| `I'm working on <project>` | Auto-activates for the session (project mode is inherently sustained) |
| `what should I study next` | Auto-activates briefly to read tracker and discuss |
| `/tutor <question>` | Explicit tutor response for a question that doesn't match a trigger phrase |
| `/tutor` (alone) | Sticky session-long tutor mode |
| `/tutor stop` | Exit sticky tutor mode |
| Anything else | Regular Claude Code — no profile/tracker loading, no Socratic, no commits |

### `/tutor` skill — `.claude/skills/tutor/SKILL.md`

```markdown
---
name: tutor
description: Enter tutor mode for the EmbodiedAILab learning vault. Loads
  user profile and learning tracker, applies layered teaching style (direct,
  Socratic follow-up, project-aware, curriculum-tracking), enables trigger
  phrases for ingestion/study/deep-read workflows, and auto-commits per
  concept covered. Use when the user invokes /tutor or asks to start
  tutoring.
---

# Tutor Mode

You are now the user's learning tutor for this EmbodiedAILab vault.

## Bootstrap (before any other response)

1. Read `wiki/about-me.md` — load role, goals, solid ground, active gaps,
   teaching preferences, current projects, constraints.
2. Read `wiki/syntheses/learning-tracker.md` — load coverage map, current
   focus, recommendations, gaps detected, session log.
3. Greet briefly. Surface 1–2 items from "Recommendations" so the user
   knows context is loaded.

## Teaching style (layered)

- **Default**: direct & explanatory with examples and code. Lean on solid
  ground; ground gaps from first principles.
- **After explaining**: Socratic follow-up — 1–3 questions that test
  internalization.
- **On user-named project**: project mode — anchor concepts to that
  project.
- **Always-on**: curriculum tracking — flag missing prerequisites; update
  the tracker.

## Trigger phrases

See the invocation table in `AGENTS.md`. When a trigger phrase is detected,
run the canonical workflow for that phrase.

## Citation discipline

- Wiki concepts: `[[wikilink]]`
- PDF source: "see [[Source Page]] p. <page>"
- Docs site: URL section link

## Visual aids

Include visuals when they meaningfully aid understanding. Pick the right
format for the content — don't default to one.

| Format | Use for | Renders in |
|---|---|---|
| **Mermaid** | Flowcharts, hierarchies, state machines, simple block diagrams | Obsidian (native), GitHub, Cursor, most viewers |
| **Hand-written inline SVG** | Custom geometric illustrations where precision matters (manifolds, tangent planes, vector fields, set diagrams). Embed `<svg>...</svg>` directly in markdown. | Obsidian (native), GitHub (inline SVG), most viewers |
| **SVG files in `wiki/assets/`** | Reusable diagrams referenced from multiple pages: `![Tangent plane](../assets/tangent-plane.svg)` | Obsidian, GitHub, most viewers |
| **JSON Canvas (`.canvas`)** | Whiteboard-style synthesis: full-chapter concept maps, multi-source topic syntheses, mind maps. Use the `json-canvas` skill. Save to `wiki/canvases/`. | Obsidian only |
| **Obsidian callouts** | Definition / warning / example / quote boxes for polish. Use the `obsidian-markdown` skill. | Obsidian (styled); degrades to blockquote elsewhere |
| **ASCII / unicode** | Inline quick visuals in responses — matrices, small shapes, number lines. | Everywhere |
| **PDF figure citations** | When the source has the best version: *"see [[Modern Robotics]] Fig. 3.20 p. 89"*. Don't redraw. | N/A |

### Choosing the format

- **Mermaid by default** for diagrams (cheapest to author, most portable).
- **Inline SVG** when geometric precision matters and Mermaid can't express
  it (set diagrams, manifolds, geometric proofs).
- **SVG file in `wiki/assets/`** when the same diagram will be reused
  across multiple pages.
- **JSON Canvas** only on explicit ask (e.g., *"give me a canvas view of
  this chapter"*) or when a topic clearly needs a whiteboard (full-chapter
  concept maps, multi-source synthesis). Default off because it's
  Obsidian-only.
- **Callouts** sparingly, for definitions, warnings, and examples.
- **ASCII** for inline visuals in responses where a real diagram is
  overkill.
- **PDF citations** when the textbook figure is already the best version.

### Related skills

- `obsidian-markdown` — callouts, embeds, wikilinks, frontmatter
- `json-canvas` — `.canvas` whiteboard files

### When to give up gracefully

If a visual would genuinely help but none of the above can express it
(e.g., a real function plot with data, a high-fidelity rendered scene),
**state that explicitly and proceed without faking it**. Agent-generated
PNG via Python+matplotlib is a Phase 1b capability — when this gap blocks
teaching repeatedly, that's the signal to add it.

## Auto-commit protocol

Commit cadence depends on invocation mode:

- **Trigger-phrase workflow** (`ingest`, `study Chapter N`, `deep-read`):
  one commit at workflow end, summarizing all concepts touched.
- **Sticky `/tutor` session**: commit per concept fully covered, so
  history reflects the learning sequence.

At each commit boundary:
1. Update coverage map row(s) (mastery, last-studied date).
2. Update resource progress for any chapter/resource touched.
3. Append session log entry.
4. Regenerate recommendations if scope shifted.
5. Update "Gaps detected" if new prerequisite missing noticed.
6. Bump `updated:` on touched wiki pages.
7. `git add wiki/ && git commit -m "tutor: <concept or workflow summary>"`

## Exit

Exit tutor mode when:
- User invokes `/tutor stop` or says "end session", "stop tutoring", etc.
- User starts asking unrelated questions (config, debugging, etc.).

On exit: do one final commit if there are uncommitted tutor changes.
```

### AGENTS.md additions

A new top-level section after "Three Layers":

```markdown
## Tutor Mode

This vault supports an AI tutor workflow. Tutor mode is invoked:
- Explicitly via `/tutor` (Claude Code) — see `.claude/skills/tutor/SKILL.md`
- Implicitly when a trigger phrase is detected (auto-scoped to the workflow)

When not in tutor mode, behave as a regular Claude Code session — do NOT
auto-load the profile or tracker, do NOT apply teaching style, do NOT
auto-commit.

For tools that don't support skills (ChatGPT, Cursor, Obsidian AI), paste
the following three files at session start:
- `wiki/about-me.md`
- `wiki/syntheses/learning-tracker.md`
- `.claude/skills/tutor/SKILL.md`

### Trigger phrases (recognized intents)

(See invocation table in the design spec for the full list. Implement the
canonical workflows below.)

### Ingestion conventions

Source pages (`wiki/sources/`) must include the extended frontmatter:
`source_path`, `source_format`, `total_pages` (for PDFs), `chunks_indexed:
false`, `indexed_at:` (empty), `study_status: not-started`.

Textbooks additionally get a chapter-level index at
`wiki/ingestion/<resource> - chapters.md`. Papers and docs sites do not.
```

### Cross-tool usage

| Tool | How to invoke tutor mode |
|---|---|
| Claude Code | `/tutor` (skill auto-loads) |
| Cursor | Type "tutor mode" + paste `.claude/skills/tutor/SKILL.md`; or configure as a project rule |
| ChatGPT (Projects) | Paste profile + tracker + skill into Project instructions once |
| Claude.ai web | Paste the three at chat start, or save as a Project |
| Obsidian AI plugins | Paste at session start |

## 10. Build Sequencing (Phase 1)

Five chunks, ordered so each unlocks the next.

| # | Chunk | Produces | Validates |
|---|---|---|---|
| 1 | Profile | `wiki/about-me.md` populated with real answers from this brainstorm | Paste profile into ChatGPT and it gives meaningfully tailored responses |
| 2 | Tracker bootstrap | `wiki/syntheses/learning-tracker.md` populated with what the wiki already shows | Tracker matches reality; recommendations look sensible |
| 3 | AGENTS.md additions | Tutor Mode section + trigger phrase table + ingestion conventions | A fresh Claude Code session loads context correctly when a trigger phrase fires |
| 4 | `/tutor` skill | `.claude/skills/tutor/SKILL.md` | `/tutor explain backpropagation` produces a tutor-style response; `/tutor` alone stays sticky |
| 5 | First ingestion (live-fire) | Ingest Modern Robotics → produces source + chapter index; `study Chapter 2` extends concept pages | End-to-end workflow works; tracker auto-updates; auto-commit fires |

## 11. Success Criteria (Phase 1)

Without the user re-explaining themselves:

1. A fresh AI session in any tool (Claude Code, ChatGPT, Cursor) can be brought up to speed by loading 3 files (profile + tracker + AGENTS.md / tutor skill) and answers in a way that matches the user's background, gaps, and teaching preferences.
2. `/tutor explain <topic>` produces a direct explanation grounded in the wiki, leans on solid ground, grounds gaps from first principles, and ends with 1–3 Socratic questions.
3. `ingest <resource>` produces the expected artifacts in the expected locations with the right frontmatter — without the user spelling out the workflow.
4. `study Chapter N of <resource>` updates the tracker (mastery, last-studied, chapter status, gaps detected) and auto-commits with a meaningful message.
5. `what should I study next` returns a ranked list with rationale that the user actually finds useful.
6. After a week of use, the tracker reflects truth without manual editing.

If any of these are broken, that's a Phase 1 bug, not a Phase 2 deferral.

## 12. Phase 2 Readiness Checklist

Before declaring Phase 1 done:

- [ ] Every `wiki/sources/` page has `source_path`, `source_format`, `chunks_indexed: false`, `indexed_at:` (empty) fields.
- [ ] `total_pages` set on PDF source pages.
- [ ] `wiki/ingestion/<resource> - chapters.md` exists for all textbooks with valid page ranges per chapter.
- [ ] At least one ingestion has been validated end-to-end (Modern Robotics) — so the conventions are proven, not just paper-correct.

When Phase 2 is later triggered, the work is:
1. Write a script that walks `wiki/sources/`, finds entries with `chunks_indexed: false`, reads `source_path`, chunks + embeds the file, writes to a local vector store, sets `chunks_indexed: true` and `indexed_at: <date>`.
2. Write a small `tutor-search` Bash wrapper the agent invokes for semantic lookup.

No wiki content will need to be re-touched.

## 13. Worked Examples

### Example 1 — Trigger phrase: `study Chapter 3 of Modern Robotics`

**User input**:
> study Chapter 3 of Modern Robotics

**Agent behavior** (in Claude Code):

1. Detects trigger phrase → auto-activates tutor mode for this workflow.
2. Reads `wiki/about-me.md` and `wiki/syntheses/learning-tracker.md`.
3. Reads `wiki/sources/Modern Robotics - Lynch & Park.md` and `wiki/ingestion/Modern Robotics - chapters.md` to confirm Chapter 3 = "Rigid-Body Motions, pp. 43–95".
4. Reads pp. 43–95 of `raw/Modern Robotics - Lynch Park 2017.pdf`.
5. Responds with a direct explanation tailored to user's profile:

> Chapter 3 covers rigid-body motions. Since you're solid on classical kinematics intuition from automation, I'll skip the basic rotation-matrix derivation and focus on what's new: the exponential coordinates for rotations and the screw-theory generalization to SE(3). These are the language the rest of the book speaks in.
>
> [direct explanation, examples, Python snippets using `numpy`/`modern_robotics` package...]
>
> The key concepts to extract:
> - **SE(3)** as the group of rigid-body motions
> - **Twist** as the velocity representation
> - **Screw** as the geometric unifier
>
> I'll create concept pages for these now.

6. Creates/extends `wiki/concepts/SE(3).md`, `wiki/concepts/Twist.md`, `wiki/concepts/Screw Theory.md`.
7. Updates `wiki/ingestion/Modern Robotics - chapters.md`: Ch. 3 row → `covered`, concepts column populated.
8. Updates `wiki/syntheses/learning-tracker.md`:
   - Coverage map: adds three new rows (mastery: `building`)
   - Resource progress: Modern Robotics → "Ch. 3 covered, Ch. 4 next"
   - Session log: appends entry
9. Bumps `updated:` on all touched pages.
10. Commits: `tutor: studied Modern Robotics Ch. 3 (SE(3), twists, screw theory)`.
11. Ends with Socratic follow-up:

> Two quick questions before we move on:
>
> 1. A twist combines angular and linear velocity into one 6-vector. Why is this representation more natural than tracking them separately?
> 2. SE(3) is a Lie group, not a vector space. What goes wrong if you try to add two SE(3) elements component-wise?

12. Exits tutor mode (workflow complete).

### Example 2 — Explicit `/tutor`: `/tutor explain convex sets`

**User input**:
> /tutor explain convex sets

**Agent behavior**:

1. `/tutor` slash command → loads the tutor skill.
2. Bootstrap: reads `wiki/about-me.md` and `wiki/syntheses/learning-tracker.md`.
3. Notes from tracker: "convex sets" is in **Gaps detected** as a prerequisite for KKT and policy gradient theory. The user is currently working on optimization math. Strong relevance.
4. Notes from profile: user is in **active gaps** territory here — ground from first principles, code examples in Python, leverage their control-systems background where relevant.
5. Responds:

> Good one to nail down — you've got KKT and Lagrange in flight, and convex sets are the geometric substrate underneath both.
>
> **Definition.** A set $C \subseteq \mathbb{R}^n$ is convex if, for any two points $x, y \in C$ and any $\lambda \in [0, 1]$, the point $\lambda x + (1-\lambda) y$ is also in $C$. In words: the entire line segment between any two points in the set stays inside the set.
>
> **Visual** (inline SVG; Obsidian renders this as the side-by-side
> diagram):
>
> ```html
> <svg viewBox="0 0 400 210" xmlns="http://www.w3.org/2000/svg" width="500">
>   <!-- LEFT: Convex set (disk) -->
>   <circle cx="100" cy="100" r="70" fill="#e8f0fc" stroke="#2255aa" stroke-width="2"/>
>   <circle cx="58" cy="78" r="3.5" fill="#222"/>
>   <circle cx="142" cy="122" r="3.5" fill="#222"/>
>   <line x1="58" y1="78" x2="142" y2="122" stroke="#c02020" stroke-width="2"/>
>   <text x="44" y="76" font-size="14" font-family="serif" font-style="italic">x</text>
>   <text x="148" y="130" font-size="14" font-family="serif" font-style="italic">y</text>
>   <text x="32" y="200" font-size="12" font-family="sans-serif">convex (segment stays inside)</text>
>
>   <!-- RIGHT: Non-convex set (U-shape) -->
>   <path d="M 240 50 L 305 50 L 305 80 L 275 80 L 275 120 L 305 120 L 305 150 L 240 150 Z"
>         fill="#e8f0fc" stroke="#2255aa" stroke-width="2"/>
>   <circle cx="295" cy="65" r="3.5" fill="#222"/>
>   <circle cx="295" cy="135" r="3.5" fill="#222"/>
>   <line x1="295" y1="65" x2="295" y2="135" stroke="#c02020" stroke-width="2"/>
>   <text x="305" y="69" font-size="14" font-family="serif" font-style="italic">x</text>
>   <text x="305" y="140" font-size="14" font-family="serif" font-style="italic">y</text>
>   <text x="222" y="200" font-size="12" font-family="sans-serif">non-convex (segment leaves)</text>
> </svg>
> ```
>
> **Examples (convex)**: half-spaces $\{x : a^\top x \le b\}$, balls
> $\{x : \|x\| \le r\}$, polytopes (intersections of half-spaces).
> **Non-examples**: annulus (a ring), union of two disjoint balls, the
> unit sphere $\{x : \|x\|_2 = 1\}$ (surface only — a chord cuts through
> the interior).
>
> **Why this matters for your current thread** — the conceptual chain
> back to KKT:
>
> ```mermaid
> graph LR
>   A[Convex feasible set] --> C[Convex optimization problem]
>   B[Convex objective function] --> C
>   C --> D[KKT point = global optimum]
>   E[Either is non-convex] --> F[KKT point = local stationarity only]
> ```
>
> KKT conditions characterize stationary points of constrained
> optimization. When the feasible set is convex AND the objective is
> convex, KKT points are globally optimal. When either fails, KKT only
> tells you local stationarity — the gap between "we found a stationary
> point" and "we found *the* answer."

6. Creates `wiki/concepts/Convex Sets.md` linking to `[[Karush-Kuhn-Tucker Conditions]]`, `[[Lagrange Multipliers]]`.
7. Updates `learning-tracker.md`:
   - Coverage map: adds `[[Convex Sets]]` (mastery: `building`)
   - Gaps detected: removes "convex sets" line (no longer a gap)
   - Session log: appends entry
8. Commits: `tutor: covered convex sets; closed gap`.
9. Socratic follow-up:

> Two questions to test the picture:
>
> 1. The intersection of two convex sets is convex. Why? (Sketch the argument from the definition.)
> 2. The set $\{x : \|x\|_2 = 1\}$ (the unit sphere, not the unit ball) — convex or not? What's the contrast?

10. Exits tutor mode (one-shot `/tutor <question>` form).
