"""Safe local tools exposed to the agent and CLI."""

from __future__ import annotations

import ast
import operator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ToolResult:
    name: str
    ok: bool
    output: str


class Calculator:
    """Evaluate a small, safe subset of Python arithmetic expressions."""

    _binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    _unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def run(self, expression: str) -> ToolResult:
        try:
            tree = ast.parse(expression, mode="eval")
            value = self._eval(tree.body)
        except Exception as exc:  # noqa: BLE001 - surface concise tool errors to users.
            return ToolResult("calculator", False, f"Invalid expression: {exc}")
        return ToolResult("calculator", True, str(value))

    def _eval(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in self._binary_ops:
            left = self._eval(node.left)
            right = self._eval(node.right)
            return self._binary_ops[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in self._unary_ops:
            return self._unary_ops[type(node.op)](self._eval(node.operand))
        msg = f"Unsupported syntax: {ast.dump(node, include_attributes=False)}"
        raise ValueError(msg)


class WorkspaceReader:
    """Read text files without allowing path traversal outside the configured workspace."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()

    def run(self, relative_path: str, max_chars: int = 8_000) -> ToolResult:
        try:
            target = (self.workspace / relative_path).resolve()
            target.relative_to(self.workspace)
            if not target.is_file():
                return ToolResult("read_file", False, f"Not a file: {relative_path}")
            content = target.read_text(encoding="utf-8")
            if len(content) > max_chars:
                return ToolResult(
                    "read_file",
                    True,
                    f"{content[:max_chars]}\n\n[... truncated to {max_chars} chars ...]",
                )
            return ToolResult("read_file", True, content)
        except ValueError:
            return ToolResult("read_file", False, "Path is outside the configured workspace")
        except OSError as exc:
            return ToolResult("read_file", False, f"Could not read file: {exc}")
