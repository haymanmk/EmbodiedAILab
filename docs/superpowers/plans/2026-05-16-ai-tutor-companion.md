# AI Tutor & Learning Companion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the AI tutor system inside the EmbodiedAILab vault per `docs/superpowers/specs/2026-05-16-ai-tutor-companion-design.md` — profile + tracker + AGENTS.md additions + `/tutor` skill, validated end-to-end by ingesting Modern Robotics and studying one chapter.

**Architecture:** All artifacts live inside the vault (no external services in Phase 1). Profile and tracker are wiki pages; the tutor protocol is a project-local Claude Code skill (`.claude/skills/tutor/SKILL.md`) with paste-in fallback for non-Claude tools. Visual aids span matplotlib (formula plots), hand-written SVG (schematics), Mermaid (structural), JSON Canvas (Obsidian-only whiteboards), and ASCII (inline). The everyday-analogy protocol (with explicit breakdown) is required for active-gap concepts.

**Tech Stack:** Markdown (Obsidian Flavored), Python 3 + pytest + PyYAML (structural validators), matplotlib + numpy (formula plots).

---

## File structure

**New files:**
- `wiki/about-me.md` — user profile (Task 2)
- `wiki/syntheses/learning-tracker.md` — curriculum tracker (Task 3)
- `.claude/skills/tutor/SKILL.md` — tutor skill (Task 5)
- `tests/conftest.py`, `tests/test_tutor_artifacts.py` — structural validators (Task 1)
- `requirements-dev.txt` — test dependencies (Task 1)

**Modified files:**
- `AGENTS.md` — add Tutor Mode section + trigger phrases + extended frontmatter conventions (Task 4)
- `index.md` — add entries for new pages (incrementally across Tasks 2, 3, 6)
- `log.md` — append entries (incrementally across each task)
- `.gitignore` — add Python test artifacts (Task 1)

**Created during ingestion (Task 6 onward):**
- `wiki/sources/Modern Robotics - Lynch & Park.md`
- `wiki/ingestion/Modern Robotics - chapters.md`
- `wiki/concepts/<new>.md` (created in Task 7 from Chapter 2 study)

**Required user-supplied input (Task 6):**
- `raw/Modern Robotics - Lynch Park 2017.pdf` — user places this file before running Task 6

---

## Task 1: Set up validation harness

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_tutor_artifacts.py`
- Create: `requirements-dev.txt`
- Modify: `.gitignore`

- [ ] **Step 1: Verify Python 3 and pip are available**

Run:
```bash
python3 --version
pip3 --version
```

Expected: Python 3.x and pip3 version strings. If absent, install Python 3 system-wide.

- [ ] **Step 2: Verify matplotlib + numpy (needed later for Task 7's plot validation, and for the tutor's formula visuals)**

Run:
```bash
python3 -c "import matplotlib, numpy; print(matplotlib.__version__, numpy.__version__)"
```

Expected: two version strings. If `ModuleNotFoundError`:
```bash
pip3 install --user matplotlib numpy
```

- [ ] **Step 3: Create `requirements-dev.txt`**

Create `/home/hayman/Workspace/EmbodiedAILab/requirements-dev.txt`:
```
pytest>=7.0
PyYAML>=6.0
```

- [ ] **Step 4: Install test dependencies**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && pip3 install --user -r requirements-dev.txt
```

Expected: pytest and PyYAML install successfully.

- [ ] **Step 5: Update `.gitignore`**

Append to `/home/hayman/Workspace/EmbodiedAILab/.gitignore`:
```
# Python test artifacts
.pytest_cache/
__pycache__/
*.pyc
```

(Current `.gitignore` contains only `.obsidian/`; the append must preserve that line.)

- [ ] **Step 6: Create `tests/conftest.py`**

Create `/home/hayman/Workspace/EmbodiedAILab/tests/conftest.py`:
```python
"""Shared fixtures and helpers for vault structural validation."""

import re
from pathlib import Path

import pytest
import yaml

VAULT = Path(__file__).resolve().parent.parent


def parse_frontmatter(path: Path):
    """Extract and parse the YAML frontmatter from a markdown file.

    Returns the parsed dict, or None if no frontmatter is present.
    """
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


@pytest.fixture
def vault() -> Path:
    return VAULT


@pytest.fixture
def fm():
    return parse_frontmatter
```

- [ ] **Step 7: Create `tests/test_tutor_artifacts.py` skeleton**

Create `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python
"""Structural validators for the AI tutor system artifacts.

Tests are organized by artifact in the order they appear in the
implementation plan: profile, tracker, AGENTS.md, /tutor skill,
first ingestion.

Each test asserts STRUCTURAL correctness (file exists, required
sections present, frontmatter fields valid). They deliberately do
NOT assert specific wording — that would be too brittle for
content-heavy markdown.
"""
```

- [ ] **Step 8: Verify pytest discovers the test file (and reports 0 tests collected)**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/ -v
```

Expected: pytest exits with code 5 (no tests collected) and prints `no tests ran`. This proves the harness works.

- [ ] **Step 9: Commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add tests/ requirements-dev.txt .gitignore
git commit -m "Add validation harness for tutor system artifacts"
```

---

## Task 2: Create the profile (`wiki/about-me.md`)

**Files:**
- Create: `wiki/about-me.md`
- Modify: `tests/test_tutor_artifacts.py` (append profile tests)
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: Append failing tests for the profile**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- Profile (wiki/about-me.md) ----------

def test_profile_exists(vault):
    assert (vault / "wiki/about-me.md").exists(), \
        "wiki/about-me.md not found"


def test_profile_frontmatter_required_fields(vault, fm):
    data = fm(vault / "wiki/about-me.md")
    assert data is not None, "frontmatter missing or unparseable"
    assert data.get("type") == "profile"
    assert data.get("domain") == "personal"
    assert data.get("role"), "role field empty"
    goals = data.get("goals", [])
    for g in ("researcher", "builder", "career"):
        assert g in goals, f"missing goal: {g}"
    assert data.get("goal_horizon"), "goal_horizon empty"
    assert data.get("primary_ai_tools"), "primary_ai_tools list empty"


