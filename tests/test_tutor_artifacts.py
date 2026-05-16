"""Structural validators for the AI tutor system artifacts.

Tests are organized by artifact in the order they appear in the
implementation plan: profile, tracker, AGENTS.md, /tutor skill,
first ingestion.

Each test asserts STRUCTURAL correctness (file exists, required
sections present, frontmatter fields valid). They deliberately do
NOT assert specific wording — that would be too brittle for
content-heavy markdown.
"""


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
