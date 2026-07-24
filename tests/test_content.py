"""Lesson content and diagram inventory."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from circuit_to_code.pdf import find_markdown_files
from svg_validation import assert_valid_svg

# Explicit curriculum checklist — rename/remove must be intentional.
REQUIRED_DIAGRAMS = [
    "diagrams/symbols-legend.svg",
    "diagrams/circuit-01-led-loop.svg",
    "diagrams/circuit-02-switch.svg",
    "diagrams/circuit-02-tactile-button.svg",
    "diagrams/circuit-03-series-parallel.svg",
    "diagrams/circuit-04-potentiometer.svg",
    "diagrams/circuit-05-photoresistor.svg",
    "diagrams/circuit-06-and-gate.svg",
    "diagrams/circuit-07-capacitor.svg",
    "diagrams/circuit-08-flasher.svg",
]


def test_beginner_markdown_exists(repo_root: Path) -> None:
    assert (repo_root / "beginner.md").is_file()


def test_find_markdown_files_includes_beginner(repo_root: Path) -> None:
    files = find_markdown_files(repo_root)
    names = {path.name for path in files}
    assert "beginner.md" in names


def test_find_markdown_files_skips_meta_docs(repo_root: Path) -> None:
    files = find_markdown_files(repo_root)
    rels = {path.relative_to(repo_root).as_posix() for path in files}
    assert "docs/developer.md" not in rels
    assert "README.md" not in rels
    assert (repo_root / "docs" / "developer.md").is_file()
    assert (repo_root / "README.md").is_file()


@pytest.mark.parametrize("relative", REQUIRED_DIAGRAMS)
def test_required_diagram_exists_and_is_valid(repo_root: Path, relative: str) -> None:
    path = repo_root / relative
    assert path.is_file(), f"Missing diagram: {relative}"
    assert_valid_svg(path)


def test_beginner_references_existing_images(repo_root: Path) -> None:
    text = (repo_root / "beginner.md").read_text(encoding="utf-8")
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert refs, "beginner.md should embed schematic images"
    for ref in refs:
        if ref.startswith(("http://", "https://")):
            continue
        target = (repo_root / ref).resolve()
        assert target.is_file(), f"Broken image reference: {ref}"
        if target.suffix.lower() == ".svg":
            assert_valid_svg(target)