def test_profile_has_required_sections(vault):
    text = (vault / "wiki/about-me.md").read_text(encoding="utf-8")
    for section in (
        "## Who I am",
        "## Where I'm going",
        "## What I know vs. what's new",
        "## How I learn best",
        "## Current projects",
        "## Constraints / preferences",
        "## Pointers",
    ):
        assert section in text, f"missing section: {section}"


def test_profile_has_everyday_analogies_preference(vault):
    text = (vault / "wiki/about-me.md").read_text(encoding="utf-8").lower()
    assert "everyday analog" in text, \
        "profile must mention everyday-analogies preference"
    assert "background" in text, \
        "profile must include the do-not-use-background-analogies rule"


def test_profile_links_to_tracker(vault):
    text = (vault / "wiki/about-me.md").read_text(encoding="utf-8")
    assert "[[learning-tracker]]" in text, \
        "profile must wikilink to [[learning-tracker]]"
```

- [ ] **Step 2: Run tests, verify all 5 fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 5 tests FAIL with messages indicating `wiki/about-me.md` does not exist.

- [ ] **Step 3: Create `wiki/about-me.md`**

Create `/home/hayman/Workspace/EmbodiedAILab/wiki/about-me.md`:
````markdown
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
- **Everyday analogies**: lead new concepts with an analogy from physical
  or common experience (a hiker on contour lines, water flowing downhill,
  a dimmer switch, line-of-sight in a room). Always state where the
  analogy breaks down — that's the most valuable part. **Do not draw
  analogies from my automation/control background** — everyday analogies
  travel better.
- **Tracking** (always on): maintain a running record of what I've covered
  and recommend what's next — see [[learning-tracker]].
- **Project mode**: when I name a project I'm working on, anchor concepts
  to that project. Don't volunteer this — wait for me to invoke it.
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
````

- [ ] **Step 4: Run tests, verify all 5 pass**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 5 tests PASS.

- [ ] **Step 5: Update `index.md`**

Read current `index.md` first:
```bash
cat /home/hayman/Workspace/EmbodiedAILab/index.md
```

Append a new section at the appropriate location (most likely at the top of the catalog, near `## Sources` or as a new `## Profile` section):
```markdown

## Profile

- [[about-me]] — user profile and teaching preferences for the AI tutor
```

If the file already has a meta/profile section, slot the entry there instead of creating a new section.

- [ ] **Step 6: Append to `log.md`**

Append to `/home/hayman/Workspace/EmbodiedAILab/log.md`:
```
## [2026-05-16] create | wiki/about-me.md — AI tutor profile per design spec
```

- [ ] **Step 7: Commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add wiki/about-me.md tests/test_tutor_artifacts.py index.md log.md
git commit -m "Add user profile (wiki/about-me.md) for AI tutor system"
```

---

## Task 3: Create the learning tracker (`wiki/syntheses/learning-tracker.md`)

**Files:**
- Create: `wiki/syntheses/learning-tracker.md`
- Modify: `tests/test_tutor_artifacts.py` (append tracker tests)
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: Append failing tests for the tracker**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- Tracker (wiki/syntheses/learning-tracker.md) ----------

TRACKER_PATH = "wiki/syntheses/learning-tracker.md"


def test_tracker_exists(vault):
    assert (vault / TRACKER_PATH).exists(), f"{TRACKER_PATH} not found"


def test_tracker_frontmatter(vault, fm):
    data = fm(vault / TRACKER_PATH)
    assert data is not None
    assert data.get("type") == "synthesis"
    assert data.get("domain") == "personal"
    assert "learning" in data.get("tags", [])
    assert "tracker" in data.get("tags", [])


def test_tracker_has_required_sections(vault):
    text = (vault / TRACKER_PATH).read_text(encoding="utf-8")
    for section in (
        "## Active focus",
        "## Recommendations",
        "## Coverage map",
        "### Concepts covered",
        "### Resource progress",
        "## Gaps detected",
        "## Session log",
    ):
        assert section in text, f"missing section: {section}"


def test_tracker_recommendations_prioritize_modern_robotics(vault):
    """Per user preference: Modern Robotics first, then ACT, then Diffusion
    Policy, with Sutton & Barto as reference (not study target)."""
    text = (vault / TRACKER_PATH).read_text(encoding="utf-8")
    mr_idx = text.find("Modern Robotics")
    act_idx = text.find("ACT")
    diff_idx = text.find("Diffusion")
    sb_idx = text.find("Sutton")
    assert mr_idx > 0 and act_idx > 0 and diff_idx > 0 and sb_idx > 0
    assert mr_idx < act_idx, "Modern Robotics must appear before ACT"
    assert act_idx < diff_idx, "ACT must appear before Diffusion Policy"
    assert "reference" in text.lower(), \
        "Sutton & Barto must be flagged as reference (not study target)"


def test_tracker_records_existing_wiki_concepts(vault):
    """The coverage map should reflect concepts that already exist in the
    wiki at bootstrap time (KKT, Lagrange, ACT, etc.)."""
    text = (vault / TRACKER_PATH).read_text(encoding="utf-8")
    for concept in (
        "Lagrange Multipliers",
        "Karush-Kuhn-Tucker Conditions",
        "Constraint Gradients and Tangent Spaces",
        "Action Chunking Transformer",
    ):
        assert concept in text, \
            f"coverage map missing existing wiki concept: {concept}"
```

- [ ] **Step 2: Run tests, verify the 5 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: profile tests PASS (5), tracker tests FAIL (5).

- [ ] **Step 3: Create `wiki/syntheses/learning-tracker.md`**

Create `/home/hayman/Workspace/EmbodiedAILab/wiki/syntheses/learning-tracker.md`:
````markdown
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
  gradients). Currently working through [[Constraint Gradients and Tangent Spaces]].
  Next: convex analysis basics, then onward to manipulator kinematics.
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
| [[Robot Learning]] | reading | 2026-05-09 | overview-only |
| [[Imitation Learning]] | reading | 2026-05-09 | overview-only |
| [[Moore-Penrose Pseudoinverse]] | reading | 2026-05-09 | overview-only |

