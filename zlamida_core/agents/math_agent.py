from __future__ import annotations

"""Agent that evaluates arithmetic expressions."""

import ast
import operator as op
from typing import Any
from pathlib import Path

from .base import Agent


class MathAgent(Agent):
    """Evaluate simple arithmetic expressions safely."""

    _OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
        ast.USub: op.neg,
    }

    def run(self, task: Any) -> Any:
        result = self._eval(str(task))
        self._record(task, result)
        return result

    def _eval(self, expr: str) -> Any:
        """Evaluate an arithmetic expression using AST parsing."""
        def _eval_node(node: ast.AST) -> Any:
            if isinstance(node, ast.Num):
                return node.n
            if isinstance(node, ast.UnaryOp) and type(node.op) in self._OPERATORS:
                return self._OPERATORS[type(node.op)](_eval_node(node.operand))
            if isinstance(node, ast.BinOp) and type(node.op) in self._OPERATORS:
                return self._OPERATORS[type(node.op)](
                    _eval_node(node.left), _eval_node(node.right)
                )
            raise ValueError(f"Unsupported expression: {expr}")

        tree = ast.parse(expr, mode="eval")
        return _eval_node(tree.body)
