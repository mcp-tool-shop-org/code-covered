# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-02-27

### Added
- SECURITY.md with data scope and response timeline
- SHIP_GATE.md and SCORECARD.md (Shipcheck audit)
- Makefile with `verify` target (lint + typecheck + test + build)
- Security & Data Scope section in README
- Codecov badge in README

### Changed
- Promoted to v1.0.0 stable release

## [0.5.2] - 2026-02-25

### Added
- Landing page using @mcptoolshop/site-theme
- Translations (7 languages)
- Codecov coverage integration
- Dependency security audit in CI
- Secret scanning in CI

### Changed
- Improved CI with paths-gated triggers and concurrency

## [0.5.1] - 2026-02-24

### Added
- MCP adapter for code-covered analysis
- JSON output format (`--format json`)
- Priority filtering (`--priority critical`)

## [0.5.0] - 2026-02-23

### Added
- Initial public release
- AST-based coverage gap analysis
- Prioritized test suggestions (critical/high/medium/low)
- Test template generation with setup hints
- CLI with `coverage.json` input
- Python API (`find_coverage_gaps`, `print_coverage_gaps`)
- Zero runtime dependencies (stdlib only)
