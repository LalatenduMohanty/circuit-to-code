"""Generate a single PDF from all Markdown files in the repository."""

from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
from weasyprint import HTML

from circuit_to_code._version import __version__

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    "node_modules",
    ".tox",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "pdf",
    "src",
    "docs",  # developer docs — not part of the student PDF
}

# Repo meta docs — keep out of the printable lesson PDF.
SKIP_FILE_NAMES = {
    "readme.md",
}


def css_for_version(version: str) -> str:
    return f"""
@page {{
  size: Letter;
  margin: 0.85in 0.75in 1.0in 0.75in;

  @bottom-left {{
    content: "Circuit to Code";
    font-size: 9pt;
    color: #666;
  }}

  @bottom-center {{
    content: "Version {version}";
    font-size: 9pt;
    color: #666;
  }}

  @bottom-right {{
    content: "Page " counter(page);
    font-size: 9pt;
    color: #666;
  }}
}}

body {{
  font-family: "Segoe UI", Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #1a1a1a;
}}

.doc-banner {{
  border: 1px solid #ccc;
  background: #f7f7f7;
  padding: 0.75em 1em;
  margin: 0 0 1.25em 0;
  page-break-after: avoid;
}}

.doc-banner h1 {{
  margin: 0 0 0.25em 0;
  font-size: 18pt;
  border: none;
  padding: 0;
}}

.doc-banner p {{
  margin: 0.15em 0;
  color: #444;
}}

h1, h2, h3, h4 {{
  color: #111;
  page-break-after: avoid;
}}

h1 {{
  font-size: 22pt;
  border-bottom: 2px solid #333;
  padding-bottom: 0.2em;
}}

h2 {{
  font-size: 16pt;
  margin-top: 1.4em;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.15em;
}}

h3 {{
  font-size: 13pt;
  margin-top: 1.2em;
}}

h4 {{
  font-size: 11.5pt;
}}

img {{
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0.8em 0;
  page-break-inside: avoid;
}}

table {{
  border-collapse: collapse;
  width: 100%;
  margin: 0.8em 0;
  font-size: 10pt;
  page-break-inside: avoid;
}}

th, td {{
  border: 1px solid #bbb;
  padding: 0.35em 0.55em;
  text-align: left;
  vertical-align: top;
}}

th {{
  background: #f0f0f0;
}}

code {{
  font-family: "Consolas", "Courier New", monospace;
  font-size: 0.92em;
  background: #f4f4f4;
  padding: 0.1em 0.3em;
  border-radius: 3px;
}}

pre {{
  background: #f4f4f4;
  padding: 0.75em;
  overflow-x: auto;
  font-size: 9.5pt;
  page-break-inside: avoid;
}}

pre code {{
  background: transparent;
  padding: 0;
}}

blockquote {{
  margin: 0.8em 0;
  padding: 0.4em 0.8em;
  border-left: 4px solid #888;
  background: #f8f8f8;
  color: #333;
}}

hr {{
  border: none;
  border-top: 1px solid #ccc;
  margin: 1.5em 0;
}}

.md-section {{
  page-break-before: always;
}}

.md-section:first-of-type {{
  page-break-before: avoid;
}}

.md-source {{
  font-size: 9pt;
  color: #666;
  margin: 0 0 1em 0;
}}
"""


def find_markdown_files(repo_root: Path) -> list[Path]:
    """Return markdown files under repo_root, sorted for a sensible PDF order."""
    files: list[Path] = []
    for path in repo_root.rglob("*.md"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.name.lower() in SKIP_FILE_NAMES:
            continue
        files.append(path)

    def sort_key(path: Path) -> tuple[int, str]:
        rel = path.relative_to(repo_root).as_posix().lower()
        name = path.name.lower()
        if name.startswith("beginner"):
            group = 0
        elif name in {"index.md"}:
            group = 1
        else:
            group = 2
        return (group, rel)

    return sorted(files, key=sort_key)


def rewrite_image_sources(html_fragment: str, md_file: Path) -> str:
    """Point relative image paths at absolute file URIs for WeasyPrint."""

    def replacer(match: re.Match[str]) -> str:
        prefix, src, suffix = match.group(1), match.group(2), match.group(3)
        if src.startswith(("http://", "https://", "data:", "file:")):
            return match.group(0)
        image_path = (md_file.parent / src).resolve()
        return f"{prefix}{image_path.as_uri()}{suffix}"

    return re.sub(
        r'(<img\b[^>]*\bsrc=["\'])([^"\']+)(["\'])',
        replacer,
        html_fragment,
        flags=re.IGNORECASE,
    )


def markdown_to_html(md_file: Path) -> str:
    text = md_file.read_text(encoding="utf-8")
    body = markdown.markdown(
        text,
        extensions=[
            "extra",
            "sane_lists",
            "tables",
            "fenced_code",
            "toc",
        ],
    )
    return rewrite_image_sources(body, md_file)


def build_html_document(
    repo_root: Path,
    md_files: list[Path],
    version: str | None = None,
) -> str:
    version = version or __version__
    sections: list[str] = []
    for md_file in md_files:
        rel = md_file.relative_to(repo_root).as_posix()
        body = markdown_to_html(md_file)
        sections.append(
            f'<section class="md-section">'
            f'<p class="md-source">Source: {html.escape(rel)}</p>'
            f"{body}"
            f"</section>"
        )

    joined = "\n".join(sections)
    banner = (
        f'<header class="doc-banner">'
        f"<h1>Circuit to Code</h1>"
        f"<p>Version {html.escape(version)}</p>"
        f"<p>Generated from Markdown lessons in this repository.</p>"
        f"</header>"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Circuit to Code v{html.escape(version)}</title>
  <style>{css_for_version(version)}</style>
</head>
<body>
{banner}
{joined}
</body>
</html>
"""


def default_output_path(repo_root: Path, version: str | None = None) -> Path:
    version = version or __version__
    return repo_root / "pdf" / f"circuit-to-code-v{version}.pdf"


def generate_pdf(
    repo_root: Path,
    output: Path | None = None,
    version: str | None = None,
) -> Path:
    version = version or __version__
    output = output or default_output_path(repo_root, version)

    md_files = find_markdown_files(repo_root)
    if not md_files:
        raise FileNotFoundError(f"No Markdown files found under {repo_root}")

    print(f"Project version: {version}")
    print(f"Found {len(md_files)} Markdown file(s):")
    for path in md_files:
        print(f"  - {path.relative_to(repo_root)}")

    document = build_html_document(repo_root, md_files, version=version)
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=document, base_url=repo_root.as_uri() + "/").write_pdf(output)
    return output.resolve()
