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

**Identifique las áreas sin cobertura y sugiera qué pruebas escribir.**

Parte de [MCP Tool Shop](https://mcp-tool-shop.github.io/) – herramientas prácticas para desarrolladores que no interfieren en su trabajo.

## ¿Por qué usar `code-covered`?

Las herramientas de cobertura le indican *qué* líneas no están probadas. `code-covered` le indica *qué pruebas debe escribir*. Lee su archivo `coverage.json`, analiza el árbol de sintaxis (AST) para comprender el contexto (controladores de excepciones, ramas, bucles) y genera pruebas preliminares priorizadas que puede incluir directamente en su conjunto de pruebas. No tiene dependencias de tiempo de ejecución, solo utiliza la biblioteca estándar.

## El problema

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% de cobertura. 12 líneas sin probar. Pero, ¿*cuáles* son esas 12 líneas? ¿Y qué pruebas las cubrirían?

## La solución

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

## Instalación

```bash
pip install code-covered
```

## Inicio rápido

### Para usuarios

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### Para desarrolladores

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

## Características

### Niveles de prioridad

| Prioridad | Lo que significa | Ejemplo |
|----------|---------------|---------|
| **Critical** | Controladores de excepciones, sentencias `raise` | `except ValueError:` nunca se activa |
| **High** | Ramas condicionales | La rama `if x > 0:` nunca se ejecuta |
| **Medium** | Cuerpos de funciones, bucles | El cuerpo del bucle nunca se ejecuta |
| **Low** | Otro código sin cubrir | Sentencias a nivel de módulo |

### Plantillas de pruebas

Cada sugerencia incluye una plantilla de prueba lista para usar:

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

### Sugerencias de configuración

Detecta patrones comunes y sugiere qué simular (mock):

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## Referencia de la interfaz de línea de comandos (CLI)

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

### Códigos de salida

| Code | Significado |
|------|---------|
| 0 | Éxito (se encontraron lagunas o no se encontraron lagunas) |
| 1 | Error (archivo no encontrado, error de análisis) |

### Salida JSON

Utilice `--format json` para la integración en sistemas de integración continua (CI):

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

## API de Python

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

## Cómo funciona

1. **Análisis de `coverage.json`**: Lee el informe JSON de `pytest-cov`.
2. **Análisis del AST**: Analiza los archivos de código fuente para comprender la estructura del código.
3. **Detección de contexto**: Identifica qué hace cada bloque sin cubrir:
- ¿Es un controlador de excepciones?
- ¿Es una rama condicional?
- ¿En qué función/clase se encuentra?
4. **Generación de plantillas**: Crea plantillas de prueba específicas basadas en el contexto.
5. **Priorización**: Clasifica por importancia (rutas de error > ramas > otros).

## Licencia

MIT: consulte [LICENSE](LICENSE) para obtener más detalles.
