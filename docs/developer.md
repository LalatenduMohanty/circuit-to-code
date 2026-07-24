# Developer guide

Notes for working on this repository (tooling, tests, PDF build). Lesson content lives
in `beginner.md`, not here.

## Prerequisites

- Python 3.10+
- [Hatch](https://hatch.pypa.io/) (`pip install hatch`)
- System libraries for WeasyPrint when generating PDFs (see CI workflow)

Project dependencies are declared in `pyproject.toml`.

## How to run

### Tests

```bash
hatch run test                 # pytest
hatch run build                # tests, then PDF into pdf/
```

### PDF only

```bash
hatch run pdf
hatch build -t custom pdf
```

### Lint / format / type-check

```bash
hatch run lint:check           # CI gate (no writes)
hatch run lint:fmt             # auto-fix Ruff + mdformat
hatch run lint:py              # ruff check
hatch run lint:py-format       # ruff format --check
hatch run lint:types           # mypy
hatch run lint:md              # mdformat --check
```

Optional extras (same tools without Hatch scripts):

```bash
pip install -e ".[lint]"
```

## Tooling overview

| Tool                            | Role                  | Config                                       |
| ------------------------------- | --------------------- | -------------------------------------------- |
| **Ruff**                        | Python lint + format  | `pyproject.toml` `[tool.ruff]`               |
| **mypy**                        | Strict type checking  | `pyproject.toml` `[tool.mypy]`               |
| **mdformat** + **mdformat-gfm** | Markdown format (GFM) | `.mdformat.toml`                             |
| **pytest**                      | Unit tests            | `pyproject.toml` `[tool.pytest.ini_options]` |

mdformat 1.x reads **`.mdformat.toml`** (not `[tool.mdformat]` in `pyproject.toml`).

## Layout

| Path                   | Purpose                                       |
| ---------------------- | --------------------------------------------- |
| `beginner.md`          | Lesson content                                |
| `diagrams/`            | SVG schematics embedded by the lessons        |
| `src/circuit_to_code/` | PDF generation package                        |
| `tests/`               | pytest suite (including SVG validation)       |
| `docs/`                | Developer docs (excluded from the lesson PDF) |
| `pdf/`                 | Generated PDF output (gitignored)             |

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs:

1. `hatch run lint:check`
2. `hatch run test`

## SVG diagrams

Lesson SVGs under `diagrams/` must be well-formed XML (UTF-8, valid `<svg>`). Tests in
`tests/test_svg_diagrams.py` catch common breaks such as raw `<` in text (`A <-> B` →
use `A to B` or `&lt;`).
