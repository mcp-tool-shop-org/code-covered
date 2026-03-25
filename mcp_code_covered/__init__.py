"""
MCP adapter for code-covered.

Exposes the code_covered.gaps tool for MCP hosts.
"""

from mcp_code_covered.tool import handle

__all__ = ["handle"]
__version__ = "1.0.0"
