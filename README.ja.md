<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="assets/logo.png" alt="code-covered" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/code-covered/"><img src="https://img.shields.io/pypi/v/code-covered" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/code-covered/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**未カバー部分を特定し、どのようなテストを作成すべきかを提案します。**

[MCP Tool Shop](https://mcp-tool-shop.github.io/) の一部です。これは、開発者の作業を妨げない、実用的な開発ツールです。

## なぜコードカバレッジが必要なのでしょうか？

カバレッジツールは、どの行がテストされていないかを教えてくれます。`code-covered` は、*どのようなテストを作成すべきか* を教えてくれます。これは、`coverage.json` を読み込み、AST（抽象構文木）を解析してコンテキスト（例外ハンドラ、ブランチ、ループなど）を理解し、テストスイートにそのまま組み込める優先順位付けされたテストの雛形を生成します。実行時の依存関係はゼロです。標準ライブラリのみを使用します。

## 問題点

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

カバレッジが74%。12行が未カバー。しかし、その12行は*具体的にどの行* なのでしょうか？そして、それらをカバーするテストは*どのようなもの* でしょうか？

## 解決策

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

## インストール方法

```bash
pip install code-covered
```

## クイックスタート

### ユーザー向け

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### 開発者向け

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

## 機能

### 優先度レベル

| 優先度 | 意味 | 例 |
|----------|---------------|---------|
| **Critical** | 例外ハンドラ、`raise` 文 | `except ValueError:` が一度もトリガーされていない |
| **High** | 条件分岐 | `if x > 0:` のブランチが一度も実行されていない |
| **Medium** | 関数本体、ループ | ループ本体が一度も実行されていない |
| **Low** | その他の未カバーコード | モジュールレベルの文 |

### テストテンプレート

各提案には、すぐに使用できるテストテンプレートが含まれています。

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

### セットアップのヒント

一般的なパターンを検出し、何を作成するかを提案します。

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## CLI（コマンドラインインターフェース）リファレンス

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

### 終了コード

| Code | 意味 |
|------|---------|
| 0 | 成功（未カバー部分が見つかった、または未カバー部分がない） |
| 1 | エラー（ファイルが見つからない、解析エラー） |

### JSON出力

CI（継続的インテグレーション）との連携には、`--format json` オプションを使用します。

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

## 仕組み

1. **`coverage.json` の解析:** `pytest-cov` からの JSON レポートを読み込みます。
2. **AST 解析:** ソースファイルを解析し、コードの構造を理解します。
3. **コンテキスト検出:** 未カバーの各ブロックが何をしているかを特定します。
- 例外ハンドラですか？
- 条件分岐ですか？
- どの関数/クラスに含まれていますか？
4. **テンプレート生成:** コンテキストに基づいて、特定のテストテンプレートを作成します。
5. **優先順位付け:** 重要度（エラーパス > ブランチ > その他）でランク付けします。

## ライセンス

MIT -- 詳細については、[LICENSE](LICENSE) を参照してください。
