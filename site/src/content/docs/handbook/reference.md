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
| `--version` | Show version and exit |
| `--diagnose` | Check environment health (text output) |
| `--diagnose-json` | Check environment health (JSON output) |

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success (gaps found or no gaps) |
| 1 | Error (file not found, parse error) |

## Python API reference

### `find_coverage_gaps(coverage_json, source_root=None)`

Analyze a coverage JSON file and return gap suggestions.

**Parameters:**
- `coverage_json` (str) — Path to the `coverage.json` file.
- `source_root` (str | None) — Optional root directory for resolving source file paths.

**Returns:**
A tuple of `(suggestions, warnings)` where:
- `suggestions` (list[GapSuggestion]) — List of suggestion objects, each with:
  - `test_name` (str) — Suggested test function name
  - `test_file` (str) — Suggested test file path (e.g., `tests/test_utils_validator.py`)
  - `description` (str) — Human-readable description of the gap
  - `priority` (str) — One of `critical`, `high`, `medium`, `low`
  - `covers_lines` (list[int]) — Line numbers this test would cover
  - `block_type` (str) — Type of uncovered block: `exception_handler`, `raise_statement`, `if_true_branch`, `if_false_branch`, `for_loop`, `while_loop`, `return_statement`, or `code_block`
  - `code_template` (str) — Ready-to-use test stub
  - `setup_hints` (list[str]) — Context-aware hints (e.g., "Mock HTTP requests with responses or httpx")
- `warnings` (list[str]) — Any warnings encountered during analysis (e.g., source files not found)

### `print_coverage_gaps(suggestions)`

Print formatted gap suggestions to stdout.

**Parameters:**
- `suggestions` (list) — List of suggestion objects from `find_coverage_gaps`.

## Diagnose command

The `--diagnose` flag checks environment health and reports the status of Python version, the installed package version, the MCP adapter, and the analyzer module.

```bash
code-covered --diagnose
# code-covered environment: OK
#   [OK] python_version: 3.12.0
#   [OK] package_version: 1.0.0
#   [OK] mcp_adapter: 1.0.0
#   [OK] analyzer: available
```

Use `--diagnose-json` for machine-readable output.

## MCP adapter

The `code_covered.gaps` MCP tool exposes the analysis engine to MCP hosts. It accepts a request with:

- `coverage` (object) — Either inline coverage JSON (with a `files` key) or an artifact reference (`artifact_id` + optional `locator`).
- `repo_root` (string, optional) — Root directory for resolving source file paths.
- `priority_filter` (string, optional) — Minimum priority threshold: `critical`, `high`, `medium`, or `low`.
- `limit` (int, optional) — Maximum number of suggestions in the response.
- `fail_on` (string, optional) — CI gating threshold: `none` (default), `critical`, `high`, or `any`. Returns exit code 2 when the threshold is met.
- `format` (string, optional) — Set to `text` to include a human-readable `text` field in the response.

The response includes `exit_code`, `result` (with coverage stats and suggestions), and `warnings`.

## Security and data scope

- **Data touched:** reads `coverage.json` (pytest-cov output) and Python source files for AST analysis. All processing is in-memory.
- **Data NOT touched:** no network requests, no filesystem writes (except explicit `-o` output), no OS credentials, no telemetry, no user data collection.
- **Permissions required:** read access to coverage report and source files only.

## License

MIT -- see [LICENSE](https://github.com/mcp-tool-shop-org/code-covered/blob/main/LICENSE) for details.
