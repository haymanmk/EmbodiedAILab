"""Structural validators for the AI tutor system artifacts.

Tests are organized by artifact in the order they appear in the
implementation plan: profile, tracker, AGENTS.md, /tutor skill,
first ingestion.

Each test asserts STRUCTURAL correctness (file exists, required
sections present, frontmatter fields valid). They deliberately do
NOT assert specific wording — that would be too brittle for
content-heavy markdown.
"""
