"""Generate a single PDF from all Markdown files in the repository."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path

import markdown
from weasyprint import HTML

from circuit_to_code._version import __version__

# Shown on the PDF cover so a standalone download still points back here.
REPO_URL = "https://github.com/LalatenduMohanty/circuit-to-code"
PROJECT_TAGLINE = (
    "Hands-on electronics lessons toward programming and embedded projects."
)
COPYRIGHT_LINE = "Copyright 2026 Lalatendu Mohanty. Licensed under Apache License 2.0."

# Lesson markdown lives only under lessons/ (numbered modules).
LESSONS_DIR_NAME = "lessons"

# Repo meta docs — keep out of the printable lesson PDF.
SKIP_FILE_NAMES = {
    "readme.md",
}

# Numbered module folders: 01-scratch, 02-spike-prime, 03-circuits, …
_MODULE_DIR_RE = re.compile(r"^(\d+)-(.+)$")


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

.toc {{
  page-break-after: always;
}}

.toc h1 {{
  font-size: 20pt;
  margin-top: 0;
}}

.toc-list {{
  list-style: none;
  padding: 0;
  margin: 0.5em 0 0 0;
}}

.toc-item {{
  margin: 0.25em 0;
  line-height: 1.35;
}}

.toc-item-h1 {{
  margin-top: 0.7em;
  font-weight: 600;
}}

.toc-item-h2 {{
  margin-left: 1.25em;
  font-size: 10.5pt;
  font-weight: 400;
}}

.toc a {{
  color: #1a1a1a;
  text-decoration: none;
}}

.toc a::after {{
  content: leader(".") target-counter(attr(href), page);
}}

.md-section {{
  page-break-before: always;
}}

.md-source {{
  font-size: 9pt;
  color: #666;
  margin: 0 0 1em 0;
}}
"""


@dataclass(frozen=True)
class LessonModule:
    """One course module under lessons/NN-slug/."""

    folder: str
    short_id: str
    order: int
    path: Path


def list_lesson_modules(repo_root: Path) -> list[LessonModule]:
    """Discover numbered lesson modules that contain printable markdown."""
    lessons_root = repo_root / LESSONS_DIR_NAME
    if not lessons_root.is_dir():
        return []

    modules: list[LessonModule] = []
    for entry in lessons_root.iterdir():
        if not entry.is_dir():
            continue
        match = _MODULE_DIR_RE.match(entry.name)
        if not match:
            continue
        has_lesson_md = any(
            path.is_file() and path.name.lower() not in SKIP_FILE_NAMES
            for path in entry.rglob("*.md")
        )
        if not has_lesson_md:
            continue
        modules.append(
            LessonModule(
                folder=entry.name,
                short_id=match.group(2).lower(),
                order=int(match.group(1)),
                path=entry,
            )
        )
    return sorted(modules, key=lambda module: (module.order, module.folder.lower()))


def resolve_lesson_selectors(
    repo_root: Path,
    selectors: list[str],
) -> list[LessonModule]:
    """Resolve user selectors to modules in course order.

    Accepts short id (scratch), folder name (01-scratch), or order number (1).
    """
    modules = list_lesson_modules(repo_root)
    if not modules:
        raise ValueError(
            f"No lesson modules found under {repo_root / LESSONS_DIR_NAME}"
        )

    by_short = {module.short_id: module for module in modules}
    by_folder = {module.folder.lower(): module for module in modules}
    by_order = {str(module.order): module for module in modules}

    selected: list[LessonModule] = []
    seen: set[str] = set()
    unknown: list[str] = []

    for raw in selectors:
        key = raw.strip().lower()
        if not key:
            continue
        module = by_short.get(key) or by_folder.get(key) or by_order.get(key)
        if module is None:
            unknown.append(raw)
            continue
        if module.folder in seen:
            continue
        seen.add(module.folder)
        selected.append(module)

    if unknown:
        valid = ", ".join(f"{module.short_id} ({module.folder})" for module in modules)
        raise ValueError(
            f"Unknown lesson selector(s): {', '.join(unknown)}. Valid: {valid}"
        )
    if not selected:
        raise ValueError("No lessons selected.")

    return sorted(selected, key=lambda module: (module.order, module.folder.lower()))


def find_markdown_files(
    repo_root: Path,
    lessons: list[str] | None = None,
) -> list[Path]:
    """Return lesson markdown under lessons/, sorted by module path order.

    When ``lessons`` is set, only markdown from the matching modules is included.
    """
    if lessons:
        modules = resolve_lesson_selectors(repo_root, lessons)
    else:
        modules = list_lesson_modules(repo_root)

    files: list[Path] = []
    for module in modules:
        module_files = [
            path
            for path in module.path.rglob("*.md")
            if path.is_file() and path.name.lower() not in SKIP_FILE_NAMES
        ]
        module_files.sort(
            key=lambda path: path.relative_to(repo_root).as_posix().lower()
        )
        files.extend(module_files)
    return files


def markdown_title(md_file: Path) -> str:
    """Return the first ATX H1 from a markdown file, or a fallback label."""
    for line in md_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_file.stem.replace("-", " ").replace("_", " ").title()


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


