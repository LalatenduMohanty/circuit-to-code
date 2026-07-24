"""Resolve the project version from install metadata or version.py."""

from __future__ import annotations

import ast
from pathlib import Path


def _read_version_file() -> str:
    # src/circuit_to_code/_version.py -> repo root
    version_py = Path(__file__).resolve().parents[2] / "version.py"
    tree = ast.parse(version_py.read_text(encoding="utf-8"), filename=str(version_py))
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__version__":
                    value = ast.literal_eval(node.value)
                    if not isinstance(value, str):
                        raise TypeError(
                            f"__version__ must be a string, got {type(value).__name__}"
                        )
                    return value
    raise RuntimeError(f"__version__ not found in {version_py}")


def get_version() -> str:
    try:
        from importlib.metadata import version

        return version("circuit-to-code")
    except Exception:
        return _read_version_file()


__version__ = get_version()
