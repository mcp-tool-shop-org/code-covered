<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/code-covered/readme.png" alt="code-covered" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/code-covered/"><img src="https://img.shields.io/pypi/v/code-covered" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/code-covered/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Find coverage gaps and suggest what tests to write.**

Part of [MCP Tool Shop](https://mcp-tool-shop.github.io/) -- practical developer tools that stay out of your way.

## Why code-covered?

Coverage tools tell you *what* lines aren't tested. `code-covered` tells you *what tests to write*. It reads your `coverage.json`, walks the AST to understand context (exception handlers, branches, loops), and generates prioritized test stubs you can drop straight into your test suite. Zero runtime dependencies -- just stdlib.

## The Problem

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% coverage. 12 lines missing. But *which* 12 lines? And what tests would cover them?

## The Solution

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

  3. [! ] test_validator_validate_input_when_condition_false
       In validate_input() lines 31-33 - when len(data) == 0 is False

  4. [! ] test_validator_process_when_condition_true
       In process() lines 52-55 - when config.strict is True
```

## Installation

```bash
pip install code-covered
```

## Quick Start

### For Users

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### For Developers

```bash
# Clone the repository
git clone https://github.com/mcp-tool-shop-org/code-covered.git
cd code-covered

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v

# Run with coverage
pytest --cov=analyzer --cov=mcp_code_covered --cov=cli --cov-report=term-missing

# Run linting
ruff check analyzer mcp_code_covered cli.py tests

# Run type checking
pyright analyzer mcp_code_covered cli.py tests
```

## Features

### Priority Levels

| Priority | What it means | Example |
|----------|---------------|---------|
| **Critical** | Exception handlers, raise statements | `except ValueError:` never triggered |
| **High** | Conditional branches | `if x > 0:` branch never taken |
| **Medium** | Function bodies, loops | Loop body never entered |
| **Low** | Other uncovered code | Module-level statements |

### Test Templates

Each suggestion includes a ready-to-use test template:

```python
def test_validate_input_handles_exception():
    """Test that validate_input handles ValueError."""
    # Arrange: Set up conditions to trigger ValueError
    # TODO: Mock dependencies to raise ValueError

    # Act
    result = validate_input()  # TODO: Add args

    # Assert: Verify exception was handled correctly
    # TODO: Add assertions
```

### Setup Hints

Detects common patterns and suggests what to mock:

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## CLI Reference

```bash
# Basic usage
code-covered coverage.json

# Show full templates
code-covered coverage.json -v

# Filter by priority
code-covered coverage.json --priority critical

# Limit results
code-covered coverage.json --limit 5

# Write test stubs to file
code-covered coverage.json -o tests/test_missing.py

# Specify source root (if coverage paths are relative)
code-covered coverage.json --source-root ./src

# JSON output for CI pipelines
code-covered coverage.json --format json
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (gaps found or no gaps) |
| 1 | Error (file not found, parse error) |

### JSON Output

Use `--format json` for CI integration:

```json
{
  "coverage_percent": 74.5,
  "files_analyzed": 3,
  "files_with_gaps": 1,
  "suggestions": [
    {
      "test_name": "test_validator_validate_input_handles_exception",
      "priority": "critical",
      "covers_lines": [23, 24, 25, 26, 27],
      "block_type": "exception_handler"
    }
  ]
}
```

## Python API

```python
from analyzer import find_coverage_gaps, print_coverage_gaps

# Find gaps
suggestions, warnings = find_coverage_gaps("coverage.json")

# Print formatted output
print_coverage_gaps(suggestions)

# Or process programmatically
for s in suggestions:
    print(f"{s.priority}: {s.test_name}")
    print(f"  Covers lines {s.covers_lines}")
    print(f"  Template:\n{s.code_template}")
```

## How It Works

1. **Parse coverage.json** -- Reads the JSON report from `pytest-cov`
2. **AST Analysis** -- Parses source files to understand code structure
3. **Context Detection** -- Identifies what each uncovered block does:
   - Is it an exception handler?
   - Is it a conditional branch?
   - What function/class is it in?
4. **Template Generation** -- Creates specific test templates based on context
5. **Prioritization** -- Ranks by importance (error paths > branches > other)

## License

MIT -- see [LICENSE](LICENSE) for details.
