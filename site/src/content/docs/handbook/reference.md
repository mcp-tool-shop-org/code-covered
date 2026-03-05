---
title: Reference
description: Full CLI and Python API reference for code-covered.
sidebar:
  order: 4
---

## CLI reference

### Synopsis

```
code-covered [OPTIONS] COVERAGE_FILE
```

### Arguments

| Argument | Description |
|----------|-------------|
| `COVERAGE_FILE` | Path to `coverage.json` produced by `pytest-cov` |

### Options

| Option | Description |
|--------|-------------|
| `-v`, `--verbose` | Show full test templates in output |
| `-o FILE`, `--output FILE` | Write generated test stubs to a file |
| `--priority LEVEL` | Filter by priority: `critical`, `high`, `medium`, `low` |
| `--limit N` | Maximum number of suggestions to display |
| `--format FORMAT` | Output format: `text` (default) or `json` |
| `--source-root DIR` | Source root directory (if coverage paths are relative) |

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success (gaps found or no gaps) |
| 1 | Error (file not found, parse error) |

## Python API reference

### `find_coverage_gaps(path)`

Analyze a coverage JSON file and return gap suggestions.

**Parameters:**
- `path` (str) — Path to the `coverage.json` file.

**Returns:**
- `suggestions` (list) — List of suggestion objects, each with:
  - `test_name` (str) — Suggested test function name
  - `priority` (str) — One of `critical`, `high`, `medium`, `low`
  - `covers_lines` (list[int]) — Line numbers this test would cover
  - `block_type` (str) — Type of uncovered block (e.g., `exception_handler`, `branch`, `loop`)
  - `code_template` (str) — Ready-to-use test stub
- `warnings` (list) — Any warnings encountered during analysis

### `print_coverage_gaps(suggestions)`

Print formatted gap suggestions to stdout.

**Parameters:**
- `suggestions` (list) — List of suggestion objects from `find_coverage_gaps`.

## Security and data scope

- **Data touched:** reads `coverage.json` (pytest-cov output) and Python source files for AST analysis. All processing is in-memory.
- **Data NOT touched:** no network requests, no filesystem writes (except explicit `-o` output), no OS credentials, no telemetry, no user data collection.
- **Permissions required:** read access to coverage report and source files only.

## License

MIT -- see [LICENSE](https://github.com/mcp-tool-shop-org/code-covered/blob/main/LICENSE) for details.