Mastery levels: **overview-only** (skimmed) → **building** (working through)
→ **working** (can apply) → **fluent** (can teach/derive).

### Resource progress

| Resource | Format | Progress | Status |
|---|---|---|---|
| [[Modern Robotics - Lynch & Park]] | textbook | Not yet ingested | queued |
| [[Sutton & Barto - RL]] | textbook | Not started | reference |
| [[LeRobot Documentation Index]] | docs-site | Reference-only browsing | reference |
| ACT paper | paper | Overview read | revisit later |
| Diffusion Policy paper | paper | Not started | queued |

## Gaps detected (agent-maintained)

Things the agent has noticed are missing from coverage but are
prerequisites for queued material:

- **Convex sets & convex functions** — referenced by KKT but not yet a
  concept page. Needed before policy gradient theory.
- **Multivariate calculus refresher (Jacobians, Hessians)** — referenced
  by both optimization and ML training. Likely background but not
  explicitly indexed in the wiki.
- **SE(3) / rigid-body transforms** — prerequisite for Modern Robotics
  Ch. 3 onward; will be covered when that chapter is studied.

## Session log

Append-only. One entry per tutor workflow.

- 2026-05-16 — Bootstrapped learning tracker from existing wiki coverage.
````

- [ ] **Step 4: Run tests, verify all 10 pass**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 10 tests PASS (5 profile + 5 tracker).

- [ ] **Step 5: Update `index.md`**

Add to the syntheses section of `/home/hayman/Workspace/EmbodiedAILab/index.md`:
```markdown
- [[learning-tracker]] — curriculum, coverage map, recommendations, session log (agent-maintained)
```

- [ ] **Step 6: Append to `log.md`**

```
## [2026-05-16] create | wiki/syntheses/learning-tracker.md — bootstrapped from existing wiki concepts
```

- [ ] **Step 7: Commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add wiki/syntheses/learning-tracker.md tests/test_tutor_artifacts.py index.md log.md
git commit -m "Add learning tracker bootstrapped from existing wiki coverage"
```

---

## Task 4: Extend `AGENTS.md` with Tutor Mode

This task makes three additions to `AGENTS.md`: (a) extends the existing source-page frontmatter convention with the new fields, (b) adds a new "Ingestion Index pages" subsection under Page Types, and (c) adds a top-level "## Tutor Mode" section after "## Operations". The original AGENTS.md content is preserved.

**Files:**
- Modify: `AGENTS.md`
- Modify: `tests/test_tutor_artifacts.py` (append AGENTS tests)

- [ ] **Step 1: Append failing tests for AGENTS.md**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- AGENTS.md additions ----------

def test_agents_has_tutor_mode_section(vault):
    text = (vault / "AGENTS.md").read_text(encoding="utf-8")
    assert "## Tutor Mode" in text


def test_agents_has_trigger_phrases_subsection(vault):
    text = (vault / "AGENTS.md").read_text(encoding="utf-8")
    assert "Trigger phrases" in text or "Trigger Phrases" in text


def test_agents_source_frontmatter_includes_new_fields(vault):
    """The source-page frontmatter example in AGENTS.md must include the
    Phase-2-readiness fields baked in for the tutor system."""
    text = (vault / "AGENTS.md").read_text(encoding="utf-8")
    for field in ("source_format", "chunks_indexed", "indexed_at",
                  "total_pages", "study_status"):
        assert field in text, \
            f"AGENTS.md source-frontmatter example missing field: {field}"


def test_agents_documents_ingestion_index_page_type(vault):
    text = (vault / "AGENTS.md").read_text(encoding="utf-8")
    assert "ingestion-index" in text or "Ingestion Index" in text, \
        "AGENTS.md must document the ingestion-index page type"
    assert "wiki/ingestion" in text, \
        "AGENTS.md must mention wiki/ingestion/ directory"


def test_agents_preserves_original_sections(vault):
    """Sanity check: the original AGENTS.md sections must still exist."""
    text = (vault / "AGENTS.md").read_text(encoding="utf-8")
    for section in (
        "## Focus",
        "## Three Layers",
        "## Directory Layout",
        "## Page Types and Frontmatter",
        "## Linking Conventions",
        "## Operations",
        "## Special Files",
        "## Hard Rules",
        "## Schema Evolution",
    ):
        assert section in text, f"original section lost: {section}"
```

- [ ] **Step 2: Run tests, verify the 5 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 10 prior PASS + 5 new FAIL.

- [ ] **Step 3: Update source-page frontmatter example in AGENTS.md**

In `/home/hayman/Workspace/EmbodiedAILab/AGENTS.md`, replace the existing source-frontmatter block with the extended version. Use Edit-style replacement:

Find this block:
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

Replace with:
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

- [ ] **Step 4: Add "Ingestion Index pages" subsection to `## Page Types and Frontmatter`**

In `/home/hayman/Workspace/EmbodiedAILab/AGENTS.md`, after the existing `### Journal pages (wiki/journal/)` section and before the next top-level `## Linking Conventions` section, insert:

