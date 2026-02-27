.PHONY: verify test lint typecheck build

verify: lint typecheck test build
	@echo "✓ All checks passed"

test:
	pytest --cov=analyzer --cov=mcp_code_covered --cov=cli --cov-report=term-missing

lint:
	ruff check analyzer mcp_code_covered cli.py tests

typecheck:
	pyright analyzer mcp_code_covered cli.py tests

build:
	python -m build --sdist --wheel
