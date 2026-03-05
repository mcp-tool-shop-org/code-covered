---
title: Getting Started
description: Install code-covered and run your first analysis.
sidebar:
  order: 1
---

## Installation

Install from PyPI:

```bash
pip install code-covered
```

## Quick start

### 1. Generate coverage data

Run your tests with JSON coverage output:

```bash
pytest --cov=myapp --cov-report=json
```

This produces a `coverage.json` file in your project root.

### 2. Analyze your gaps

```bash
code-covered coverage.json
```

You'll see a prioritized list of missing tests, ranked by risk.

### 3. Generate test stubs

Write ready-to-use test stubs directly to a file:

```bash
code-covered coverage.json -o tests/test_gaps.py
```

Open the generated file, fill in the TODOs, and run your tests again.

## For developers

Clone and set up a development environment:

```bash
git clone https://github.com/mcp-tool-shop-org/code-covered.git
cd code-covered

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -e ".[dev]"

# Run tests
pytest -v

# Run with coverage
pytest --cov=analyzer --cov=mcp_code_covered --cov=cli --cov-report=term-missing

# Linting and type checking
ruff check analyzer mcp_code_covered cli.py tests
pyright analyzer mcp_code_covered cli.py tests
```
