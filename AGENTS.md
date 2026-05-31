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

1. **Raw sources** (`raw/`) — substantively immutable. The user adds these (e.g. via Obsidian Web Clipper). You may apply **rendering-only fixes** (LaTeX escapes, malformed `\left(\right.` pairs, stripped function macros like `sim`/`log` without their backslash, invisible-function-application U+2061 unicode characters, broken alignment environments). Never alter substance — content, claims, attributions, structure, examples must stay verbatim. Every rendering-fix pass must be logged in `log.md` so the diff is reviewable.
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
    ├── about-me.md        # user profile (loaded by /tutor skill)
    ├── sources/           # one summary page per source
    ├── entities/          # people, places, organizations, books, products
    ├── concepts/          # ideas, theories, frameworks, methodologies
    ├── syntheses/         # cross-source analyses, evolving theses (incl. learning-tracker)
    ├── ingestion/         # chapter-level indices for large multi-chapter resources (textbooks)
    ├── assets/            # SVG/PNG/image storage (reusable diagrams, matplotlib plots)
    ├── canvases/          # JSON Canvas (.canvas) whiteboard files (optional, Obsidian-only)
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
source_format: pdf | paper | docs-site | web | video
total_pages: 615           # for PDFs only
author: Name
published: 2024-11-01
chunks_indexed: false      # Phase 2 hook — flips true after vector indexing
indexed_at:                # Phase 2 hook — date when chunks were indexed
study_status: not-started  # not-started | in-progress | covered | reference-only
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

### Ingestion Index pages (`wiki/ingestion/`)

Used **only** for resources too large to summarize on a single page
(textbooks). Each gets one chapter-level index. Papers and docs sites
do NOT get an ingestion index — their source page is sufficient.

Filename: `{Resource Title} - chapters.md`.

````yaml
---
type: ingestion-index
source: [[Resource Source Page]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
````

Body: a single table with columns `# | Title | Pages | Concepts | Status`.
Status values: `not started` | `queued` | `next` | `covered`.

## Markdown Formatting

This vault is read primarily through Obsidian, which **reflows prose to fit the editor pane**. Hard-wrapping paragraphs at a fixed column makes lines ragged on wide screens and produces noisy diffs whenever a sentence is edited mid-paragraph.

**Do NOT hard-wrap prose, list-item text, or blockquotes at ~72/80 columns.** Let paragraphs run as one long line; the editor wraps visually. This applies to all wiki pages — concept, source, synthesis, journal, ingestion-index — and to `index.md`, `log.md`, and this file.

Keep as-is (do NOT join onto one line):

- **Table rows** — one row per line, already the convention.
- **Code blocks** (` ``` `) — preserve exact line breaks; never reflow.
- **List items** — one item per line; if an item's text is long, let it stay on one line (don't break it across multiple physical lines).
- **YAML frontmatter** — one field per line.
- **Mermaid / ASCII / inline SVG blocks** — preserve exactly.

Common failure mode to avoid: wrapping prose at ~72 columns because that's the "developer comment" or "terminal-prose" convention. This is wrong for Obsidian markdown — that convention belongs to source code, not vault content.

Long URLs, long table cells, and long inline code spans are fine on a single line. Readability comes from headings, list structure, and tables — not from line length.

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

## Tutor Mode

This vault supports an AI tutor workflow built on top of the standard
operations above. Tutor mode is invoked in two ways:

- **Explicitly** via `/tutor` (Claude Code) — loads `.claude/skills/tutor/SKILL.md`.
- **Implicitly** when a trigger phrase is detected — auto-scoped to the
  workflow.

Outside tutor mode, behave as a standard Claude Code / wiki-maintainer
session — do NOT auto-load the profile or tracker, do NOT apply teaching
style, do NOT auto-commit.

For tools that don't support skills (ChatGPT, Cursor, Obsidian AI), paste
these three files at session start to simulate tutor context:

- `wiki/about-me.md`
- `wiki/syntheses/learning-tracker.md`
- `.claude/skills/tutor/SKILL.md`

### Trigger phrases (recognized intents)

When in tutor mode (or when one of these phrases is detected, which
auto-activates tutor mode for the duration of the workflow):

| Phrase | Workflow |
|---|---|
| `ingest <resource>` | Read resource in `raw/`; produce `wiki/sources/<resource>.md` with extended frontmatter; for textbooks only, also produce `wiki/ingestion/<resource> - chapters.md`. Update `index.md`, `log.md`, tracker. |
| `study Chapter N of <resource>` | Read that chapter from the PDF; produce/extend `wiki/concepts/` pages; flip chapter row in ingestion index to `covered`; update tracker. |
| `deep-read <paper>` | Read paper end-to-end; produce/extend source + concept pages; update tracker. |
| `I'm working on <project>` | Enter project mode for the session; add/update under "Current projects" in `wiki/about-me.md`. |
| `what should I study next` | Discuss tracker recommendations (don't just dump). |

### Ingestion conventions (Phase 2 readiness)

All `wiki/sources/` pages MUST include the extended frontmatter fields
(`source_format`, `source_path`, `total_pages` for PDFs, `chunks_indexed:
false`, `indexed_at:`, `study_status`). These are baked in so a future
vector-index layer can find unindexed sources without touching wiki
content.

Textbooks additionally get a chapter-level index at
`wiki/ingestion/<resource> - chapters.md`. Papers and docs sites do not.

## Special Files

### `index.md` (content catalog)

Organized by category: Sources, Entities, Concepts, Syntheses, Journal. Each entry: `- [[Page]] — one-line summary`. **Updated on every ingest.** Read this FIRST when answering queries.

### `log.md` (chronological record)

Append-only. Every entry: `## [YYYY-MM-DD] {op} | {subject}` (greppable: `grep "^## \[" log.md | tail -10`).

## Hard Rules

- **Never alter substance of files in `raw/`** — content, claims, attributions, examples, and structure must stay verbatim. **Rendering-only fixes are allowed and must be logged in `log.md`**: malformed LaTeX delimiter pairs (e.g., `\left(\right.` → `\left(`), function macros stripped of their backslash (`sim`/`log`/`exp` → `\sim`/`\log`/`\exp`), invisible-function-application U+2061 characters, broken alignment environments — i.e., format-only repairs that change appearance but not meaning. If in doubt, leave alone or ask.
- **Never write wiki content without reading this file first** — conventions can drift.
- **Never skip the index update** during ingest — a page not in `index.md` is invisible to future queries.
- **Never auto-fix during lint** — report findings, let the user decide.
- **Never let a substantive query answer disappear into chat** — offer to file it.
- **One source at a time** unless the user says batch.

## Schema Evolution

If a convention here is wrong or missing, propose an edit to this file and discuss with the user before changing your behavior. Don't silently diverge from documented conventions.
