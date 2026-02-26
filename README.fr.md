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

**Identifiez les lacunes en matière de couverture de code et suggérez les tests à écrire.**

Fait partie de [MCP Tool Shop](https://mcp-tool-shop.github.io/) : des outils pratiques pour les développeurs qui ne vous gênent pas.

## Pourquoi utiliser `code-covered` ?

Les outils de couverture vous indiquent *quelles* lignes ne sont pas testées. `code-covered` vous indique *quels tests écrire*. Il lit votre fichier `coverage.json`, analyse l'arbre syntaxique (AST) pour comprendre le contexte (gestionnaires d'exceptions, branches, boucles) et génère des squelettes de tests priorisés que vous pouvez directement intégrer à votre suite de tests. Aucune dépendance d'exécution, seulement la bibliothèque standard.

## Le problème

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74 % de couverture. 12 lignes non testées. Mais *quelles* 12 lignes ? Et quels tests les couvriraient ?

## La solution

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

## Installation

```bash
pip install code-covered
```

## Démarrage rapide

### Pour les utilisateurs

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### Pour les développeurs

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

## Fonctionnalités

### Niveaux de priorité

| Priorité | Ce que cela signifie | Exemple |
|----------|---------------|---------|
| **Critical** | Gestionnaires d'exceptions, instructions `raise` | `except ValueError:` jamais déclenché |
| **High** | Branches conditionnelles | Branche `if x > 0:` jamais prise |
| **Medium** | Corps de fonction, boucles | Corps de boucle jamais exécuté |
| **Low** | Autres parties de code non couvertes | Instructions au niveau du module |

### Modèles de tests

Chaque suggestion inclut un modèle de test prêt à l'emploi :

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

### Conseils de configuration

Détecte les schémas courants et suggère ce qu'il faut simuler (mock) :

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## Référence de l'interface en ligne de commande (CLI)

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

### Codes de sortie

| Code | Signification |
|------|---------|
| 0 | Succès (lacunes trouvées ou aucune lacune) |
| 1 | Erreur (fichier non trouvé, erreur d'analyse) |

### Sortie JSON

Utilisez `--format json` pour l'intégration dans les systèmes d'intégration continue (CI) :

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

## Fonctionnement

1. **Analyse de `coverage.json`** : Lit le rapport JSON de `pytest-cov`.
2. **Analyse de l'AST** : Analyse les fichiers sources pour comprendre la structure du code.
3. **Détection du contexte** : Identifie ce que chaque bloc non couvert fait :
- Est-ce un gestionnaire d'exceptions ?
- Est-ce une branche conditionnelle ?
- À quelle fonction/classe appartient-il ?
4. **Génération de modèles** : Crée des modèles de tests spécifiques en fonction du contexte.
5. **Priorisation** : Classe par importance (chemins d'erreur > branches > autres).

## Licence

MIT : voir [LICENSE](LICENSE) pour plus de détails.
