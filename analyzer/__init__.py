"""
Code Analysis Module for Code-Covered

Three complementary analysis approaches:
- CoverageParser: Reads coverage.py output to find untested code
- GapAnalyzer: Maps uncovered lines to specific test suggestions
- StaticAnalyzer: AST-based syntactic pattern detection
- AnomalyDetector: Embedding-based semantic outlier detection (HNSW)

Together they provide comprehensive code coverage analysis.
"""

from .anomaly_detector import AnomalyDetector, AnomalyScore
from .static_analyzer import StaticAnalyzer, StaticIssue, IssueType, FunctionInfo
from .test_generator import TestGenerator, GeneratedTest
from .coverage_gaps import (
    CoverageParser,
    CoverageReport,
    FileCoverage,
    GapAnalyzer,
    GapSuggestion,
    UncoveredBlock,
    find_coverage_gaps,
    print_coverage_gaps,
)

__all__ = [
    # Coverage gap analysis
    "CoverageParser",
    "CoverageReport",
    "FileCoverage",
    "GapAnalyzer",
    "GapSuggestion",
    "UncoveredBlock",
    "find_coverage_gaps",
    "print_coverage_gaps",
    # Static analysis
    "AnomalyDetector", "AnomalyScore",
    "StaticAnalyzer", "StaticIssue", "IssueType", "FunctionInfo",
    "TestGenerator", "GeneratedTest",
]
