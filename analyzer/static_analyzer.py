"""
Static Analysis using AST

Complements the embedding-based anomaly detector with rule-based pattern detection.
Finds syntactic issues that don't require semantic understanding.
"""

import ast
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Set, Dict
import logging

logger = logging.getLogger(__name__)


class IssueType(Enum):
    """Categories of detected issues."""
    # Error-prone patterns
    UNHANDLED_EXCEPTION = auto()
    MISSING_NULL_CHECK = auto()
    MISSING_BOUNDS_CHECK = auto()

    # Resource issues
    UNCLOSED_RESOURCE = auto()

    # Logic issues
    UNREACHABLE_CODE = auto()
    EMPTY_EXCEPT = auto()
    MUTABLE_DEFAULT = auto()

    # Complexity
    COMPLEX_BRANCH = auto()

    # Test coverage hints
    NO_ERROR_PATH_TEST = auto()
    NO_EDGE_CASE_TEST = auto()


@dataclass
class StaticIssue:
    """A statically-detected code issue."""
    type: IssueType
    file_path: Path
    line_start: int
    line_end: int
    function_name: Optional[str]
    message: str
    code_snippet: str
    severity: str  # 'error', 'warning', 'info'
    suggested_test: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "type": self.type.name,
            "file": str(self.file_path),
            "line_start": self.line_start,
            "line_end": self.line_end,
            "function": self.function_name,
            "message": self.message,
            "severity": self.severity,
            "suggested_test": self.suggested_test
        }


@dataclass
class FunctionInfo:
    """Extracted function metadata."""
    name: str
    node: ast.FunctionDef
    args: List[str]
    has_return: bool
    raises: Set[str]
    complexity: int
    line_start: int
    line_end: int


