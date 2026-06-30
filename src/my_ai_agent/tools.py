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

            # Security: prevent DoS via large resource consumption
            if isinstance(node.op, ast.Pow) and right > 1000:
                msg = f"Exponent too large: {right}"
                raise ValueError(msg)
            if (
                isinstance(node.op, ast.Mult)
                and isinstance(left, int)
                and isinstance(right, int)
                and (left.bit_length() + right.bit_length() > 10000)
            ):
                msg = "Multiplication result too large"
                raise ValueError(msg)

            result = self._binary_ops[type(node.op)](left, right)

            # Security: limit result magnitude
            if isinstance(result, int | float) and abs(result) > 1e100:
                msg = f"Result magnitude too large: {result}"
                raise ValueError(msg)
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

            # Security: read iteratively to avoid OOM for very large files
            content_parts = []
            chars_read = 0
            with target.open("r", encoding="utf-8") as f:
                while chars_read < max_chars:
                    chunk = f.read(max_chars - chars_read)
                    if not chunk:
                        break
                    content_parts.append(chunk)
                    chars_read += len(chunk)
            return ToolResult("read_file", True, "".join(content_parts))
        except ValueError:
            return ToolResult("read_file", False, "Path is outside the configured workspace")
        except OSError as exc:
            return ToolResult("read_file", False, f"Could not read file: {exc}")
