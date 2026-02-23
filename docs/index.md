# code-covered

**Find coverage gaps and suggest what tests to write.**

Coverage tools tell you *what* lines aren't tested. `code-covered` tells you *what tests to write*. It reads your `coverage.json`, walks the AST to understand context (exception handlers, branches, loops), and generates prioritized test stubs you can drop straight into your test suite.

Zero runtime dependencies -- just stdlib.

## Features

- **Priority-ranked suggestions** -- Critical (exception handlers, raise statements), High (conditional branches), Medium (function bodies, loops), Low (other uncovered code)
- **Ready-to-use test templates** -- Each suggestion includes an Arrange/Act/Assert stub with setup hints
- **AST-aware analysis** -- Understands code structure, not just line numbers
- **Multiple output formats** -- Human-readable terminal output or JSON for CI pipelines
- **Test stub generation** -- Write test files directly with `-o`

## Installation

```bash
pip install code-covered
```

## Quick start

```bash
# Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# Find what tests you're missing
code-covered coverage.json

# Generate test stubs to a file
code-covered coverage.json -o tests/test_gaps.py
```

## Links

- [PyPI](https://pypi.org/project/code-covered/)
- [Source](https://github.com/mcp-tool-shop-org/code-covered)
- [Issues](https://github.com/mcp-tool-shop-org/code-covered/issues)
- [MCP Tool Shop](https://mcp-tool-shop.github.io/)

## License

MIT