```markdown

### Ingestion Index pages (`wiki/ingestion/`)

Used **only** for resources too large to summarize on a single page
(textbooks). Each gets one chapter-level index. Papers and docs sites
do NOT get an ingestion index — their source page is sufficient.

Filename: `{Resource Title} - chapters.md`.

```yaml
---
type: ingestion-index
source: [[Resource Source Page]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

Body: a single table with columns `# | Title | Pages | Concepts | Status`.
Status values: `not started` | `queued` | `next` | `covered`.
```

- [ ] **Step 5: Add "## Tutor Mode" section after "## Operations"**

In `/home/hayman/Workspace/EmbodiedAILab/AGENTS.md`, after the entire `## Operations` section (which ends just before `## Special Files`), insert a new section:

```markdown

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
```

- [ ] **Step 6: Run tests, verify all 15 pass**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 15 tests PASS.

- [ ] **Step 7: Append to `log.md`**

```
## [2026-05-16] modify | AGENTS.md — added Tutor Mode, trigger phrases, ingestion-index page type, extended source frontmatter
```

- [ ] **Step 8: Commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add AGENTS.md tests/test_tutor_artifacts.py log.md
git commit -m "Extend AGENTS.md with Tutor Mode, trigger phrases, and extended frontmatter conventions"
```

---

## Task 5: Create the `/tutor` skill (`.claude/skills/tutor/SKILL.md`)

**Files:**
- Create: `.claude/skills/tutor/SKILL.md`
- Modify: `tests/test_tutor_artifacts.py` (append skill tests)
- Modify: `log.md`

- [ ] **Step 1: Append failing tests for the skill**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- /tutor skill (.claude/skills/tutor/SKILL.md) ----------

SKILL_PATH = ".claude/skills/tutor/SKILL.md"


def test_skill_exists(vault):
    assert (vault / SKILL_PATH).exists(), f"{SKILL_PATH} not found"


def test_skill_frontmatter(vault, fm):
    data = fm(vault / SKILL_PATH)
    assert data is not None
    assert data.get("name") == "tutor"
    assert data.get("description"), "skill description empty"


def test_skill_has_required_sections(vault):
    text = (vault / SKILL_PATH).read_text(encoding="utf-8")
    for section in (
        "## Bootstrap",
        "## Teaching style",
        "## Default explanation pattern",
        "## Trigger phrases",
        "## Citation discipline",
        "## Visual aids",
        "## Auto-commit protocol",
        "## Exit",
    ):
        assert section in text, f"missing section: {section}"


def test_skill_includes_everyday_analogy_rule(vault):
    text = (vault / SKILL_PATH).read_text(encoding="utf-8").lower()
    assert "everyday" in text, "skill must enforce everyday-analogy preference"
    assert "breaks down" in text or "breakdown" in text, \
        "skill must require analogy-breakdown discipline"
    assert "automation" in text or "background" in text, \
        "skill must explicitly forbid background-based analogies"


def test_skill_documents_matplotlib_convention(vault):
    text = (vault / SKILL_PATH).read_text(encoding="utf-8")
    assert "matplotlib" in text.lower()
    assert "wiki/assets" in text, \
        "matplotlib convention must use wiki/assets/<topic>/ layout"


def test_skill_lists_trigger_phrases(vault):
    text = (vault / SKILL_PATH).read_text(encoding="utf-8")
    for phrase in (
        "ingest",
        "study Chapter",
        "deep-read",
        "I'm working on",
        "what should I study next",
    ):
        assert phrase in text, f"missing trigger phrase: {phrase}"
```

- [ ] **Step 2: Run tests, verify the 6 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 15 prior PASS + 6 new FAIL.

- [ ] **Step 3: Create the skill directory**

```bash
mkdir -p /home/hayman/Workspace/EmbodiedAILab/.claude/skills/tutor
```

- [ ] **Step 4: Create `.claude/skills/tutor/SKILL.md`**

Create `/home/hayman/Workspace/EmbodiedAILab/.claude/skills/tutor/SKILL.md`:
````markdown
---
name: tutor
description: Enter tutor mode for the EmbodiedAILab learning vault. Loads user profile and learning tracker, applies layered teaching style (direct, everyday analogies, Socratic follow-up, project-aware, curriculum-tracking), enables trigger phrases for ingestion/study/deep-read workflows, and auto-commits per concept covered. Use when the user invokes /tutor or asks to start tutoring.
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

## Default explanation pattern (for active-gap concepts)

When teaching a concept in active gaps, structure the explanation:

1. **Everyday analogy** (if a natural one exists): use a physical,
   spatial, or common-experience analogy — something happening around
   us, not domain-specific knowledge. Examples:
   - *A hiker walking along a contour line* to explain why $\nabla h(x)$
     is perpendicular to the constraint surface $h(x)=c$ (the hiker
     stays at constant elevation, so they walk perpendicular to the
     steepest-ascent direction).
   - *A dimmer switch* for the sigmoid function (smooth transition from
     off to on, unlike a binary switch).
   - *Line-of-sight in a room* for convex sets.

   Always state where the analogy breaks down. An analogy without a
   breakdown is a misleading shortcut, not a mental model.

2. **Definition + intuition**: precise statement, plus plain-words
   meaning.

3. **Worked example or visualization**: as appropriate (see Visual aids).

4. **Connection back to current thread**: how this fits the user's
   in-flight learning.

If no natural everyday analogy fits, skip step 1 — don't force a weak
one. **Do NOT draw analogies from the user's automation/control
background**; everyday analogies travel better.

When an analogy lands well (user signals understanding), record it on the
concept page in a `## Bridges from` section so future sessions reuse it.

## Trigger phrases

| Input | Workflow |
|---|---|
| `ingest <resource>` | Read resource in `raw/`; produce `wiki/sources/<resource>.md` with extended frontmatter; for textbooks only, also produce `wiki/ingestion/<resource> - chapters.md`. Update `index.md`, `log.md`, tracker. |
| `study Chapter N of <resource>` | Read that chapter from the PDF; produce/extend `wiki/concepts/` pages; flip the chapter row in the ingestion index to `covered`; update tracker. |
| `deep-read <paper>` | Read paper end-to-end; produce/extend source + concept pages; update tracker. |
| `I'm working on <project>` | Enter project mode for the session; add/update entry under "Current projects" in `wiki/about-me.md`. |
| `what should I study next` | Read tracker recommendations and discuss; don't just dump. |

## Citation discipline

- Wiki concepts: `[[wikilink]]`
- PDF source: "see [[Source Page]] p. <page>"
- Docs site: URL section link

## Visual aids

Pick the format that fits the content. The core decision: **does drawing
this require evaluating a mathematical expression to compute pixel
positions?**

- **Yes (formula-driven)** → matplotlib (see convention below).
- **No (schematic/conceptual)** → SVG, Mermaid, or ASCII.

| Format | Use for |
|---|---|
| Mermaid | Flowcharts, hierarchies, state machines, simple block diagrams |
| Hand-written inline SVG | Schematic geometric illustrations (sets, manifolds, tangent planes). Embed `<svg>...</svg>` directly in markdown — no code fence. |
| SVG files in `wiki/assets/` | Reusable schematic diagrams referenced from multiple pages |
| **Matplotlib → PNG** | Formula-driven plots — function plots, gradient fields, level sets, loss landscapes, decision boundaries, sampled distributions |
| JSON Canvas (`.canvas`) | Whiteboard-style synthesis (Obsidian-only). Use the `json-canvas` skill. Save to `wiki/canvases/`. |
| Obsidian callouts | Definition / warning / example boxes. Use the `obsidian-markdown` skill. |
| ASCII / unicode | Inline quick visuals where a real diagram is overkill |
| PDF figure citations | When the source has the best version: *"see [[Source]] Fig. N p. M"*. Don't redraw. |

### Matplotlib invocation convention

When matplotlib is the right tool:

1. Create directory `wiki/assets/<topic>/` (e.g., `wiki/assets/sigmoid/`).
2. Write a small Python script at `wiki/assets/<topic>/<name>.py` that
   produces `<name>.png` next to itself (use `plt.savefig("<name>.png",
   dpi=120)`).
3. Run via Bash: `cd wiki/assets/<topic> && python <name>.py`.
4. Embed in the concept page: `![<caption>](../assets/<topic>/<name>.png)`.
5. Commit both `.py` and `.png` (script keeps the plot
   reproducible/editable; PNG renders everywhere).

### When to give up gracefully

If a visual would genuinely help but none of the above can express it
(3D rendered scenes, animations, interactive widgets), state that
explicitly and proceed without faking it. Those capabilities are Phase 1b
or beyond.

## Auto-commit protocol

Commit cadence depends on invocation mode:

- **Trigger-phrase workflow** (`ingest`, `study Chapter N`, `deep-read`):
  one commit at workflow end, summarizing all concepts touched.
- **Sticky `/tutor` session**: commit per concept fully covered, so
  history reflects the learning sequence.

At each commit boundary:

1. Update coverage map row(s) (mastery, last-studied date).
2. Update resource progress for any chapter/resource touched.
3. Append session log entry to `wiki/syntheses/learning-tracker.md`.
4. Regenerate recommendations if scope shifted.
5. Update "Gaps detected" if a new prerequisite missing was noticed.
6. Bump `updated:` on touched wiki pages.
7. `git add wiki/ && git commit -m "tutor: <concept or workflow summary>"`

## Exit

Exit tutor mode when:

- User invokes `/tutor stop` or says "end session", "stop tutoring", etc.
- User starts asking unrelated questions (config, debugging, etc.).

On exit: do one final commit if there are uncommitted tutor changes.
````

- [ ] **Step 5: Run tests, verify all 21 pass**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 21 tests PASS (5 profile + 5 tracker + 5 AGENTS + 6 skill).

- [ ] **Step 6: Append to `log.md`**

```
## [2026-05-16] create | .claude/skills/tutor/SKILL.md — /tutor slash command for vault-scoped tutor mode
```

- [ ] **Step 7: Commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add .claude/ tests/test_tutor_artifacts.py log.md
git commit -m "Add /tutor skill with everyday-analogy protocol and visual aids guide"
```

---

## Task 6: First ingestion — Modern Robotics (live-fire validation)

This task validates the end-to-end ingestion workflow. It has **manual steps** that require running Claude Code with the `/tutor` skill loaded, because the actual ingestion is an LLM action (reading the PDF and producing summary pages). The tests verify structural correctness of the resulting artifacts.

**Files:**
- Required input (user-supplied): `raw/Modern Robotics - Lynch Park 2017.pdf`
- Created by tutor: `wiki/sources/Modern Robotics - Lynch & Park.md`
- Created by tutor: `wiki/ingestion/Modern Robotics - chapters.md`
- Updated by tutor: `wiki/syntheses/learning-tracker.md`, `index.md`, `log.md`
- Modify: `tests/test_tutor_artifacts.py` (append ingestion tests)

- [ ] **Step 1: Verify the Modern Robotics PDF is in place**

The user must obtain a copy of *Modern Robotics: Mechanics, Planning, and Control* by Kevin Lynch and Frank Park (2017) and place it at `raw/Modern Robotics - Lynch Park 2017.pdf`.

Verify:
```bash
ls -la /home/hayman/Workspace/EmbodiedAILab/raw/ | grep -i "modern robotics"
```

Expected: one PDF file listed. If absent, the user must add it before continuing.

- [ ] **Step 2: Append failing tests for the ingestion artifacts**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- First ingestion: Modern Robotics ----------

MR_SOURCE = "wiki/sources/Modern Robotics - Lynch & Park.md"
MR_INDEX = "wiki/ingestion/Modern Robotics - chapters.md"


def test_mr_source_page_exists(vault):
    assert (vault / MR_SOURCE).exists(), f"{MR_SOURCE} not found"


def test_mr_source_frontmatter(vault, fm):
    data = fm(vault / MR_SOURCE)
    assert data is not None
    assert data.get("type") == "source"
    assert data.get("source_format") == "pdf"
    assert data.get("source_path", "").startswith("raw/")
    assert data.get("source_path", "").endswith(".pdf")
    assert data.get("total_pages", 0) > 100, \
        "total_pages should be set to actual page count"
    assert data.get("chunks_indexed") is False, \
        "Phase-2 hook chunks_indexed must be present and False"
    # indexed_at must be PRESENT in frontmatter (even if empty / null)
    assert "indexed_at" in data
    assert data.get("study_status") in (
        "not-started", "in-progress", "covered", "reference-only"
    )


def test_mr_source_has_required_body_sections(vault):
    text = (vault / MR_SOURCE).read_text(encoding="utf-8")
    # Per AGENTS.md source-page convention
    for section in ("## Summary", "## Key claims", "## Connections"):
        assert section in text, f"missing section: {section}"


def test_mr_chapter_index_exists(vault):
    assert (vault / MR_INDEX).exists(), f"{MR_INDEX} not found"


def test_mr_chapter_index_frontmatter(vault, fm):
    data = fm(vault / MR_INDEX)
    assert data is not None
    assert data.get("type") == "ingestion-index"
    assert "Modern Robotics" in str(data.get("source", ""))


def test_mr_chapter_index_has_table(vault):
    text = (vault / MR_INDEX).read_text(encoding="utf-8")
    # Verify the table header columns
    assert "Title" in text and "Pages" in text and "Concepts" in text \
        and "Status" in text, "chapter index table missing required columns"
    # Verify at least 4 chapter rows (Modern Robotics has 13 chapters)
    table_rows = [
        line for line in text.splitlines()
        if line.startswith("|") and "---" not in line
    ]
    # Subtract 1 for the header row
    data_rows = len(table_rows) - 1
    assert data_rows >= 4, f"expected at least 4 chapter rows, got {data_rows}"


def test_mr_tracker_resource_progress_updated(vault):
    text = (vault / "wiki/syntheses/learning-tracker.md").read_text(encoding="utf-8")
    # The resource row for Modern Robotics should no longer say "Not yet ingested"
    assert "Modern Robotics" in text
    # After ingestion: status should be "queued" (chapter index built but not studied yet)
    # or already "in-progress" if Task 7 ran first. Both acceptable.
    assert "Not yet ingested" not in text, \
        "tracker still reports 'Not yet ingested' — was ingestion workflow run?"
```

- [ ] **Step 3: Run tests, verify the 6 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 21 prior PASS + 6 new FAIL (Modern Robotics artifacts don't exist yet).

- [ ] **Step 4: Open a Claude Code session in the vault and trigger ingestion**

This is a **manual step**. In a Claude Code terminal at `/home/hayman/Workspace/EmbodiedAILab`, run:

```
ingest Modern Robotics
```

The `/tutor` skill (loaded automatically because the trigger phrase auto-activates tutor mode per `AGENTS.md`) will:

1. Read `wiki/about-me.md` and `wiki/syntheses/learning-tracker.md` for context.
2. Read `raw/Modern Robotics - Lynch Park 2017.pdf` — at minimum the table of contents and first/last chapters.
3. Produce `wiki/sources/Modern Robotics - Lynch & Park.md` with the extended frontmatter (including correct `total_pages`).
4. Produce `wiki/ingestion/Modern Robotics - chapters.md` with one row per chapter, all `Status: not started`.
5. Update `index.md` to add entries for the new source and ingestion index pages.
6. Update `wiki/syntheses/learning-tracker.md`: change the Modern Robotics resource row from "Not yet ingested" to "Chapter index built, no chapters covered" (or similar), append a session log entry.
7. Append to `log.md`.
8. Auto-commit per the tutor's protocol: `tutor: ingested Modern Robotics, created chapter index`.

If the trigger phrase doesn't auto-activate tutor mode, fall back to invoking `/tutor` first, then sending `ingest Modern Robotics` as the next prompt.

- [ ] **Step 5: Verify the artifacts exist and pass structural validation**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: all 27 tests PASS.

If any of the new 6 tests fail, inspect the failure messages — the most common issues are: missing extended frontmatter fields (the tutor must explicitly use them per the AGENTS.md convention), or the chapter index table missing required columns. Edit the produced artifacts to fix, do NOT relax the tests.

- [ ] **Step 6: Spot-check the artifacts for content quality (subjective)**

Open the two new pages in Obsidian (or `cat` them) and verify:

- The source page summary is 3–6 sentences and accurate to Modern Robotics' actual content.
- The chapter index lists ALL chapters (Modern Robotics has 13 chapters) with reasonable page-range estimates. Missing chapters should be fixed manually.
- The connections section in the source page wikilinks to at least 2–3 relevant existing concepts (KKT, Lagrange Multipliers, etc.).

If the agent missed chapters or got page ranges badly wrong, manually correct the chapter index and re-run the tests.

- [ ] **Step 7: Verify the auto-commit was made by the tutor skill**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && git log --oneline -5
```

Expected: most recent commit starts with `tutor:` and mentions Modern Robotics ingestion. If absent, the tutor skipped the auto-commit step — fix the skill or commit manually:

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add wiki/ index.md log.md
git commit -m "tutor: ingested Modern Robotics, created chapter index"
```

- [ ] **Step 8: Commit the new tests (not committed by the tutor)**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add tests/test_tutor_artifacts.py
git commit -m "Add structural validators for Modern Robotics ingestion artifacts"
```

---

## Task 7: Study Chapter 2 of Modern Robotics (per-chapter workflow validation)

Validates the chapter-level workflow: agent reads a specific chapter range, extends/creates concept pages, flips the chapter status, updates the tracker, and auto-commits. This is the lower-level live-fire test alongside Task 6.

Chapter 2 of Modern Robotics is *Configuration Space* — directly relevant to the user's current optimization-math thread (constraint surfaces, tangent spaces, degrees of freedom).

**Files:**
- Created/extended by tutor: `wiki/concepts/C-Space.md`, `wiki/concepts/Constraint Gradients and Tangent Spaces.md` (existing — to be extended)
- Updated by tutor: `wiki/ingestion/Modern Robotics - chapters.md`, `wiki/syntheses/learning-tracker.md`
- Modify: `tests/test_tutor_artifacts.py` (append chapter-study tests)

- [ ] **Step 1: Append failing tests for Chapter 2 study**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- Study Chapter 2 of Modern Robotics ----------

def test_mr_chapter2_marked_covered(vault):
    """After studying Chapter 2, its row in the ingestion index must be
    marked 'covered'."""
    text = (vault / MR_INDEX).read_text(encoding="utf-8")
    # Find lines describing Chapter 2 — should contain '2' as the first col
    # and 'covered' (not 'not started' / 'queued') as the last col.
    lines = [
        line for line in text.splitlines()
        if line.startswith("|") and "Configuration Space" in line
    ]
    assert len(lines) >= 1, "no Chapter 2 row found in chapter index"
    assert "covered" in lines[0].lower(), \
        f"Chapter 2 row not marked covered: {lines[0]}"


def test_mr_chapter2_produced_cspace_concept(vault):
    """Chapter 2 introduces C-space. There should be a concept page for it
    (or a substantively-extended existing page)."""
    candidates = [
        vault / "wiki/concepts/C-Space.md",
        vault / "wiki/concepts/Configuration Space.md",
    ]
    assert any(p.exists() for p in candidates), \
        "no concept page found for C-space / Configuration Space"


def test_mr_chapter2_concept_links_back_to_source(vault):
    """The C-space concept page must wikilink back to the Modern Robotics
    source page."""
    for candidate in (
        vault / "wiki/concepts/C-Space.md",
        vault / "wiki/concepts/Configuration Space.md",
    ):
        if candidate.exists():
            text = candidate.read_text(encoding="utf-8")
            assert "Modern Robotics" in text, \
                f"{candidate.name} missing wikilink back to source"
            return


def test_tracker_session_log_records_chapter2(vault):
    text = (vault / "wiki/syntheses/learning-tracker.md").read_text(encoding="utf-8")
    log_section = text.split("## Session log", 1)
    assert len(log_section) == 2, "tracker missing Session log section"
    log_text = log_section[1]
    assert "Chapter 2" in log_text or "Ch. 2" in log_text or "C-Space" in log_text \
        or "Configuration Space" in log_text, \
        "session log does not record Chapter 2 study"
```

- [ ] **Step 2: Run tests, verify the 4 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 27 prior PASS + 4 new FAIL.

- [ ] **Step 3: Open a Claude Code session and trigger Chapter 2 study**

In Claude Code at `/home/hayman/Workspace/EmbodiedAILab`, run:

```
study Chapter 2 of Modern Robotics
```

The `/tutor` skill (auto-activated by the trigger phrase) will:

1. Read profile + tracker if not already loaded.
2. Read `wiki/ingestion/Modern Robotics - chapters.md` to find Chapter 2's page range.
3. Read those pages of `raw/Modern Robotics - Lynch Park 2017.pdf`.
4. Produce or extend concept pages — at minimum a C-space page; likely also extends `Constraint Gradients and Tangent Spaces.md`.
5. **Apply the everyday-analogy protocol** for any active-gap concept (Chapter 2 introduces topology of configuration spaces — likely a new concept requiring an analogy with breakdown).
6. **Apply visual aids appropriately** — for a topological / geometric concept, hand-written inline SVG is the natural choice (no formula evaluation needed for typical C-space illustrations). Matplotlib only if a function plot is genuinely needed.
7. Flip the Chapter 2 row in the ingestion index to `covered`, populate its `Concepts` column with wikilinks.
8. Update the tracker coverage map with new/updated concept rows, append session log entry, refresh recommendations if appropriate.
9. Auto-commit: `tutor: studied Modern Robotics Ch. 2 (configuration space)`.

- [ ] **Step 4: Verify the artifacts**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: all 31 tests PASS.

- [ ] **Step 5: Spot-check the produced concept page**

Open the new/extended C-space concept page in Obsidian (or `cat` it). Verify subjectively:

- It includes an **everyday analogy** for what C-space is (e.g., "the set of all positions a hand can hold a phone — the phone's 6 degrees of freedom in 3D space form its C-space"), and **explicitly states where the analogy breaks down**.
- It includes a visual — most likely inline SVG showing a simple C-space example (a 2-link arm and its 2D configuration torus, or similar).
- It contains a `## Bridges from` section recording the analogy.
- It wikilinks back to `[[Modern Robotics - Lynch & Park]]` and cites the chapter/page range.

If any of these are missing, the `/tutor` skill is not applying its protocol correctly — file a bug against the SKILL.md and fix.

- [ ] **Step 6: Verify the tutor's auto-commit**

```bash
cd /home/hayman/Workspace/EmbodiedAILab && git log --oneline -3
```

Expected: the most recent commit starts with `tutor:` and mentions Chapter 2.

- [ ] **Step 7: Commit the new tests**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add tests/test_tutor_artifacts.py
git commit -m "Add structural validators for Chapter 2 study workflow"
```

---

## Task 8: End-to-end `/tutor explain` validation (matplotlib + analogy + bridges)

The final validation exercises the third major surface of the tutor: an explicit `/tutor <question>` invocation for a topic that doesn't match any trigger phrase, requiring the agent to (a) use an everyday analogy with breakdown, (b) produce a matplotlib plot using the documented convention, (c) record the analogy in a `## Bridges from` section, and (d) auto-commit. This is the live-fire test for the formula-driven visual path.

**Files:**
- Created by tutor: `wiki/concepts/Sigmoid Function.md`, `wiki/assets/sigmoid/sigmoid.py`, `wiki/assets/sigmoid/sigmoid.png`
- Updated by tutor: `wiki/syntheses/learning-tracker.md`
- Modify: `tests/test_tutor_artifacts.py` (append e2e validation tests)

- [ ] **Step 1: Append failing tests for the sigmoid worked example**

Append to `/home/hayman/Workspace/EmbodiedAILab/tests/test_tutor_artifacts.py`:
```python


# ---------- End-to-end: /tutor explain the sigmoid function ----------

SIG_CONCEPT = "wiki/concepts/Sigmoid Function.md"
SIG_PY = "wiki/assets/sigmoid/sigmoid.py"
SIG_PNG = "wiki/assets/sigmoid/sigmoid.png"


def test_sigmoid_concept_exists(vault):
    assert (vault / SIG_CONCEPT).exists()


def test_sigmoid_concept_has_bridges_from_section(vault):
    text = (vault / SIG_CONCEPT).read_text(encoding="utf-8")
    assert "## Bridges from" in text, \
        "concept page must record analogy in '## Bridges from' section"


def test_sigmoid_concept_includes_breakdown_language(vault):
    text = (vault / SIG_CONCEPT).read_text(encoding="utf-8").lower()
    assert "break" in text, \
        "concept page must state where the analogy breaks down"


def test_sigmoid_matplotlib_artifacts_exist(vault):
    assert (vault / SIG_PY).exists(), \
        "matplotlib convention requires the .py script alongside the .png"
    assert (vault / SIG_PNG).exists(), \
        "matplotlib convention requires the .png saved next to the script"


def test_sigmoid_concept_embeds_the_png(vault):
    text = (vault / SIG_CONCEPT).read_text(encoding="utf-8")
    # Relative embed from wiki/concepts/ -> wiki/assets/sigmoid/sigmoid.png
    assert "../assets/sigmoid/sigmoid.png" in text or \
        "assets/sigmoid/sigmoid.png" in text, \
        "concept page must embed the generated PNG"


def test_sigmoid_script_writes_png_locally(vault):
    """The .py script should save the PNG via plt.savefig('sigmoid.png',
    ...) — i.e., relative path, so 'cd wiki/assets/sigmoid && python ...'
    works."""
    text = (vault / SIG_PY).read_text(encoding="utf-8")
    assert 'savefig("sigmoid.png"' in text or "savefig('sigmoid.png'" in text, \
        "script must save sigmoid.png locally (no absolute path)"
```

- [ ] **Step 2: Run tests, verify the 6 new tests fail**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: 31 prior PASS + 6 new FAIL.

- [ ] **Step 3: Open Claude Code and invoke `/tutor` for sigmoid**

In Claude Code at `/home/hayman/Workspace/EmbodiedAILab`, run the slash command:

```
/tutor explain the sigmoid function
```

The skill will:

1. Bootstrap (read profile + tracker).
2. Recognize sigmoid as a formula-driven concept → use matplotlib per the convention.
3. Write `wiki/assets/sigmoid/sigmoid.py` (a small numpy + matplotlib script).
4. Run the script via Bash (`cd wiki/assets/sigmoid && python sigmoid.py`) to produce `wiki/assets/sigmoid/sigmoid.png`.
5. Create `wiki/concepts/Sigmoid Function.md` with the everyday analogy (dimmer switch is the canonical one), the breakdown, the definition, the embedded PNG, and a `## Bridges from` section.
6. Update tracker (coverage map, session log).
7. Append a Socratic follow-up (2–3 questions).
8. Auto-commit: `tutor: covered sigmoid function (dimmer-switch analogy, matplotlib plot)`.

- [ ] **Step 4: Verify the artifacts**

Run:
```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/test_tutor_artifacts.py -v
```

Expected: all 37 tests PASS.

- [ ] **Step 5: Visually verify the PNG renders correctly**

Open `wiki/concepts/Sigmoid Function.md` in Obsidian. Verify:

- The sigmoid plot renders inline (not a broken-image icon).
- The plot shows a smooth S-curve from approximately (-6, 0) to (6, 1), with σ(0)=0.5 marked.
- The everyday analogy (dimmer switch) is stated *before* the definition.
- The breakdown is explicit.
- The `## Bridges from` section records the analogy.

If the PNG doesn't render, check the embed path in the concept page matches the file location.

- [ ] **Step 6: Manually run a regression — `/tutor` alone for sticky session**

In a fresh Claude Code session, run just:

```
/tutor
```

(no question). The skill should:

1. Bootstrap silently (read profile + tracker).
2. Greet briefly and surface 1–2 items from "Recommendations" (showing the recommendations the tracker now contains — likely "Modern Robotics Ch. 3" since Ch. 2 is covered).
3. Wait for input — stay sticky in tutor mode until `/tutor stop` or session ends.

If this behavior doesn't match, the bootstrap section of `SKILL.md` needs adjustment.

- [ ] **Step 7: Verify all tutor commits**

```bash
cd /home/hayman/Workspace/EmbodiedAILab && git log --oneline | head -10
```

Expected: at least three `tutor:` commits in recent history (Modern Robotics ingestion, Chapter 2 study, sigmoid explanation).

- [ ] **Step 8: Commit the e2e validation tests**

```bash
cd /home/hayman/Workspace/EmbodiedAILab
git add tests/test_tutor_artifacts.py
git commit -m "Add e2e validators for /tutor explain workflow (sigmoid + matplotlib)"
```

- [ ] **Step 9: Run the full test suite once more for a clean baseline**

```bash
cd /home/hayman/Workspace/EmbodiedAILab && python3 -m pytest tests/ -v
```

Expected: 37 tests PASS. This is the Phase 1 "done" gate.

---

## Phase 1 completion checklist

After Task 8, verify against the spec's §11 Success Criteria:

- [ ] A fresh AI session in any tool can be brought up to speed by loading 3 files (profile + tracker + SKILL.md / AGENTS.md) and answers in a way matching the user's background.
- [ ] `/tutor explain <topic>` produces a direct explanation grounded in the wiki, with an everyday analogy + breakdown, and ends with 1–3 Socratic questions.
- [ ] `ingest <resource>` produces expected artifacts in expected locations with correct frontmatter — without spelling out the workflow.
- [ ] `study Chapter N of <resource>` updates the tracker and auto-commits with a meaningful message.
- [ ] `what should I study next` returns a ranked list with rationale.
- [ ] After a week of actual use, the tracker reflects truth without manual editing. (Cannot be verified at plan-end; this is the longer-term success criterion.)
- [ ] Active-gap concepts are taught with an everyday analogy bridge (or explicit note that none fits), including breakdown.

And against §12 Phase 2 Readiness:

- [ ] Every `wiki/sources/` page has the extended frontmatter (verified by Task 6's tests).
- [ ] `total_pages` set on PDF source pages (verified by Task 6's tests).
- [ ] `wiki/ingestion/<resource> - chapters.md` exists for Modern Robotics with valid page ranges (verified by Task 6).
- [ ] At least one ingestion validated end-to-end (Modern Robotics) — done by Tasks 6 and 7.
