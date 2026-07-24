"""SVG diagram validation helpers for lesson content tests.

Layers (cheap → stricter):
1. Encoding — UTF-8, no binary/control garbage
2. Well-formed XML — catches unescaped ``<`` / ``&`` in text (e.g. ``A <-> B``)
3. SVG contract — root element, namespace, and sizing attributes
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
_ALLOWED_CONTROLS = {"\t", "\n", "\r"}


def validate_svg_bytes(data: bytes, *, label: str = "<memory>") -> list[str]:
    """Return human-readable issues; empty list means the SVG looks healthy."""
    issues: list[str] = []

    if not data:
        return [f"{label}: file is empty"]
    if len(data) < 32:
        issues.append(f"{label}: file too small ({len(data)} bytes) to be a real SVG")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"{label}: not valid UTF-8 ({exc})"]

    for index, char in enumerate(text):
        code = ord(char)
        if code < 32 and char not in _ALLOWED_CONTROLS:
            issues.append(
                f"{label}: forbidden control character U+{code:04X} at offset {index}"
            )
            break

    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        issues.append(
            f"{label}: not well-formed XML ({exc}). "
            "Common cause: raw '<' or '&' inside text — escape as &lt; / &amp; "
            "(e.g. write 'A to B' instead of 'A <-> B')."
        )
        return issues

    local_name = root.tag.rsplit("}", 1)[-1]
    if local_name != "svg":
        issues.append(f"{label}: root element is <{local_name}>, expected <svg>")

    namespaced = root.tag == f"{{{SVG_NS}}}svg"
    xmlns_attr = root.get("xmlns") == SVG_NS
    if not namespaced and not xmlns_attr:
        issues.append(f'{label}: missing SVG namespace (expected xmlns="{SVG_NS}")')

    view_box = root.get("viewBox") or root.get("viewbox")
    width = root.get("width")
    height = root.get("height")
    if not view_box and not (width and height):
        issues.append(
            f"{label}: needs a viewBox (preferred) or both width and height "
            "so renderers can size the diagram"
        )

    if len(root) == 0:
        issues.append(f"{label}: <svg> has no child content")

    return issues


def validate_svg_path(path: Path) -> list[str]:
    """Validate an on-disk SVG; label issues with the path name."""
    if not path.is_file():
        return [f"{path}: file does not exist"]
    return validate_svg_bytes(path.read_bytes(), label=path.as_posix())


def discover_svg_files(repo_root: Path) -> list[Path]:
    """All lesson SVGs under diagrams/ (sorted for stable pytest IDs)."""
    diagrams = repo_root / "diagrams"
    if not diagrams.is_dir():
        return []
    return sorted(diagrams.rglob("*.svg"))


def assert_valid_svg(path: Path) -> None:
    """Pytest-friendly assertion with a multi-line failure message."""
    issues = validate_svg_path(path)
    assert not issues, "Broken SVG:\n" + "\n".join(f"  - {item}" for item in issues)