_HEADING_RE = re.compile(r"<h([12])(\s[^>]*)?>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


def _plain_heading_text(inner_html: str) -> str:
    return html.unescape(_TAG_RE.sub("", inner_html)).strip()


def _slug_prefix(md_file: Path, repo_root: Path) -> str:
    rel = md_file.relative_to(repo_root).with_suffix("").as_posix()
    return re.sub(r"[^a-zA-Z0-9]+", "-", rel).strip("-").lower()


def assign_heading_ids(
    body_html: str,
    id_prefix: str,
) -> tuple[str, list[tuple[int, str, str]]]:
    """Give H1/H2 unique ids and return (html, toc entries of level/text/id)."""
    entries: list[tuple[int, str, str]] = []
    counter = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal counter
        level = int(match.group(1))
        attrs = match.group(2) or ""
        inner = match.group(3)
        text = _plain_heading_text(inner)
        if not text:
            return match.group(0)
        counter += 1
        heading_id = f"{id_prefix}-{counter}"
        attrs = re.sub(r"""\s+id\s*=\s*(['"]).*?\1""", "", attrs, flags=re.IGNORECASE)
        entries.append((level, text, heading_id))
        return f'<h{level}{attrs} id="{html.escape(heading_id, quote=True)}">{inner}</h{level}>'

    return _HEADING_RE.sub(replacer, body_html), entries


def build_toc_html(entries: list[tuple[int, str, str]]) -> str:
    if not entries:
        return ""
    items: list[str] = []
    for level, text, heading_id in entries:
        css = "toc-item toc-item-h1" if level == 1 else "toc-item toc-item-h2"
        items.append(
            f'<li class="{css}">'
            f'<a href="#{html.escape(heading_id, quote=True)}">'
            f"{html.escape(text)}</a></li>"
        )
    joined = "\n".join(items)
    return (
        f'<nav class="toc" aria-label="Table of contents">'
        f"<h1>Contents</h1>"
        f'<ul class="toc-list">{joined}</ul>'
        f"</nav>"
    )


def build_html_document(
    repo_root: Path,
    md_files: list[Path],
    version: str | None = None,
    lesson_ids: list[str] | None = None,
) -> str:
    version = version or __version__
    sections: list[str] = []
    toc_entries: list[tuple[int, str, str]] = []

    for md_file in md_files:
        rel = md_file.relative_to(repo_root).as_posix()
        prefix = _slug_prefix(md_file, repo_root)
        body = markdown_to_html(md_file)
        body, entries = assign_heading_ids(body, prefix)
        toc_entries.extend(entries)
        sections.append(
            f'<section class="md-section" id="{html.escape(prefix, quote=True)}">'
            f'<p class="md-source">Source: {html.escape(rel)}</p>'
            f"{body}"
            f"</section>"
        )

    joined = "\n".join(sections)
    toc = build_toc_html(toc_entries)
    tagline = PROJECT_TAGLINE
    title = f"Circuit to Code v{version}"
    if lesson_ids:
        titles = [markdown_title(path) for path in md_files]
        if len(titles) == 1:
            tagline = titles[0]
            title = f"{titles[0]} — Circuit to Code v{version}"
        else:
            tagline = "Selected lessons: " + "; ".join(titles)
            title = f"Circuit to Code ({', '.join(lesson_ids)}) v{version}"

    banner = (
        f'<header class="doc-banner">'
        f"<h1>Circuit to Code</h1>"
        f"<p>{html.escape(tagline)}</p>"
        f"<p>Version {html.escape(version)}</p>"
        f"<p>{html.escape(COPYRIGHT_LINE)}</p>"
        f'<p>Source and updates: <a href="{html.escape(REPO_URL)}">'
        f"{html.escape(REPO_URL)}</a></p>"
        f"</header>"
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>{html.escape(title)}</title>
  <style>{css_for_version(version)}</style>
</head>
<body>
{banner}
{toc}
{joined}
</body>
</html>
"""


def default_output_path(
    repo_root: Path,
    version: str | None = None,
    lesson_ids: list[str] | None = None,
) -> Path:
    version = version or __version__
    if lesson_ids:
        slug = "-".join(lesson_ids)
        return repo_root / "pdf" / f"circuit-to-code-{slug}-v{version}.pdf"
    return repo_root / "pdf" / f"circuit-to-code-v{version}.pdf"


def generate_pdf(
    repo_root: Path,
    output: Path | None = None,
    version: str | None = None,
    lessons: list[str] | None = None,
) -> Path:
    version = version or __version__
    lesson_ids: list[str] | None = None
    if lessons:
        lesson_ids = [
            module.short_id for module in resolve_lesson_selectors(repo_root, lessons)
        ]

    output = output or default_output_path(repo_root, version, lesson_ids=lesson_ids)

    md_files = find_markdown_files(repo_root, lessons=lessons)
    if not md_files:
        raise FileNotFoundError(f"No Markdown files found under {repo_root}")

    print(f"Project version: {version}")
    if lesson_ids:
        print(f"Lessons: {', '.join(lesson_ids)}")
    print(f"Found {len(md_files)} Markdown file(s):")
    for path in md_files:
        print(f"  - {path.relative_to(repo_root)}")

    document = build_html_document(
        repo_root,
        md_files,
        version=version,
        lesson_ids=lesson_ids,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=document, base_url=repo_root.as_uri() + "/").write_pdf(output)
    return output.resolve()
