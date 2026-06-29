"""Safe local tools exposed to the agent and CLI."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import operator


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
            left, right = self._eval(node.left), self._eval(node.right)
            # DoS mitigation: limit resource-intensive operations
            if isinstance(node.op, ast.Pow):
                if right > 1000:
                    raise ValueError(f"Exponent too large: {right}")
                if left not in (0, 1, -1) and right > 100:
                    raise ValueError("Result magnitude exceeds safety limit")
            if isinstance(node.op, ast.Mult) and hasattr(left, "bit_length") and \
               hasattr(right, "bit_length") and left.bit_length() + right.bit_length() > 10000:
                raise ValueError("Multiplication operands too large")
            result = self._binary_ops[type(node.op)](left, right)
            if isinstance(result, int | float) and abs(result) > 1e100:
                raise ValueError("Result magnitude exceeds safety limit")
            return result
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

            # OOM mitigation: read only the required amount from the file
            with target.open("r", encoding="utf-8") as f:
                content = f.read(max_chars)
            return ToolResult("read_file", True, content)
        except ValueError:
            return ToolResult("read_file", False, "Path is outside the configured workspace")
        except OSError as exc:
            return ToolResult("read_file", False, f"Could not read file: {exc}")
