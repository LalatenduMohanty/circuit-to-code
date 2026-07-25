# Circuit to Code

Hands-on electronics lessons for anyone learning circuits and components — a path toward
programming and real-world embedded projects (Scratch / LEGO Spike Prime friendly), with
schematics and a printable PDF.

**Start here:** course path and full contents are in
[`lessons/README.md`](lessons/README.md) (Scratch → Circuits (Beginner) → micro:bit →
Circuits (Intermediate) → CircuitPython and/or Arduino → Robot Missions; optional SPIKE
Prime after Scratch).

**Download the printable PDF:**
[`pdf/circuit-to-code-v0.4.0.pdf`](pdf/circuit-to-code-v0.4.0.pdf)

## Generate the PDF

### Prerequisites

- Python 3.10 or newer
- [Hatch](https://hatch.pypa.io/) — `pip install hatch`
- WeasyPrint system libraries (Linux example):

```bash
sudo apt-get install -y --no-install-recommends \
  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info
```

### Quick start

From the repository root:

```bash
hatch run pdf
```

This writes a versioned file under `pdf/`, for example:

```text
pdf/circuit-to-code-v0.4.0.pdf
```

### Specific lessons

Generate one or more modules instead of the full book:

```bash
hatch run pdf --lesson scratch
hatch run pdf --lesson spike-prime
hatch run pdf --lesson circuits
hatch run pdf --lesson microbit
hatch run pdf --lesson circuitpython
hatch run pdf --lesson arduino
hatch run pdf --lesson robot-missions
hatch run pdf --lesson scratch --lesson circuits
```

Selectors accept the short id (`scratch`, `spike-prime`, `circuits`, `circuitpython`,
`arduino`, `robot-missions`), folder name (`01-scratch`), or order number (`1`). The
`circuits` module includes both Beginner and Intermediate sections. Filtered builds
write names like `pdf/circuit-to-code-scratch-v0.4.0.pdf`.

### Other ways to build

```bash
# Same as hatch run pdf (CLI entry point)
hatch run circuit-to-code

# Custom output path
hatch run pdf -o /tmp/circuits.pdf

# Hatch custom build target (also writes under pdf/)
hatch build -t custom pdf

# Run tests, then generate the PDF
hatch run build
```

### What goes into the PDF

Markdown lessons under `lessons/` (in numbered module order) plus their embedded
diagrams. Use `--lesson` to include only selected modules. Developer docs under `docs/`
and this README are not included.

## More developer commands

See [`docs/developer.md`](docs/developer.md) for tests, linting (Ruff / mypy /
mdformat), and project layout.

## License

Copyright 2026 Lalatendu Mohanty. Licensed under the [Apache License 2.0](LICENSE). See
[`NOTICE`](NOTICE) for the copyright notice.
