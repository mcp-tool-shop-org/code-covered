---
title: Beginners Guide
description: A gentle introduction to code-covered for newcomers.
sidebar:
  order: 99
---

## What is this tool?

code-covered is a command-line tool that reads your Python test coverage report and tells you exactly what tests to write next. Standard coverage tools show you which lines are not tested, but they stop there. code-covered goes further: it analyzes your source code with Python's AST module, understands the context of each uncovered block (is it an exception handler? a conditional branch? a raise statement?), and generates prioritized, ready-to-use test stubs you can drop into your test suite.

It has zero runtime dependencies -- only the Python standard library -- and works anywhere `pytest-cov` produces a `coverage.json` file.

## Who is this for?

- **Python developers** who use pytest and want to improve test coverage systematically rather than guessing what to test next.
- **Teams adopting coverage gates** in CI pipelines who need to quickly identify and fill the highest-risk gaps.
- **Developers new to testing** who want concrete guidance on what a test for a specific code pattern should look like.
- **MCP host users** who want coverage analysis available as a tool in their AI-assisted workflow.

## Prerequisites

Before using code-covered, you need:

1. **Python 3.10 or later** installed on your system.
2. **pytest** and **pytest-cov** installed in your project (these produce the coverage report that code-covered reads):
   ```bash
   pip install pytest pytest-cov
   ```
3. **A Python project with tests** -- code-covered analyzes existing coverage data, so you need at least a few tests already running with pytest.

## Your first 5 minutes

**Step 1: Install code-covered.**

```bash
pip install code-covered
```

**Step 2: Run your tests with JSON coverage output.**

Navigate to your project directory and run:

```bash
pytest --cov=yourmodule --cov-report=json
```

Replace `yourmodule` with the name of the package or directory you want coverage for. This produces a `coverage.json` file in your project root.

**Step 3: Analyze the coverage gaps.**

```bash
code-covered coverage.json
```

You will see a summary showing your overall coverage percentage, the number of files with gaps, and a prioritized list of test suggestions ranked by risk.

**Step 4: Generate test stubs.**

```bash
code-covered coverage.json -o tests/test_gaps.py
```

This writes ready-to-use test function stubs to the specified file. Each stub follows the Arrange/Act/Assert pattern and includes TODO comments marking where you need to fill in test-specific logic.

**Step 5: Fill in the stubs and re-run.**

Open `tests/test_gaps.py`, replace the TODO comments with real assertions and setup code, then run your tests again to confirm coverage improved.

## Common mistakes

**Running code-covered without a coverage.json file.** You must run `pytest --cov=yourmodule --cov-report=json` first. code-covered reads the JSON report -- it does not run your tests itself.

**Using the wrong coverage report format.** code-covered requires the JSON format (`--cov-report=json`), not the default terminal output, HTML, or XML formats.

**Forgetting `--source-root` when paths are relative.** If your `coverage.json` contains relative file paths that do not resolve from the current directory, pass `--source-root ./src` (or wherever your source lives) so code-covered can find and parse the actual source files.

**Expecting code-covered to write complete tests.** The generated stubs are scaffolds with TODO markers. You still need to provide the right inputs, mocks, and assertions for your specific codebase.

**Ignoring the priority levels.** Critical and high priority gaps (uncovered exception handlers, raise statements, conditional branches) represent the highest risk. Address those before chasing low-priority gaps for percentage points.

## Next steps

- Read the [Usage guide](/code-covered/handbook/usage/) for the full set of CLI flags, Python API, and CI integration patterns.
- Read [How It Works](/code-covered/handbook/how-it-works/) to understand the five-step analysis pipeline.
- Consult the [Reference](/code-covered/handbook/reference/) for the complete CLI option table, Python API signatures, and MCP adapter details.

## Glossary

| Term | Definition |
|------|-----------|
| **coverage.json** | The JSON coverage report produced by `pytest-cov` (via `--cov-report=json`). Contains per-file data on which lines were executed, missed, and excluded. |
| **AST** | Abstract Syntax Tree. Python's built-in representation of source code structure. code-covered uses it to understand what each uncovered line does. |
| **gap** | A block of uncovered code that represents a missing test. Each gap is classified by type and priority. |
| **suggestion** | A concrete recommendation to write a specific test, including a function name, description, priority, and a code template. |
| **priority** | Risk ranking assigned to each gap: critical (exception handlers, raise statements), high (conditional branches), medium (function bodies, loops), low (other code). |
| **block type** | The structural category of an uncovered block: `exception_handler`, `raise_statement`, `if_true_branch`, `if_false_branch`, `for_loop`, `while_loop`, `return_statement`, or `code_block`. |
| **test stub** | A generated test function skeleton following the Arrange/Act/Assert pattern, with TODO comments where you fill in project-specific logic. |
| **setup hint** | A context-aware tip suggesting what to mock or configure (e.g., "Mock HTTP requests with responses or httpx"). Detected from patterns in the uncovered code. |
| **MCP adapter** | The `code_covered.gaps` tool that exposes the analysis engine to MCP hosts, accepting inline coverage JSON or artifact references. |
| **source root** | The directory where your source files live, used to resolve relative paths in the coverage report. |
