"""Version consistency checks."""

from __future__ import annotations

import ast
from pathlib import Path

from circuit_to_code import __version__ as package_version


def test_version_py_defines_semver(repo_root: Path) -> None:
    version_py = repo_root / "version.py"
    tree = ast.parse(version_py.read_text(encoding="utf-8"))
    values = [
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        for target in node.targets
        if isinstance(target, ast.Name) and target.id == "__version__"
    ]
    assert values, "__version__ missing from version.py"
    version = values[0]
    parts = version.split(".")
    assert len(parts) >= 2
    assert all(part.isdigit() for part in parts[:2])


def test_package_version_matches_version_py(repo_root: Path) -> None:
    ns: dict[str, object] = {}
    exec((repo_root / "version.py").read_text(encoding="utf-8"), ns)
    assert package_version == ns["__version__"]
