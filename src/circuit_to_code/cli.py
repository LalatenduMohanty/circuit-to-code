"""Command-line interface for PDF generation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from circuit_to_code._version import __version__
from circuit_to_code.pdf import default_output_path, generate_pdf


def find_repo_root(start: Path | None = None) -> Path:
    """Walk upward until pyproject.toml / version.py is found."""
    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if (candidate / "pyproject.toml").exists() and (
            candidate / "version.py"
        ).exists():
            return candidate
    # Fallback: repository layout relative to this package (src/<pkg>/cli.py)
    return Path(__file__).resolve().parents[2]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="circuit-to-code",
        description=(
            "Generate a single PDF from all Markdown files in this repository "
            f"(version {__version__})."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"circuit-to-code {__version__}",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root to scan (default: auto-detect)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output PDF path (default: <repo-root>/pdf/circuit-to-code-vX.Y.Z.pdf)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = (
        args.repo_root.resolve() if args.repo_root is not None else find_repo_root()
    )
    output = (
        args.output.resolve()
        if args.output is not None
        else default_output_path(repo_root, __version__)
    )

    pdf_path = generate_pdf(repo_root, output=output, version=__version__)
    print(f"Wrote PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
