"""
Test Generator for Code-Covered

Generates pytest tests from:
- Static analysis issues (StaticAnalyzer)
- Anomaly detections (AnomalyDetector)
- Function metadata

Can be enhanced via fine-tuned models for smarter test generation.
"""

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Dict
import logging

from .static_analyzer import StaticAnalyzer, StaticIssue, IssueType, FunctionInfo

logger = logging.getLogger(__name__)


@dataclass
class GeneratedTest:
    """A generated test case."""
    test_name: str
    test_code: str
    target_file: Path
    target_function: str
    issue_type: Optional[IssueType]
    description: str
    confidence: float = 1.0  # For model-generated tests

    def to_dict(self) -> dict:
        return {
            "test_name": self.test_name,
            "test_code": self.test_code,
            "target_file": str(self.target_file),
            "target_function": self.target_function,
            "issue_type": self.issue_type.name if self.issue_type else None,
            "description": self.description,
            "confidence": self.confidence
        }


class TestGenerator:
    """
    Generates pytest tests from code analysis.

    Supports two modes:
    1. Rule-based: Uses static analysis to generate targeted tests
    2. Model-based: Uses fine-tuned LLM for smarter generation (when available)
    """

    def __init__(self, analyzer: Optional[StaticAnalyzer] = None, model=None):
        """
        Args:
            analyzer: StaticAnalyzer instance (creates one if not provided)
            model: Optional fine-tuned model for enhanced generation
        """
        self.analyzer = analyzer or StaticAnalyzer()
        self.model = model

    def generate_for_file(self, path: Path) -> List[GeneratedTest]:
        """Generate tests for all functions in a file."""
        tests = []

        # Run static analysis
        issues = self.analyzer.analyze_file(path)
        functions = self.analyzer.get_functions()

        # Group issues by function
        issues_by_func: Dict[str, List[StaticIssue]] = {}
        for issue in issues:
            func_name = issue.function_name or "__module__"
            issues_by_func.setdefault(func_name, []).append(issue)

        # Generate tests for each function
        for func in functions:
            # Skip private/dunder methods
            if func.name.startswith('_') and not func.name.startswith('__'):
                continue

            # Basic test
            tests.append(self._generate_basic_test(func, path))

            # Exception test if function raises
            if func.raises:
                tests.append(self._generate_exception_test(func, path))

            # Edge case test
            tests.append(self._generate_edge_case_test(func, path))

            # Issue-specific tests
            for issue in issues_by_func.get(func.name, []):
                if issue.suggested_test:
                    tests.append(GeneratedTest(
                        test_name=f"test_{func.name}_{issue.type.name.lower()}",
                        test_code=issue.suggested_test,
                        target_file=path,
                        target_function=func.name,
                        issue_type=issue.type,
                        description=f"Test for {issue.type.name}: {issue.message}"
                    ))

        # If model available, enhance with smarter tests
        if self.model:
            tests = self._enhance_with_model(tests, path)

        return tests

    def generate_for_code(self, code: str, filename: str = "module") -> List[GeneratedTest]:
        """Generate tests for code string."""
        tests = []

        issues = self.analyzer.analyze_code(code, filename)
        functions = self.analyzer.get_functions()

        path = Path(filename)

        for func in functions:
            if func.name.startswith('_') and not func.name.startswith('__'):
                continue

            tests.append(self._generate_basic_test(func, path))

            if func.raises:
                tests.append(self._generate_exception_test(func, path))

        return tests

    def _generate_basic_test(self, func: FunctionInfo, path: Path) -> GeneratedTest:
        """Generate basic functionality test."""
        args = self._generate_arg_placeholders(func)
        call_args = self._format_call_args(func)

        if func.has_return:
            assertion = "assert result is not None"
        else:
            assertion = "# Function executes without error"

        test_code = f'''def test_{func.name}_basic():
    """Test basic functionality of {func.name}."""
    {args}
    result = {func.name}({call_args})
    {assertion}
'''
        return GeneratedTest(
            test_name=f"test_{func.name}_basic",
            test_code=test_code,
            target_file=path,
            target_function=func.name,
            issue_type=None,
            description=f"Basic functionality test for {func.name}"
        )

    def _generate_exception_test(self, func: FunctionInfo, path: Path) -> GeneratedTest:
        """Generate exception handling test."""
        exceptions = ", ".join(func.raises) or "Exception"

        test_code = f'''def test_{func.name}_raises():
    """Test that {func.name} raises expected exceptions."""
    import pytest
    with pytest.raises(({exceptions})):
        {func.name}(None)  # TODO: Use invalid input
'''
        return GeneratedTest(
            test_name=f"test_{func.name}_raises",
            test_code=test_code,
            target_file=path,
            target_function=func.name,
            issue_type=IssueType.NO_ERROR_PATH_TEST,
            description=f"Exception test for {func.name}"
        )

    def _generate_edge_case_test(self, func: FunctionInfo, path: Path) -> GeneratedTest:
        """Generate edge case test scaffolding."""
        cases = []
        for arg in func.args:
            if arg == 'self':
                continue
            cases.append(f"    # Test {arg}=None, {arg}=[], {arg}=''")

        test_code = f'''def test_{func.name}_edge_cases():
    """Test {func.name} with edge cases."""
    import pytest
{chr(10).join(cases) if cases else "    pass  # Add edge cases"}
'''
        return GeneratedTest(
            test_name=f"test_{func.name}_edge_cases",
            test_code=test_code,
            target_file=path,
            target_function=func.name,
            issue_type=IssueType.NO_EDGE_CASE_TEST,
            description=f"Edge case tests for {func.name}"
        )

    def _generate_arg_placeholders(self, func: FunctionInfo) -> str:
        """Generate placeholder values based on arg names."""
        placeholders = []
        for arg in func.args:
            if arg == 'self':
                continue

            # Infer type from name
            if any(x in arg.lower() for x in ['path', 'file']):
                placeholders.append(f'{arg} = "test.txt"')
            elif any(x in arg.lower() for x in ['list', 'items', 'values']):
                placeholders.append(f'{arg} = [1, 2, 3]')
            elif any(x in arg.lower() for x in ['dict', 'data', 'config']):
                placeholders.append(f'{arg} = {{"key": "value"}}')
            elif any(x in arg.lower() for x in ['num', 'count', 'id', 'index']):
                placeholders.append(f'{arg} = 1')
            elif any(x in arg.lower() for x in ['name', 'text', 'str', 'msg']):
                placeholders.append(f'{arg} = "test"')
            elif any(x in arg.lower() for x in ['flag', 'is_', 'enable', 'has_']):
                placeholders.append(f'{arg} = True')
            else:
                placeholders.append(f'{arg} = None  # TODO: Set value')

        return "\n    ".join(placeholders) if placeholders else "# No args"

    def _format_call_args(self, func: FunctionInfo) -> str:
        """Format arguments for function call."""
        args = [arg for arg in func.args if arg != 'self']
        return ", ".join(args) if args else ""

    def _enhance_with_model(self, tests: List[GeneratedTest], path: Path) -> List[GeneratedTest]:
        """Enhance tests using fine-tuned model."""
        # Placeholder for model integration
        # When a fine-tuned model is available:
        # 1. Pass function code to model
        # 2. Get smarter test suggestions
        # 3. Add confidence scores
        return tests

    def write_test_file(self, tests: List[GeneratedTest], output_path: Path):
        """Write generated tests to file."""
        header = '''"""
Auto-generated tests by code-covered.
Review and customize before running.
"""

import pytest

'''
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(header)
            for test in tests:
                f.write(f"\n# {test.description}\n")
                f.write(test.test_code)
                f.write("\n")

        logger.info(f"Wrote {len(tests)} tests to {output_path}")

    def generate_test_content(self, tests: List[GeneratedTest]) -> str:
        """Generate test file content as string."""
        header = '''"""Auto-generated tests by code-covered."""

import pytest

'''
        content = header
        for test in tests:
            content += f"\n# {test.description}\n"
            content += test.test_code
            content += "\n"
        return content
