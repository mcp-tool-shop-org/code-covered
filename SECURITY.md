# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅ Yes    |
| < 1.0   | ❌ No     |

## Reporting a Vulnerability

Email: **64996768+mcp-tool-shop@users.noreply.github.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Version affected
- Potential impact

### Response timeline

| Action | Target |
|--------|--------|
| Acknowledge report | 48 hours |
| Assess severity | 7 days |
| Release fix | 30 days |

## Scope

This tool operates **locally only** and has **zero runtime dependencies** (stdlib only).

- **Data touched:** reads `coverage.json` files (pytest-cov output) and Python source files for AST analysis. All processing is in-memory — no files written unless `-o` flag is used for test stub output.
- **Data NOT touched:** no network requests, no filesystem writes (except explicit `-o` output), no OS credentials, no environment variables read, no user data collection.
- **No telemetry** is collected or sent.
- **No secrets handling** — does not read, store, or transmit credentials.
