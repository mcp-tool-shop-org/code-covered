import type { SiteConfig } from "@mcptoolshop/site-theme"

export const config: SiteConfig = {
  title: "code-covered",
  description:
    "Find coverage gaps and generate the tests you're missing.",
  logoBadge: "CC",
  brandName: "code-covered",
  repoUrl: "https://github.com/mcp-tool-shop-org/code-covered",
  footerText:
    'MIT Licensed — built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>',

  hero: {
    badge: "Python · pytest · Zero dependencies",
    headline: "Know your gaps.",
    headlineAccent: "Write the missing tests.",
    description:
      "code-covered reads your coverage.json, walks the AST to understand context — exception handlers, branches, loops — then generates prioritized, ready-to-use test stubs. Not just what lines are missing. What tests to write.",
    primaryCta: { href: "#get-started", label: "Get started" },
    secondaryCta: { href: "#how-it-works", label: "How it works" },
    previews: [
      {
        label: "Quick start",
        code: "pip install code-covered\n\n# Run tests with coverage JSON\npytest --cov=myapp --cov-report=json\n\n# Find what you're missing\ncode-covered coverage.json"
      },
      {
        label: "Example output",
        code: "Coverage: 74.5% (35/47 lines)\nFiles analyzed: 1 (1 with gaps)\n\nMissing tests: 4\n  [!!] CRITICAL: 2\n  [! ] HIGH: 2\n\nTop suggestions:\n  1. [!!] test_validator_validate_input_handles_exception\n       In validate_input() lines 23-27\n       — when ValueError is raised\n\n  2. [!!] test_validator_parse_data_raises_error\n       In parse_data() lines 45-45 — raise ParseError"
      },
      {
        label: "Generate stubs",
        code: "# Write test stubs directly to a file\ncode-covered coverage.json -o tests/test_gaps.py\n\n# Filter to critical gaps only\ncode-covered coverage.json --priority critical\n\n# JSON output for CI pipelines\ncode-covered coverage.json --format json\n\n# Show full test templates\ncode-covered coverage.json -v"
      }
    ]
  },

  sections: [
    {
      kind: "features",
      id: "features",
      title: "More than a coverage report",
      subtitle: "It understands your code. Not just which lines are missing.",
      features: [
        {
          title: "AST-aware context",
          desc: "Walks the source AST to understand what each uncovered block actually does — is it an exception handler? A branch condition? A loop body? The suggestion reflects the context."
        },
        {
          title: "Prioritized by risk",
          desc: "Critical first: exception handlers and raise statements that were never triggered. Then branches, then loops. The gaps most likely to break production surface at the top."
        },
        {
          title: "Zero dependencies",
          desc: "Pure Python stdlib. No heavy installs, no API calls, no runtime magic. Works anywhere pytest-cov produces a coverage.json. Install once, run anywhere."
        }
      ]
    },
    {
      kind: "data-table",
      id: "priorities",
      title: "Priority levels",
      subtitle: "Every gap is classified before it's surfaced.",
      columns: ["Priority", "Triggered by", "Example"],
      rows: [
        [
          "Critical",
          "Exception handlers, raise statements",
          "except ValueError: never triggered"
        ],
        [
          "High",
          "Conditional branches",
          "if x > 0: branch never taken"
        ],
        [
          "Medium",
          "Function bodies, loops",
          "Loop body never entered"
        ],
        [
          "Low",
          "Other uncovered code",
          "Module-level statements"
        ]
      ]
    },
    {
      kind: "code-cards",
      id: "get-started",
      title: "Get started",
      cards: [
        {
          title: "Install & run",
          code: "pip install code-covered\n\n# Generate coverage.json\npytest --cov=myapp --cov-report=json\n\n# Analyze gaps\ncode-covered coverage.json\n\n# Verbose: show full templates\ncode-covered coverage.json -v"
        },
        {
          title: "Generate test stubs",
          code: "# Write stubs to a file\ncode-covered coverage.json -o tests/test_missing.py\n\n# Filter by priority\ncode-covered coverage.json --priority critical\ncode-covered coverage.json --priority high\n\n# Limit output\ncode-covered coverage.json --limit 5"
        },
        {
          title: "CI integration",
          code: "# JSON output for scripts and pipelines\ncode-covered coverage.json --format json\n\n# Exit codes\n# 0 — success (gaps found or clean)\n# 1 — error (file not found, parse error)\n\n# Specify source root if paths are relative\ncode-covered coverage.json --source-root ./src"
        },
        {
          title: "Python API",
          code: "from analyzer import find_coverage_gaps\n\n# Find gaps programmatically\nsuggestions, warnings = find_coverage_gaps(\"coverage.json\")\n\nfor s in suggestions:\n    print(f\"{s.priority}: {s.test_name}\")\n    print(f\"  Lines: {s.covers_lines}\")\n    print(f\"  Template:\\n{s.code_template}\")"
        }
      ]
    },
    {
      kind: "features",
      id: "how-it-works",
      title: "How it works",
      subtitle: "Five steps from coverage report to ready-to-paste test stub.",
      features: [
        {
          title: "Parse & map",
          desc: "Reads coverage.json from pytest-cov. Parses source files with stdlib ast to map every uncovered line back to the function, class, and block it lives in."
        },
        {
          title: "Detect & template",
          desc: "Classifies each gap — exception handler, branch, loop, raise statement — and generates a specific, context-aware test template with Arrange/Act/Assert scaffolding and setup hints."
        },
        {
          title: "Prioritize & emit",
          desc: "Ranks by risk and outputs to terminal, test stub files, or JSON for CI. Drop the generated stubs into your test suite and fill in the TODOs."
        }
      ]
    }
  ]
}
