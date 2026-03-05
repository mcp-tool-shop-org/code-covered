---
title: How It Works
description: The problem code-covered solves and how it solves it.
sidebar:
  order: 2
---

## The problem

Coverage tools tell you what percentage of your code is tested and which lines are missing. But they stop there.

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% coverage. 12 lines missing. But which 12 lines? And what tests would actually cover them?

## The solution

code-covered bridges the gap between "lines not covered" and "tests you should write." It reads your `coverage.json`, walks the AST to understand what each uncovered block actually does, and generates prioritized test suggestions with ready-to-use stubs.

```
$ code-covered coverage.json

============================================================
code-covered
============================================================
Coverage: 74.5% (35/47 lines)
Files analyzed: 1 (1 with gaps)

Missing tests: 4
  [!!] CRITICAL: 2
  [!]  HIGH: 2

Top suggestions:
  1. [!!] test_validator_validate_input_handles_exception
       In validate_input() lines 23-27 - when ValueError is raised

  2. [!!] test_validator_parse_data_raises_error
       In parse_data() lines 45-45 - raise ParseError
```

## The five-step pipeline

1. **Parse coverage.json** — Reads the JSON report produced by `pytest-cov`.

2. **AST analysis** — Parses each source file with Python's stdlib `ast` module to map every uncovered line back to its function, class, and enclosing block.

3. **Context detection** — Classifies what each uncovered block does:
   - Is it an exception handler (`except` block)?
   - Is it a conditional branch (`if`/`elif`/`else`)?
   - Is it a loop body (`for`/`while`)?
   - Is it a `raise` statement?

4. **Template generation** — Creates specific, context-aware test templates with Arrange/Act/Assert scaffolding and setup hints (e.g., "Mock HTTP requests with responses or httpx").

5. **Prioritization** — Ranks suggestions by risk. Error paths and raise statements surface first, then branches, then loops, then everything else.

## Zero dependencies

code-covered uses only the Python standard library. No heavy installs, no API calls, no runtime magic. It works anywhere `pytest-cov` produces a `coverage.json`.