class StaticAnalyzer:
    """
    AST-based static analyzer for Python code.

    Detects common bug patterns and generates test suggestions.
    Works alongside the embedding-based AnomalyDetector for comprehensive coverage.
    """

    def __init__(self):
        self.issues: List[StaticIssue] = []
        self.functions: List[FunctionInfo] = []
        self.current_file: Optional[Path] = None
        self.source_lines: List[str] = []

    def analyze_file(self, path: Path) -> List[StaticIssue]:
        """Analyze a single Python file."""
        self.issues = []
        self.functions = []
        self.current_file = path

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            self.source_lines = content.split("\n")
            tree = ast.parse(content, filename=str(path))
        except SyntaxError as e:
            self.issues.append(StaticIssue(
                type=IssueType.UNHANDLED_EXCEPTION,
                file_path=path,
                line_start=e.lineno or 1,
                line_end=e.lineno or 1,
                function_name=None,
                message=f"Syntax error: {e.msg}",
                code_snippet=self._get_snippet(e.lineno or 1, e.lineno or 1),
                severity="error"
            ))
            return self.issues
        except Exception as e:
            logger.error(f"Failed to parse {path}: {e}")
            return self.issues

        self._collect_functions(tree)
        self._detect_issues(tree)
        return self.issues

    def analyze_directory(self, path: Path, recursive: bool = True) -> List[StaticIssue]:
        """Analyze all Python files in a directory."""
        all_issues = []
        pattern = "**/*.py" if recursive else "*.py"

        for py_file in path.glob(pattern):
            if "__pycache__" in str(py_file):
                continue
            issues = self.analyze_file(py_file)
            all_issues.extend(issues)

        return all_issues

    def analyze_code(self, code: str, filename: str = "<string>") -> List[StaticIssue]:
        """Analyze code string directly."""
        self.issues = []
        self.functions = []
        self.current_file = Path(filename)
        self.source_lines = code.split("\n")

        try:
            tree = ast.parse(code, filename=filename)
        except SyntaxError as e:
            self.issues.append(StaticIssue(
                type=IssueType.UNHANDLED_EXCEPTION,
                file_path=self.current_file,
                line_start=e.lineno or 1,
                line_end=e.lineno or 1,
                function_name=None,
                message=f"Syntax error: {e.msg}",
                code_snippet=self._get_snippet(e.lineno or 1, e.lineno or 1),
                severity="error"
            ))
            return self.issues

        self._collect_functions(tree)
        self._detect_issues(tree)
        return self.issues

    def _get_snippet(self, start: int, end: int, context: int = 2) -> str:
        """Extract code snippet with context."""
        start_idx = max(0, start - 1 - context)
        end_idx = min(len(self.source_lines), end + context)
        lines = self.source_lines[start_idx:end_idx]
        return "\n".join(f"{start_idx + i + 1:4d} | {line}" for i, line in enumerate(lines))

    def _collect_functions(self, tree: ast.AST):
        """Collect function metadata."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                info = FunctionInfo(
                    name=node.name,
                    node=node,
                    args=[arg.arg for arg in node.args.args],
                    has_return=self._has_return(node),
                    raises=self._get_raises(node),
                    complexity=self._calculate_complexity(node),
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno
                )
                self.functions.append(info)

    def _has_return(self, node: ast.FunctionDef) -> bool:
        for child in ast.walk(node):
            if isinstance(child, ast.Return) and child.value is not None:
                return True
        return False

    def _get_raises(self, node: ast.FunctionDef) -> Set[str]:
        raises = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Raise) and child.exc:
                if isinstance(child.exc, ast.Call) and isinstance(child.exc.func, ast.Name):
                    raises.add(child.exc.func.id)
                elif isinstance(child.exc, ast.Name):
                    raises.add(child.exc.id)
        return raises

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.Match):
                complexity += len(child.cases)
        return complexity

    def _detect_issues(self, tree: ast.AST):
        """Run all detection passes."""
        self._detect_mutable_defaults(tree)
        self._detect_empty_except(tree)
        self._detect_unclosed_resources(tree)
        self._detect_unreachable_code(tree)
        self._detect_complex_functions()

    def _detect_mutable_defaults(self, tree: ast.AST):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for default in node.args.defaults + node.args.kw_defaults:
                    if default is None:
                        continue
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        self.issues.append(StaticIssue(
                            type=IssueType.MUTABLE_DEFAULT,
                            file_path=self.current_file,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            function_name=node.name,
                            message="Mutable default argument - use None and assign in function body",
                            code_snippet=self._get_snippet(node.lineno, node.lineno),
                            severity="warning",
                            suggested_test=f"def test_{node.name}_mutable_default():\n    # Verify no state leakage between calls\n    r1 = {node.name}()\n    r2 = {node.name}()\n    assert r1 is not r2"
                        ))

    def _detect_empty_except(self, tree: ast.AST):
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    self.issues.append(StaticIssue(
                        type=IssueType.EMPTY_EXCEPT,
                        file_path=self.current_file,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        function_name=self._find_enclosing_function(node),
                        message="Bare except catches all exceptions including KeyboardInterrupt",
                        code_snippet=self._get_snippet(node.lineno, node.end_lineno or node.lineno),
                        severity="warning"
                    ))
                elif len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    self.issues.append(StaticIssue(
                        type=IssueType.EMPTY_EXCEPT,
                        file_path=self.current_file,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        function_name=self._find_enclosing_function(node),
                        message="Exception silently ignored - consider logging or re-raising",
                        code_snippet=self._get_snippet(node.lineno, node.end_lineno or node.lineno),
                        severity="info"
                    ))

    def _detect_unclosed_resources(self, tree: ast.AST):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = None
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    func_name = node.func.attr

                if func_name == "open" and not self._is_inside_with(tree, node):
                    self.issues.append(StaticIssue(
                        type=IssueType.UNCLOSED_RESOURCE,
                        file_path=self.current_file,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        function_name=self._find_enclosing_function(node),
                        message="File opened without context manager - may not be closed on error",
                        code_snippet=self._get_snippet(node.lineno, node.end_lineno or node.lineno),
                        severity="warning"
                    ))

    def _detect_unreachable_code(self, tree: ast.AST):
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.For, ast.While)):
                body = node.body
                for i, stmt in enumerate(body[:-1]):
                    if isinstance(stmt, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                        next_stmt = body[i + 1]
                        self.issues.append(StaticIssue(
                            type=IssueType.UNREACHABLE_CODE,
                            file_path=self.current_file,
                            line_start=next_stmt.lineno,
                            line_end=next_stmt.end_lineno or next_stmt.lineno,
                            function_name=self._find_enclosing_function(next_stmt),
                            message="Unreachable code after return/raise/break",
                            code_snippet=self._get_snippet(next_stmt.lineno, next_stmt.end_lineno or next_stmt.lineno),
                            severity="error"
                        ))

    def _detect_complex_functions(self):
        for func in self.functions:
            if func.complexity > 10:
                self.issues.append(StaticIssue(
                    type=IssueType.COMPLEX_BRANCH,
                    file_path=self.current_file,
                    line_start=func.line_start,
                    line_end=func.line_end,
                    function_name=func.name,
                    message=f"High cyclomatic complexity ({func.complexity}) - consider refactoring",
                    code_snippet=self._get_snippet(func.line_start, min(func.line_start + 5, func.line_end)),
                    severity="warning"
                ))

    def _find_enclosing_function(self, target_node: ast.AST) -> Optional[str]:
        for func in self.functions:
            if func.line_start <= getattr(target_node, 'lineno', 0) <= func.line_end:
                return func.name
        return None

    def _is_inside_with(self, tree: ast.AST, target: ast.AST) -> bool:
        for node in ast.walk(tree):
            if isinstance(node, ast.With):
                for item in node.items:
                    if item.context_expr is target:
                        return True
        return False

    def get_functions(self) -> List[FunctionInfo]:
        """Return collected function metadata."""
        return self.functions

    def summary(self) -> Dict[str, int]:
        """Return issue counts by severity."""
        return {
            "error": len([i for i in self.issues if i.severity == "error"]),
            "warning": len([i for i in self.issues if i.severity == "warning"]),
            "info": len([i for i in self.issues if i.severity == "info"]),
            "total": len(self.issues)
        }
