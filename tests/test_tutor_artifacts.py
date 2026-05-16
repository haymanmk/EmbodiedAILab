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
