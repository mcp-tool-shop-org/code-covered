---
title: Usage
description: CLI commands, Python API, and feature details.
sidebar:
  order: 3
---

## CLI commands

### Basic analysis

```bash
# Analyze a coverage report
code-covered coverage.json

# Show full test templates
code-covered coverage.json -v
```

### Filtering and limiting

```bash
# Filter by priority level
code-covered coverage.json --priority critical
code-covered coverage.json --priority high

# Limit number of suggestions
code-covered coverage.json --limit 5
```

### Output options

```bash
# Write test stubs to a file
code-covered coverage.json -o tests/test_missing.py

# JSON output for CI pipelines
code-covered coverage.json --format json

# Specify source root (if coverage paths are relative)
code-covered coverage.json --source-root ./src
```

## Priority levels

Every gap is classified before it surfaces:

| Priority | Triggered by | Example |
|----------|-------------|---------|
| **Critical** | Exception handlers, raise statements | `except ValueError:` never triggered |
| **High** | Conditional branches | `if x > 0:` branch never taken |
| **Medium** | Function bodies, loops | Loop body never entered |
| **Low** | Other uncovered code | Module-level statements |

## Test templates

Each suggestion includes a ready-to-use test template following the Arrange/Act/Assert pattern:

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

## Setup hints

code-covered detects common patterns in your code and suggests what to mock:

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## Python API

Use code-covered programmatically:

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

## CI integration

Use JSON output to integrate with CI pipelines:

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
