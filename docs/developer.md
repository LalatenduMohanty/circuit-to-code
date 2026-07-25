# Developer guide

Notes for working on this repository (tooling, tests, PDF build). Lesson content lives
under `lessons/`, not here.

## Prerequisites

- Python 3.10+
- [Hatch](https://hatch.pypa.io/) (`pip install hatch`)
- System libraries for WeasyPrint when generating PDFs (see CI workflow)

Project dependencies are declared in `pyproject.toml`.

## How to run

### Tests

```bash
hatch run test                 # pytest (PDF tests write under temp dirs)
hatch run pdf -o /tmp/check.pdf   # verify full PDF build without touching pdf/
hatch run build                # tests, then overwrite pdf/circuit-to-code-vX.Y.Z.pdf
```

CI runs unit tests and a temp-path PDF build on every change. Prefer
`hatch run pdf -o …` for day-to-day checks.

### PDF only

```bash
hatch run pdf -o /tmp/check.pdf         # verify without updating tracked release PDF
hatch run pdf                           # writes pdf/circuit-to-code-vX.Y.Z.pdf
hatch run pdf --lesson scratch          # one module
hatch run pdf --lesson circuits --lesson microbit
hatch build -t custom pdf               # full book into pdf/
```

`--lesson` accepts short id (`scratch`), folder (`01-scratch`), or number (`1`). The
Hatch `pdf` script forwards args to the CLI (`circuit-to-code {args}`).

### Committing PDFs

Tracked files under `pdf/` are release artifacts. Commit a regenerated PDF **only** when
bumping `__version__` in `version.py` (and update the README download link). Otherwise
leave `pdf/` out of the commit — CI rejects PRs that change `pdf/*.pdf` without a
`version.py` change.

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

| Path                   | Purpose                                         |
| ---------------------- | ----------------------------------------------- |
| `lessons/`             | Course modules (`NN-slug/`) and syllabus        |
| `lessons/NN-slug/`     | One module: lesson markdown + optional diagrams |
| `src/circuit_to_code/` | PDF generation package                          |
| `tests/`               | pytest suite (including SVG validation)         |
| `docs/`                | Developer docs (excluded from the lesson PDF)   |
| `pdf/`                 | Release PDF(s); commit only with version bumps  |

## Course modules

Numbered folders under `lessons/` define the recommended path and PDF order:

1. `01-scratch` — Scratch programming
2. `02-spike-prime` — LEGO SPIKE Prime *(optional)*
3. `03-circuits` — breadboard electronics (`beginner.md` + `intermediate.md`)
4. `04-microbit` — BBC micro:bit V2
5. `05-circuitpython` — CircuitPython on Pico (or Nano RP2040); recommended text path
6. `06-arduino` — Arduino Uno C++ sketches; alternate / follow-on text path

Learning order for Circuits: Beginner → micro:bit → Intermediate (both circuit files
live in `03-circuits/`; handoffs describe when to read each section). CircuitPython and
Arduino both require both Circuits sections; CircuitPython is the gentler default after
Intermediate.

**Planned later:** deeper mission labs; ESP32; full Raspberry Pi; libraries and shields;
capstone / certificate.

### Adding a module

Create the next numbered folder under `lessons/`, for example `07-…/`, put the lesson
markdown inside, and keep module-specific images in that folder’s `diagrams/` directory.
Zero-padded numbers keep GitHub and the printable PDF in the same order. The
learner-facing syllabus lives in [`lessons/README.md`](../lessons/README.md).

## CI

GitHub Actions (`.github/workflows/ci.yml`) runs:

1. `hatch run lint:check`
2. `hatch run test`
3. `hatch run pdf -o $RUNNER_TEMP/…` (build check; output is not committed)
4. On pull requests: fail if `pdf/*.pdf` changed without a `version.py` bump

## SVG diagrams

Lesson SVGs under `lessons/**/diagrams/` must be well-formed XML (UTF-8, valid `<svg>`).
Tests in `tests/test_svg_diagrams.py` catch common breaks such as raw `<` in text
(`A <-> B` → use `A to B` or `&lt;`).
