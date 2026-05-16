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
