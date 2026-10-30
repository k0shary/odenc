from __future__ import annotations

from odenc.ast import Constant, Expr, FuncCall, NegOp, VarValue
from odenc.langs.lang_var.pretty import PrettyPrinter as PrettyPrinterVar


class PrettyPrinter(PrettyPrinterVar):
    def pretty_expr(self, expr: Expr, in_complex: bool) -> str:
        match expr:
            case NegOp(operand):
                # Parenthesize a complex or already-negated operand to preserve
                # semantics and avoid emitting forbidden -- chains.
                if isinstance(operand, Constant) and operand.value < 0:
                    return f"-({self.pretty_expr(operand, False)})"
                if isinstance(operand, (Constant, VarValue, FuncCall)):
                    return f"-{self.pretty_expr(operand, True)}"
                return f"-({self.pretty_expr(operand, False)})"
            case _:
                return super().pretty_expr(expr, in_complex)
