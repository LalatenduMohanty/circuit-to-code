# Circuit to Code

Hands-on electronics lessons for anyone learning circuits and components — a path toward
programming and real-world embedded projects (Scratch / LEGO Spike Prime friendly), with
schematics and a printable PDF.

**Start here:** course path and full contents are in
[`lessons/README.md`](lessons/README.md) (Scratch → Circuits → micro:bit).

**Download the printable PDF:**
[`pdf/circuit-to-code-v0.2.0.pdf`](pdf/circuit-to-code-v0.2.0.pdf)

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
pdf/circuit-to-code-v0.2.0.pdf
```

### Other ways to build

```bash
# Same as hatch run pdf (CLI entry point)
hatch run circuit-to-code

# Custom output path
hatch run circuit-to-code -- -o /tmp/circuits.pdf

# Hatch custom build target (also writes under pdf/)
hatch build -t custom pdf

# Run tests, then generate the PDF
hatch run build
```

### What goes into the PDF

Markdown lessons under `lessons/` (in numbered module order) plus their embedded
diagrams. Developer docs under `docs/` and this README are not included.

## More developer commands

See [`docs/developer.md`](docs/developer.md) for tests, linting (Ruff / mypy /
mdformat), and project layout.

## License

Copyright 2026 Lalatendu Mohanty. Licensed under the [Apache License 2.0](LICENSE). See
[`NOTICE`](NOTICE) for the copyright notice.
