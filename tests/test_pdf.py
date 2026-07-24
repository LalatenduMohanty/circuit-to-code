"""PDF generation unit tests."""

from __future__ import annotations

from pathlib import Path

from circuit_to_code.pdf import (
    build_html_document,
    css_for_version,
    default_output_path,
    find_markdown_files,
    generate_pdf,
    markdown_to_html,
)


def test_default_output_path_includes_version(repo_root: Path) -> None:
    path = default_output_path(repo_root, "1.2.3")
    assert path == repo_root / "pdf" / "circuit-to-code-v1.2.3.pdf"


def test_css_mentions_version() -> None:
    css = css_for_version("9.9.9")
    assert "Version 9.9.9" in css


def test_html_document_includes_version_banner(repo_root: Path) -> None:
    md_files = find_markdown_files(repo_root)
    document = build_html_document(repo_root, md_files, version="0.1.0")
    assert "Version 0.1.0" in document
    assert "Circuit to Code" in document
    assert 'class="doc-banner"' in document


def test_markdown_to_html_rewrites_local_images(repo_root: Path) -> None:
    beginner = repo_root / "beginner.md"
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
