<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  
            <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/code-covered/readme.png"
           alt="code-covered" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/code-covered/"><img src="https://img.shields.io/pypi/v/code-covered" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/code-covered/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**Identifique lacunas na cobertura de testes e sugira quais testes devem ser escritos.**

Parte do [MCP Tool Shop](https://mcp-tool-shop.github.io/) -- ferramentas práticas para desenvolvedores que não atrapalham o seu fluxo de trabalho.

## Por que usar `code-covered`?

Ferramentas de cobertura mostram quais linhas de código não foram testadas. `code-covered` informa *quais testes você deve escrever*. Ele lê seu arquivo `coverage.json`, analisa a estrutura da árvore sintática (AST) para entender o contexto (tratadores de exceção, ramificações, loops) e gera modelos de testes priorizados que você pode inserir diretamente em sua suíte de testes. Não possui dependências de tempo de execução – apenas a biblioteca padrão.

## O Problema

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% de cobertura. 12 linhas não testadas. Mas *quais* 12 linhas? E quais testes cobririam essas linhas?

## A Solução

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

## Instalação

```bash
pip install code-covered
```

## Início Rápido

### Para Usuários

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### Para Desenvolvedores

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

## Recursos

### Níveis de Prioridade

| Prioridade | O que isso significa | Exemplo |
|----------|---------------|---------|
| **Critical** | Tratadores de exceção, declarações `raise` | `except ValueError:` nunca acionado |
| **High** | Ramificações condicionais | `if x > 0:` ramificação nunca executada |
| **Medium** | Corpos de funções, loops | Corpo do loop nunca executado |
| **Low** | Outro código não coberto | Declarações de nível de módulo |

### Modelos de Teste

Cada sugestão inclui um modelo de teste pronto para uso:

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

### Dicas de Configuração

Detecta padrões comuns e sugere o que simular (mock):

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## Referência da Interface de Linha de Comando (CLI)

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

### Códigos de Saída

| Code | Significado |
|------|---------|
| 0 | Sucesso (lacunas encontradas ou nenhuma lacuna) |
| 1 | Erro (arquivo não encontrado, erro de análise) |

### Saída JSON

Use `--format json` para integração com sistemas de CI:

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

## API Python

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

## Como Funciona

1. **Análise de `coverage.json`** -- Lê o relatório JSON do `pytest-cov`.
2. **Análise da AST** -- Analisa os arquivos de código-fonte para entender a estrutura do código.
3. **Detecção de Contexto** -- Identifica o que cada bloco não coberto faz:
- É um tratador de exceção?
- É uma ramificação condicional?
- Em qual função/classe está?
4. **Geração de Modelos** -- Cria modelos de teste específicos com base no contexto.
5. **Priorização** -- Classifica por importância (caminhos de erro > ramificações > outros).

## Licença

MIT -- veja [LICENSE](LICENSE) para detalhes.
