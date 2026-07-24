# SPDX-License-Identifier: Apache-2.0
"""Hatchling custom builder — generate the lesson PDF (no wheel)."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

from hatchling.builders.plugin.interface import BuilderInterface


class PdfBuilder(BuilderInterface):  # type: ignore[type-arg]
    """Build target that writes the versioned lesson PDF under pdf/."""

    PLUGIN_NAME = "custom"

    def get_version_api(self) -> dict[str, Callable[..., Any]]:
        return {"standard": self.build_standard}

    def build_standard(self, directory: str, **build_data: object) -> str:
        del build_data
        project_version = self.metadata.version
        root = Path(self.root)
        src = root / "src"
        if str(src) not in sys.path:
            sys.path.insert(0, str(src))

        from circuit_to_code.pdf import generate_pdf

        # `directory` is set to pdf/ via: hatch build -t custom -d pdf
        output = Path(directory) / f"circuit-to-code-v{project_version}.pdf"
        self.app.display_info(f"Generating PDF (version {project_version}) -> {output}")
        pdf_path = generate_pdf(root, output=output, version=project_version)
        self.app.display_success(f"PDF ready: {pdf_path}")
        return str(pdf_path)
