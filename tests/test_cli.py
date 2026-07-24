"""CLI unit tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from circuit_to_code.cli import find_repo_root, main, parse_args


def test_find_repo_root_from_tests_dir(repo_root: Path) -> None:
    assert find_repo_root(repo_root / "tests") == repo_root


def test_parse_args_output_option(tmp_path: Path) -> None:
    out = tmp_path / "out.pdf"
    args = parse_args(["--repo-root", str(tmp_path), "-o", str(out)])
    assert args.output == out
    assert args.repo_root == tmp_path


def test_main_generates_pdf(repo_root: Path, tmp_path: Path) -> None:
    out = tmp_path / "guide.pdf"
    code = main(["--repo-root", str(repo_root), "-o", str(out)])
    assert code == 0
    assert out.is_file()
    assert out.read_bytes()[:4] == b"%PDF"


def test_main_version_flag_exits() -> None:
    with pytest.raises(SystemExit) as exc:
        parse_args(["--version"])
    assert exc.value.code == 0
