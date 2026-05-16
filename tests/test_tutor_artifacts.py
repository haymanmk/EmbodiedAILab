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
