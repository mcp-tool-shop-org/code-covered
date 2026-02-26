<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/code-covered/readme.png" alt="code-covered" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/code-covered/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/code-covered/"><img src="https://img.shields.io/pypi/v/code-covered" alt="PyPI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/code-covered/"><img src="https://img.shields.io/badge/Landing_Page-live-blue" alt="Landing Page"></a>
</p>

**उन क्षेत्रों की पहचान करें जहां कवरेज की कमी है, और यह सुझाव दें कि कौन से परीक्षण लिखने चाहिए।**

[MCP Tool Shop](https://mcp-tool-shop.github.io/) का हिस्सा -- व्यावहारिक डेवलपर उपकरण जो आपके काम में बाधा नहीं डालते।

## 'कोड-कवर्ड' क्यों?

कवरेज उपकरण आपको बताते हैं कि *कौन सी* पंक्तियाँ परीक्षण नहीं की गई हैं। `कोड-कवर्ड` आपको बताता है कि *कौन से परीक्षण लिखने चाहिए*। यह आपकी `coverage.json` फ़ाइल को पढ़ता है, संदर्भ को समझने के लिए एब्स्ट्रैक्ट सिंटैक्स ट्री (AST) का विश्लेषण करता है (अपवाद हैंडलर, शाखाएँ, लूप), और प्राथमिकता वाले परीक्षण टेम्पलेट उत्पन्न करता है जिन्हें आप सीधे अपने परीक्षण सूट में डाल सकते हैं। इसमें कोई रनटाइम निर्भरता नहीं है - केवल स्टैंडर्ड लाइब्रेरी।

## समस्या

```
$ pytest --cov=myapp
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/validator.py      47     12    74%
```

74% कवरेज। 12 पंक्तियाँ छूटी हुई। लेकिन *कौन सी* 12 पंक्तियाँ? और उन्हें कवर करने के लिए कौन से परीक्षण होंगे?

## समाधान

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

## स्थापना

```bash
pip install code-covered
```

## त्वरित शुरुआत

### उपयोगकर्ताओं के लिए

```bash
# 1. Run your tests with coverage JSON output
pytest --cov=myapp --cov-report=json

# 2. Find what tests you're missing
code-covered coverage.json

# 3. Generate test stubs
code-covered coverage.json -o tests/test_gaps.py
```

### डेवलपर्स के लिए

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

## विशेषताएं

### प्राथमिकता स्तर

| प्राथमिकता | इसका क्या मतलब है | उदाहरण |
|----------|---------------|---------|
| **Critical** | अपवाद हैंडलर, 'raise' स्टेटमेंट | `except ValueError:` कभी ट्रिगर नहीं हुआ |
| **High** | शर्तिया शाखाएँ | `if x > 0:` शाखा कभी नहीं ली गई |
| **Medium** | फ़ंक्शन बॉडी, लूप | लूप बॉडी कभी नहीं चला |
| **Low** | अन्य बिना कवर किए गए कोड | मॉड्यूल-स्तरीय स्टेटमेंट |

### परीक्षण टेम्पलेट

प्रत्येक सुझाव में एक तैयार-से-उपयोग परीक्षण टेम्पलेट शामिल है:

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

### सेटअप संकेत

यह सामान्य पैटर्न का पता लगाता है और यह सुझाव देता है कि क्या मॉक करना है:

```
Hints: Mock HTTP requests with responses or httpx, Use @pytest.mark.asyncio decorator
```

## सीएलआई संदर्भ

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

### एग्जिट कोड

| Code | अर्थ |
|------|---------|
| 0 | सफलता (गैप पाए गए या कोई गैप नहीं) |
| 1 | त्रुटि (फ़ाइल नहीं मिली, पार्सिंग त्रुटि) |

### JSON आउटपुट

सीआई एकीकरण के लिए `--format json` का उपयोग करें:

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

## पायथन एपीआई

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

## यह कैसे काम करता है

1. **`coverage.json` को पार्स करें** -- `pytest-cov` से JSON रिपोर्ट को पढ़ें।
2. **एएसटी विश्लेषण** -- कोड संरचना को समझने के लिए स्रोत फ़ाइलों का विश्लेषण करें।
3. **संदर्भ का पता लगाना** -- पहचानें कि प्रत्येक बिना कवर किए गए ब्लॉक का क्या कार्य है:
- क्या यह एक अपवाद हैंडलर है?
- क्या यह एक शर्तिया शाखा है?
- यह किस फ़ंक्शन/क्लास में है?
4. **टेम्पलेट पीढ़ी** -- संदर्भ के आधार पर विशिष्ट परीक्षण टेम्पलेट बनाएं।
5. **प्राथमिकता** -- महत्व के अनुसार रैंक करें (त्रुटि पथ > शाखाएँ > अन्य)।

## लाइसेंस

एमआईटी -- विवरण के लिए [लाइसेंस](LICENSE) देखें।
