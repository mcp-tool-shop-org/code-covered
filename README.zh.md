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

**发现代码覆盖率的不足，并建议编写哪些测试用例。**

它是 [MCP Tool Shop](https://mcp-tool-shop.github.io/) 的一部分，提供实用且不干扰开发的工具。

## 为什么使用 `code-covered`？

代码覆盖率工具可以告诉你哪些行代码没有被测试。`code-covered` 告诉你*应该编写哪些测试用例*。它读取你的 `coverage.json` 文件，通过分析抽象语法树（AST）来理解代码的上下文（异常处理、分支、循环），并生成优先级排序的测试用例模板，你可以直接将其添加到你的测试套件中。它没有任何运行时依赖，只依赖标准库。

## 问题

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

代码覆盖率达到 74%。有 12 行代码没有被覆盖。但是，是*哪 12 行*代码？以及，需要编写哪些测试用例来覆盖它们？

## 解决方案

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

## 安装

```bash
pip install code-covered
```

## 快速开始

### 面向用户

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### 面向开发者

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

## 特性

### 优先级级别

| 优先级 | 含义 | 示例 |
|----------|---------------|---------|
| **Critical** | 异常处理、`raise` 语句 | `except ValueError:` 从未触发 |
| **High** | 条件分支 | `if x > 0:` 分支从未被执行 |
| **Medium** | 函数体、循环 | 循环体从未被执行 |
| **Low** | 其他未覆盖的代码 | 模块级别的语句 |

### 测试模板

每个建议都包含一个可以直接使用的测试模板：

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

### 配置提示

它会检测常见的模式，并建议应该模拟哪些内容：

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## 命令行参考

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

### 退出码

| Code | 含义 |
|------|---------|
| 0 | 成功（找到未覆盖的代码或没有未覆盖的代码） |
| 1 | 错误（文件未找到、解析错误） |

### JSON 输出

使用 `--format json` 进行 CI 集成：

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

## 工作原理

1. **解析 `coverage.json`** -- 读取 `pytest-cov` 生成的 JSON 报告。
2. **AST 分析** -- 解析源代码文件以理解代码结构。
3. **上下文检测** -- 识别每个未覆盖的代码块的作用：
- 它是异常处理吗？
- 它是条件分支吗？
- 它位于哪个函数/类中？
4. **模板生成** -- 根据上下文创建特定的测试模板。
5. **优先级排序** -- 根据重要性进行排序（错误路径 > 分支 > 其他）。

## 许可证

MIT -- 详情请参见 [LICENSE](LICENSE)。
