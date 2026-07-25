"""PDF generation unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from circuit_to_code.pdf import (
    COPYRIGHT_LINE,
    PROJECT_TAGLINE,
    REPO_URL,
    build_html_document,
    css_for_version,
    default_output_path,
    find_markdown_files,
    generate_pdf,
    list_lesson_modules,
    markdown_to_html,
    resolve_lesson_selectors,
)


def test_default_output_path_includes_version(repo_root: Path) -> None:
    path = default_output_path(repo_root, "1.2.3")
    assert path == repo_root / "pdf" / "circuit-to-code-v1.2.3.pdf"


def test_default_output_path_includes_lesson_slug(repo_root: Path) -> None:
    path = default_output_path(repo_root, "1.2.3", lesson_ids=["scratch"])
    assert path == repo_root / "pdf" / "circuit-to-code-scratch-v1.2.3.pdf"
    multi = default_output_path(
        repo_root, "1.2.3", lesson_ids=["scratch", "circuits"]
    )
    assert multi == repo_root / "pdf" / "circuit-to-code-scratch-circuits-v1.2.3.pdf"


def test_css_mentions_version() -> None:
    css = css_for_version("9.9.9")
    assert "Version 9.9.9" in css


def test_list_lesson_modules_discovers_three(repo_root: Path) -> None:
    modules = list_lesson_modules(repo_root)
    assert [m.short_id for m in modules] == ["scratch", "circuits", "microbit"]
    assert [m.folder for m in modules] == [
        "01-scratch",
        "02-circuits",
        "03-microbit",
    ]


@pytest.mark.parametrize(
    "selector,expected",
    [
        ("scratch", "scratch"),
        ("01-scratch", "scratch"),
        ("1", "scratch"),
        ("circuits", "circuits"),
        ("02-circuits", "circuits"),
        ("2", "circuits"),
        ("microbit", "microbit"),
        ("03-microbit", "microbit"),
        ("3", "microbit"),
    ],
)
def test_resolve_lesson_selectors_aliases(
    repo_root: Path, selector: str, expected: str
) -> None:
    modules = resolve_lesson_selectors(repo_root, [selector])
    assert [m.short_id for m in modules] == [expected]


def test_resolve_lesson_selectors_dedupes_and_orders(repo_root: Path) -> None:
    modules = resolve_lesson_selectors(
        repo_root, ["microbit", "scratch", "1", "01-scratch"]
    )
    assert [m.short_id for m in modules] == ["scratch", "microbit"]


def test_resolve_lesson_selectors_unknown(repo_root: Path) -> None:
    with pytest.raises(ValueError, match="Unknown lesson selector"):
        resolve_lesson_selectors(repo_root, ["not-a-lesson"])


def test_find_markdown_files_filters_by_lesson(repo_root: Path) -> None:
    files = find_markdown_files(repo_root, lessons=["circuits"])
    rels = [path.relative_to(repo_root).as_posix() for path in files]
    assert rels == ["lessons/02-circuits/beginner.md"]


def test_html_document_includes_version_banner(repo_root: Path) -> None:
    md_files = find_markdown_files(repo_root)
    document = build_html_document(repo_root, md_files, version="0.1.0")
    assert "Version 0.1.0" in document
    assert "Circuit to Code" in document
    assert 'class="doc-banner"' in document
    assert PROJECT_TAGLINE in document
    assert COPYRIGHT_LINE in document
    assert REPO_URL in document
    assert f'href="{REPO_URL}"' in document


def test_html_document_includes_table_of_contents(repo_root: Path) -> None:
    md_files = find_markdown_files(repo_root)
    document = build_html_document(repo_root, md_files, version="0.2.0")
    assert 'class="toc"' in document
    assert "<h1>Contents</h1>" in document
    assert "Learning Scratch Programming" in document
    assert "Beginner Circuits" in document
    assert "Guide to micro:bit V2" in document
    assert "target-counter(attr(href), page)" in document
    assert 'href="#lessons-01-scratch-scratch-programming-1"' in document


def test_filtered_html_includes_only_selected_lesson(repo_root: Path) -> None:
    md_files = find_markdown_files(repo_root, lessons=["scratch"])
    document = build_html_document(
        repo_root, md_files, version="0.2.0", lesson_ids=["scratch"]
    )
    assert "Learning Scratch Programming" in document
    assert "Source: lessons/01-scratch/scratch-programming.md" in document
    assert "Source: lessons/02-circuits/beginner.md" not in document
    assert "Source: lessons/03-microbit/microbit-v2.md" not in document
    assert 'id="lessons-02-circuits-beginner-1"' not in document
    assert PROJECT_TAGLINE not in document


def test_markdown_to_html_rewrites_local_images(repo_root: Path) -> None:
    beginner = repo_root / "lessons" / "02-circuits" / "beginner.md"
    html = markdown_to_html(beginner)
    assert "file://" in html
    assert "symbols-legend.svg" in html


def test_generate_pdf_writes_valid_versioned_file(
    repo_root: Path, tmp_path: Path
) -> None:
    version = "0.1.0"
    output = tmp_path / f"circuit-to-code-v{version}.pdf"
    pdf_path = generate_pdf(repo_root, output=output, version=version)

    assert pdf_path == output.resolve()
    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 10_000
    assert pdf_path.read_bytes()[:4] == b"%PDF"


def test_generate_pdf_filtered_default_name(
    repo_root: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    version = "0.1.0"
    # Keep lesson content from the real repo, but write the default PDF under tmp.
    monkeypatch.setattr(
        "circuit_to_code.pdf.default_output_path",
        lambda _root, ver=None, lesson_ids=None: (
            tmp_path
            / (
                f"circuit-to-code-{'-'.join(lesson_ids)}-v{ver or version}.pdf"
                if lesson_ids
                else f"circuit-to-code-v{ver or version}.pdf"
            )
        ),
    )
    pdf_path = generate_pdf(repo_root, version=version, lessons=["scratch"])
    assert pdf_path.name == f"circuit-to-code-scratch-v{version}.pdf"
    assert pdf_path.is_file()
    assert pdf_path.read_bytes()[:4] == b"%PDF"
