# Scorecard

> Score a repo before remediation. Fill this out first, then use SHIP_GATE.md to fix.

**Repo:** code-covered
**Date:** 2026-02-27
**Type tags:** [pypi] [cli]

## Pre-Remediation Assessment

| Category | Score | Notes |
|----------|-------|-------|
| A. Security | 6/10 | No SECURITY.md, no threat model in README |
| B. Error Handling | 9/10 | Exit codes, no raw stacks, structured JSON output |
| C. Operator Docs | 7/10 | Good README but no CHANGELOG, no verify script |
| D. Shipping Hygiene | 7/10 | CI has coverage + dep-audit, but no Makefile verify target |
| E. Identity (soft) | 10/10 | Logo, translations, landing page, GitHub metadata |
| **Overall** | **39/50** | |

## Key Gaps

1. No SECURITY.md
2. No threat model / data scope in README
3. No CHANGELOG.md
4. No Makefile with verify target
5. No Codecov badge
6. Version below 1.0.0 (was 0.5.2)

## Remediation Priority

| Priority | Item | Estimated effort |
|----------|------|-----------------|
| 1 | Create SECURITY.md with data scope | 3 min |
| 2 | Add Security & Data Scope to README | 2 min |
| 3 | Create CHANGELOG.md | 3 min |
| 4 | Add Makefile with verify target | 2 min |
| 5 | Bump to v1.0.0 | 1 min |

## Post-Remediation

| Category | Before | After |
|----------|--------|-------|
| A. Security | 6/10 | 10/10 |
| B. Error Handling | 9/10 | 10/10 |
| C. Operator Docs | 7/10 | 10/10 |
| D. Shipping Hygiene | 7/10 | 10/10 |
| E. Identity (soft) | 10/10 | 10/10 |
| **Overall** | 39/50 | 50/50 |
