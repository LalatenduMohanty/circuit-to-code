"""Ensure the Hatch custom PDF build keeps working."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest


def test_hatch_custom_builder_imports(repo_root: Path) -> None:
    pytest.importorskip("hatchling")
    sys.path.insert(0, str(repo_root))
    import hatch_build

    assert hasattr(hatch_build, "PdfBuilder")
    assert hatch_build.PdfBuilder.PLUGIN_NAME == "custom"


def test_hatch_build_custom_pdf(repo_root: Path) -> None:
    env = os.environ.copy()
    env["HATCH_DATA_DIR"] = str(repo_root / ".hatch")

    result = subprocess.run(
        ["hatch", "build", "-t", "custom", "pdf"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"hatch build failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    version_ns: dict[str, object] = {}
    exec((repo_root / "version.py").read_text(encoding="utf-8"), version_ns)
    version = version_ns["__version__"]
    pdf_path = repo_root / "pdf" / f"circuit-to-code-v{version}.pdf"
    assert pdf_path.is_file()
    assert pdf_path.read_bytes()[:4] == b"%PDF"
    assert pdf_path.stat().st_size > 10_000
