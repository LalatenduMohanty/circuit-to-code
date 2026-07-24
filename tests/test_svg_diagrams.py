"""Architected SVG integrity tests.

Goal: fail CI when a lesson diagram cannot be parsed/rendered, including the
regression where raw ``<`` in text (e.g. ``A <-> B``) produces invalid XML.

Test strategy
-------------
* Contract unit tests — synthetic fixtures prove each validation layer fires.
* Repo inventory — every ``diagrams/**/*.svg`` must pass validation.
* Markdown coupling — every local ``![](...svg)`` in lessons must exist and
  pass the same validator (prevents “file exists but is broken”).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from svg_validation import (
    SVG_NS,
    assert_valid_svg,
    discover_svg_files,
    validate_svg_bytes,
    validate_svg_path,
)

_REPO_ROOT = Path(__file__).resolve().parents[1]
_REPO_SVGS = discover_svg_files(_REPO_ROOT)

# Minimal healthy SVG used as a baseline for mutation tests.
_VALID_SVG = f"""\
<svg xmlns="{SVG_NS}" viewBox="0 0 100 40">
  <rect width="100" height="40" fill="#fafafa"/>
  <text x="8" y="24" font-size="12">OK</text>
</svg>
"""


def _issues_matching(issues: list[str], fragment: str) -> bool:
    return any(fragment in item for item in issues)


# ---------------------------------------------------------------------------
# Layer contract tests (negative fixtures — the safety net)
# ---------------------------------------------------------------------------


def test_accepts_minimal_valid_svg() -> None:
    assert validate_svg_bytes(_VALID_SVG.encode("utf-8")) == []


def test_rejects_unescaped_less_than_in_text() -> None:
    """Historical bug: ``A <-> B`` breaks XML because ``<`` starts a tag."""
    broken = _VALID_SVG.replace(">OK</text>", ">A <-> B</text>")
    issues = validate_svg_bytes(broken.encode("utf-8"), label="bad-arrows.svg")
    assert _issues_matching(issues, "not well-formed XML"), issues
    assert _issues_matching(issues, "escape as &lt;"), issues


def test_rejects_unescaped_ampersand_in_text() -> None:
    broken = _VALID_SVG.replace(">OK</text>", ">R1 & R2</text>")
    issues = validate_svg_bytes(broken.encode("utf-8"), label="bad-amp.svg")
    assert _issues_matching(issues, "not well-formed XML"), issues


def test_rejects_truncated_markup() -> None:
    issues = validate_svg_bytes(
        b"<svg xmlns='http://www.w3.org/2000/svg'><rect",
        label="trunc.svg",
    )
    assert _issues_matching(issues, "not well-formed XML"), issues


def test_rejects_non_utf8_bytes() -> None:
    # CP1252 byte that is not valid UTF-8
    payload = (
        b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
        b"<text>\x94</text></svg>"
    )
    issues = validate_svg_bytes(payload, label="latin1.svg")
    assert _issues_matching(issues, "not valid UTF-8"), issues


def test_rejects_control_characters() -> None:
    broken = _VALID_SVG.replace("OK", "OK\x14bad")
    issues = validate_svg_bytes(broken.encode("utf-8"), label="ctrl.svg")
    assert _issues_matching(issues, "forbidden control character"), issues


def test_rejects_empty_file() -> None:
    issues = validate_svg_bytes(b"", label="empty.svg")
    assert _issues_matching(issues, "empty"), issues


def test_rejects_non_svg_root() -> None:
    html = b"<html xmlns='http://www.w3.org/1999/xhtml'><body/></html>"
    issues = validate_svg_bytes(html, label="html.svg")
    assert _issues_matching(issues, "expected <svg>"), issues


def test_rejects_missing_namespace() -> None:
    bare = b'<svg viewBox="0 0 10 10"><rect width="10" height="10"/></svg>'
    issues = validate_svg_bytes(bare, label="no-ns.svg")
    assert _issues_matching(issues, "missing SVG namespace"), issues


def test_rejects_missing_viewbox_and_dimensions() -> None:
    bare = f'<svg xmlns="{SVG_NS}"><rect width="10" height="10"/></svg>'.encode()
    issues = validate_svg_bytes(bare, label="no-size.svg")
    assert _issues_matching(issues, "viewBox"), issues


def test_rejects_svg_with_no_children() -> None:
    empty = f'<svg xmlns="{SVG_NS}" viewBox="0 0 10 10"></svg>'.encode()
    issues = validate_svg_bytes(empty, label="no-kids.svg")
    assert _issues_matching(issues, "no child content"), issues


def test_escaped_less_than_in_text_is_allowed() -> None:
    """Properly escaped arrows must remain valid."""
    good = _VALID_SVG.replace(">OK</text>", ">A &lt;-&gt; B</text>")
    assert validate_svg_bytes(good.encode("utf-8")) == []


def test_validate_svg_path_missing_file(tmp_path: Path) -> None:
    missing = tmp_path / "nope.svg"
    issues = validate_svg_path(missing)
    assert _issues_matching(issues, "does not exist"), issues


def test_assert_valid_svg_raises_for_broken(tmp_path: Path) -> None:
    path = tmp_path / "broken.svg"
    path.write_text(_VALID_SVG.replace("OK", "A <-> B"), encoding="utf-8")
    with pytest.raises(AssertionError, match="not well-formed XML"):
        assert_valid_svg(path)


def test_assert_valid_svg_passes_for_good(tmp_path: Path) -> None:
    path = tmp_path / "good.svg"
    path.write_text(_VALID_SVG, encoding="utf-8")
    assert_valid_svg(path)


# ---------------------------------------------------------------------------
# Repository inventory (positive — all shipped diagrams)
# ---------------------------------------------------------------------------


def test_diagrams_directory_has_svgs() -> None:
    assert _REPO_SVGS, "expected at least one SVG under diagrams/"


@pytest.mark.parametrize(
    "svg_path",
    _REPO_SVGS,
    ids=[path.relative_to(_REPO_ROOT).as_posix() for path in _REPO_SVGS],
)
def test_each_diagram_svg_is_valid(svg_path: Path) -> None:
    assert_valid_svg(svg_path)


def test_markdown_svg_references_are_valid(repo_root: Path) -> None:
    """Every local SVG embedded from Markdown must pass validation."""
    md_files = sorted(
        path
        for path in repo_root.rglob("*.md")
        if ".hatch" not in path.parts and "node_modules" not in path.parts
    )
    pattern = re.compile(r"!\[[^\]]*\]\(([^)]+\.svg)\)", re.IGNORECASE)
    refs: list[tuple[Path, str]] = []
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        for ref in pattern.findall(text):
            if ref.startswith(("http://", "https://")):
                continue
            refs.append((md_file, ref))

    assert refs, "expected Markdown lessons to embed at least one SVG"

    failures: list[str] = []
    for md_file, ref in refs:
        target = (md_file.parent / ref).resolve()
        if not target.is_file():
            failures.append(f"{md_file.name}: missing {ref}")
            continue
        for issue in validate_svg_path(target):
            failures.append(f"{md_file.name} -> {ref}: {issue}")

    assert not failures, "Broken Markdown SVG references:\n" + "\n".join(
        f"  - {item}" for item in failures
    )
