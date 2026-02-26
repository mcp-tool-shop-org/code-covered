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

**Individua le aree non coperte dal testing e suggerisci quali test scrivere.**

Parte di [MCP Tool Shop](https://mcp-tool-shop.github.io/) -- strumenti pratici per sviluppatori che non interferiscono con il tuo lavoro.

## Perché usare `code-covered`?

Gli strumenti di copertura ti dicono *quali* righe di codice non sono state testate. `code-covered` ti dice *quali test scrivere*. Legge il tuo file `coverage.json`, analizza l'albero sintattico (AST) per comprendere il contesto (gestori di eccezioni, rami, cicli) e genera test di esempio prioritari che puoi inserire direttamente nella tua suite di test. Nessuna dipendenza a runtime, solo librerie standard.

## Il Problema

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% di copertura. 12 righe non testate. Ma *quali* 12 righe? E quali test le coprirebbero?

## La Soluzione

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

## Installazione

```bash
pip install code-covered
```

## Guida Rapida

### Per Utenti

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### Per Sviluppatori

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

## Funzionalità

### Livelli di Priorità

| Priorità | Cosa significa | Esempio |
|----------|---------------|---------|
| **Critical** | Gestori di eccezioni, istruzioni `raise` | `except ValueError:` mai attivato |
| **High** | Rami condizionali | `if x > 0:` ramo mai eseguito |
| **Medium** | Corpi di funzione, cicli | Corpo del ciclo mai eseguito |
| **Low** | Altro codice non coperto | Istruzioni a livello di modulo |

### Modelli di Test

Ogni suggerimento include un modello di test pronto all'uso:

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

### Suggerimenti per la Configurazione

Rileva schemi comuni e suggerisce cosa simulare (mock):

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## Riferimento alla CLI

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

### Codici di Uscita

| Code | Significato |
|------|---------|
| 0 | Successo (lacune trovate o nessuna lacuna) |
| 1 | Errore (file non trovato, errore di analisi) |

### Output JSON

Usa `--format json` per l'integrazione con i sistemi di Continuous Integration (CI):

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

## Come Funziona

1. **Analisi di `coverage.json`** -- Legge il report JSON da `pytest-cov`.
2. **Analisi dell'AST** -- Analizza i file sorgente per comprendere la struttura del codice.
3. **Rilevamento del Contesto** -- Identifica cosa fa ogni blocco di codice non testato:
- È un gestore di eccezioni?
- È un ramo condizionale?
- A quale funzione/classe appartiene?
4. **Generazione di Modelli** -- Crea modelli di test specifici in base al contesto.
5. **Prioritizzazione** -- Ordina in base all'importanza (percorsi di errore > rami > altro).

## Licenza

MIT -- consulta [LICENSE](LICENSE) per i dettagli.
