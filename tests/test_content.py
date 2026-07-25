"""Lesson content and diagram inventory."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from circuit_to_code.pdf import find_markdown_files
from svg_validation import assert_valid_svg

# Explicit curriculum checklist — rename/remove must be intentional.
REQUIRED_DIAGRAMS = [
    "lessons/03-circuits/diagrams/symbols-legend.svg",
    "lessons/03-circuits/diagrams/circuit-01-led-loop.svg",
    "lessons/03-circuits/diagrams/circuit-02-switch.svg",
    "lessons/03-circuits/diagrams/circuit-02-tactile-button.svg",
    "lessons/03-circuits/diagrams/circuit-03-series-parallel.svg",
    "lessons/03-circuits/diagrams/circuit-04-potentiometer.svg",
    "lessons/03-circuits/diagrams/circuit-05-photoresistor.svg",
    "lessons/03-circuits/diagrams/circuit-06-and-gate.svg",
    "lessons/03-circuits/diagrams/circuit-07-capacitor.svg",
    "lessons/03-circuits/diagrams/circuit-08-flasher.svg",
    "lessons/03-circuits/diagrams/intermediate-symbols-legend.svg",
    "lessons/03-circuits/diagrams/intermediate-circuit-01-transistor-load.svg",
    "lessons/03-circuits/diagrams/intermediate-circuit-02-diode.svg",
    "lessons/03-circuits/diagrams/intermediate-circuit-03-voltage-divider.svg",
    "lessons/03-circuits/diagrams/intermediate-circuit-04-motor-driver.svg",
    "lessons/03-circuits/diagrams/intermediate-circuit-05-pwm-throttle.svg",
    "lessons/04-microbit/diagrams/microbit-v2-overview.jpg",
    "lessons/07-robot-missions/diagrams/program-flow.svg",
    "lessons/07-robot-missions/diagrams/brain-vs-motors.svg",
    "lessons/07-robot-missions/diagrams/motor-counter.svg",
]

LESSON_FILES = [
    "lessons/01-scratch/scratch-programming.md",
    "lessons/02-spike-prime/spike-prime.md",
    "lessons/03-circuits/beginner.md",
    "lessons/03-circuits/intermediate.md",
    "lessons/04-microbit/microbit-v2.md",
    "lessons/05-circuitpython/circuitpython.md",
    "lessons/06-arduino/arduino.md",
    "lessons/07-robot-missions/robot-missions.md",
]


def test_lesson_markdown_files_exist(repo_root: Path) -> None:
    for relative in LESSON_FILES:
        assert (repo_root / relative).is_file(), f"Missing lesson: {relative}"


def test_find_markdown_files_includes_lessons_in_course_order(repo_root: Path) -> None:
    files = find_markdown_files(repo_root)
    rels = [path.relative_to(repo_root).as_posix() for path in files]
    assert rels == LESSON_FILES


def test_find_markdown_files_filters_to_one_module(repo_root: Path) -> None:
    files = find_markdown_files(repo_root, lessons=["microbit"])
    rels = [path.relative_to(repo_root).as_posix() for path in files]
    assert rels == ["lessons/04-microbit/microbit-v2.md"]


def test_find_markdown_files_circuits_includes_both_sections(repo_root: Path) -> None:
    files = find_markdown_files(repo_root, lessons=["circuits"])
    rels = [path.relative_to(repo_root).as_posix() for path in files]
    assert rels == [
        "lessons/03-circuits/beginner.md",
        "lessons/03-circuits/intermediate.md",
    ]


def test_find_markdown_files_skips_meta_docs(repo_root: Path) -> None:
    files = find_markdown_files(repo_root)
    rels = {path.relative_to(repo_root).as_posix() for path in files}
    assert "docs/developer.md" not in rels
    assert "README.md" not in rels
    assert "lessons/README.md" not in rels
    assert (repo_root / "docs" / "developer.md").is_file()
    assert (repo_root / "README.md").is_file()
    assert (repo_root / "lessons" / "README.md").is_file()


@pytest.mark.parametrize("relative", REQUIRED_DIAGRAMS)
def test_required_diagram_exists(repo_root: Path, relative: str) -> None:
    path = repo_root / relative
    assert path.is_file(), f"Missing diagram: {relative}"
    if path.suffix.lower() == ".svg":
        assert_valid_svg(path)


@pytest.mark.parametrize(
    "lesson",
    [
        "lessons/03-circuits/beginner.md",
        "lessons/03-circuits/intermediate.md",
        "lessons/04-microbit/microbit-v2.md",
        "lessons/07-robot-missions/robot-missions.md",
    ],
)
def test_lesson_references_existing_images(repo_root: Path, lesson: str) -> None:
    text = (repo_root / lesson).read_text(encoding="utf-8")
    refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    assert refs, f"{lesson} should embed images"
    for ref in refs:
        if ref.startswith(("http://", "https://")):
            continue
        target = ((repo_root / lesson).parent / ref).resolve()
        assert target.is_file(), f"Broken image reference in {lesson}: {ref}"
        if target.suffix.lower() == ".svg":
            assert_valid_svg(target)
