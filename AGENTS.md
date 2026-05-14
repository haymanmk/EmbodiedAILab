# AGENTS.md — EmbodiedAILab Schema

This vault, **EmbodiedAILab**, is a focused research knowledge base built on the **LLM-wiki pattern**: the user curates raw sources and asks questions; the LLM (you) maintains a persistent, interlinked markdown wiki that compounds with every source.

**You write the wiki. The user reads it. The user owns the raw sources.**

> Claude Code users: a more detailed pattern reference lives at `~/.claude/skills/llm-wiki/SKILL.md`. This file is the vault-specific instantiation.

## Focus

Focused research lab notebook covering modern robotics and embodied AI:

- **robot learning** — imitation learning, reinforcement learning, offline datasets, policy evaluation
- **embodied AI** — vision-language-action models, language-conditioned control, agentic robotics
- **robotics foundations** — kinematics, dynamics, planning, controls, calibration, safety
- **development tools** — LeRobot, ROS 2, MoveIt, simulation, datasets, hardware interfaces
- **research reading** — papers, tutorials, textbooks, reports, and evolving theses

Cross-domain links are encouraged when they serve this focus. For example, a textbook chapter can link to a robot-learning concept; a hardware note can link to a synthesis on data collection; a personal research journal entry can link to an embodied AI question.

## Three Layers

1. **Raw sources** (`raw/`) — immutable. The user adds these (e.g. via Obsidian Web Clipper). You read but never modify.
2. **The wiki** (`wiki/`) — yours to write and maintain. Summary pages, entity pages, concept pages, syntheses, comparisons.
3. **The schema** (this file) — co-evolved with the user. If conventions need updating, propose the change here first; don't silently diverge.

## Directory Layout

```
.
├── AGENTS.md              # this file
├── index.md               # content catalog (you maintain)
├── log.md                 # chronological record (append-only)
├── raw/
│   ├── assets/            # downloaded images, PDFs, attachments
│   └── *.md               # source documents (clipped articles, transcripts, notes)
└── wiki/
    ├── sources/           # one summary page per source
    ├── entities/          # people, places, organizations, books, products
    ├── concepts/          # ideas, theories, frameworks, methodologies
    ├── syntheses/         # cross-source analyses, evolving theses
    └── journal/           # personal journal entries (domain: personal only)
```

Obsidian's "Attachment folder path" is set to `raw/assets/`. New downloads land there.

## Page Types and Frontmatter

Every wiki page has YAML frontmatter so Dataview can query it.

### Common fields (all wiki pages)

```yaml
---
type: source | entity | concept | synthesis | comparison | journal
domain: personal | research | reading | general
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
---
```

### Source pages (`wiki/sources/`)

One per ingested source. Filename: `{Title} - {Author or Site}.md` (Obsidian-safe; no slashes/colons).

```yaml
---
type: source
domain: research
created: 2026-05-09
updated: 2026-05-09
source_url: https://...
source_path: raw/article-slug.md
author: Name
published: 2024-11-01
tags: [...]
---
```

Body sections: **Summary** (3–6 sentences), **Key claims** (bulleted, each linkable), **Notable quotes** (verbatim, with location), **Connections** (wikilinks to entities/concepts touched), **Open questions**.

### Entity pages (`wiki/entities/`)

Filename: `{Entity Name}.md`. Body: **Overview**, **Key facts**, **Mentions** (wikilinks to source pages where this entity appears), **Related** (wikilinks to other entities/concepts).

### Concept pages (`wiki/concepts/`)

Filename: `{Concept Name}.md`. Body: **Definition**, **Origins / sources**, **Variations / debates** (where sources contradict, note it), **Related concepts**, **Mentions**.

### Synthesis pages (`wiki/syntheses/`)

Cross-source analyses. Filename: `{Topic} - synthesis.md`. Body: **Thesis** (current best understanding), **Supporting sources**, **Contradicting sources**, **Open questions**, **Last revised** (date + what changed).

### Journal pages (`wiki/journal/`)

Personal entries. Filename: `YYYY-MM-DD.md`. Free-form. Link liberally to entities/concepts. Domain is always `personal`.

## Linking Conventions

- **All cross-references use wikilinks**: `[[Page Name]]`. Use display text when needed: `[[Page Name|alias]]`.
- **Cite sources inline** when stating a claim: "X is true (per [[Source: Title - Author]])".
- **One subject per page**. Don't mix two entities or concepts on one page.
- **Use aliases via frontmatter** for synonyms: `aliases: ["Alt name", "Abbreviation"]`.

## Operations

### Ingest (new raw source → wiki)

1. Read the source in `raw/` in full. View images in `raw/assets/` if relevant.
2. Discuss takeaways with the user; let them flag what to emphasize.
3. Create the source page in `wiki/sources/`.
4. Update affected entity, concept, and synthesis pages — typically 5–15 pages per source. Strengthen, contradict, or extend existing claims. Create new entity/concept pages as needed.
5. Update `index.md` — add new pages under their categories with one-line summaries.
6. Append to `log.md`: `## [YYYY-MM-DD] ingest | {source title}` followed by the list of pages touched.
7. Report what changed so the user can browse the diff.

**Default to one source at a time** with a takeaways check-in. Only batch-ingest if the user explicitly asks.

### Query (question → answer)

1. Read `index.md` first to identify candidate pages.
2. Drill into pages and follow wikilinks.
3. Synthesize an answer with citations to wiki pages.
4. **Offer to file substantive answers as new wiki pages** — comparisons, analyses, new connections shouldn't disappear into chat. This is the compounding step.
5. If a page is created, append to `log.md`: `## [YYYY-MM-DD] query | {topic}`.

Output forms: markdown page (default), comparison table, Marp slide deck, chart, or canvas — match the question.

### Lint (health check)

When the user asks for a lint pass, scan and **report** (do not auto-fix):

- Contradictions between pages
- Stale claims that newer sources have superseded
- Orphan pages (no inbound wikilinks)
- Concepts referenced repeatedly but with no dedicated page
- Missing cross-references — pages that should link but don't
- Open questions worth filling with a web search or new source

User prioritizes; you execute the chosen fixes.

## Special Files

### `index.md` (content catalog)

Organized by category: Sources, Entities, Concepts, Syntheses, Journal. Each entry: `- [[Page]] — one-line summary`. **Updated on every ingest.** Read this FIRST when answering queries.

### `log.md` (chronological record)

Append-only. Every entry: `## [YYYY-MM-DD] {op} | {subject}` (greppable: `grep "^## \[" log.md | tail -10`).

## Hard Rules

- **Never modify files in `raw/`** — including typos. Raw is immutable.
- **Never write wiki content without reading this file first** — conventions can drift.
- **Never skip the index update** during ingest — a page not in `index.md` is invisible to future queries.
- **Never auto-fix during lint** — report findings, let the user decide.
- **Never let a substantive query answer disappear into chat** — offer to file it.
- **One source at a time** unless the user says batch.

## Schema Evolution

If a convention here is wrong or missing, propose an edit to this file and discuss with the user before changing your behavior. Don't silently diverge from documented conventions.
