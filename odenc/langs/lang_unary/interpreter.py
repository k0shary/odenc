from odenc.ast import Expr, NegOp
from odenc.interpreter import to_int64
from odenc.interpreter.context import Context
import odenc.langs.lang_var.interpreter as interpreter_var


class Interpreter(interpreter_var.Interpreter):
    def interp_expr(self, expr: Expr, ctx: Context):
        match expr:
            case NegOp(operand):
                value = self.interp_expr(operand, ctx)
                assert isinstance(value, int)
                return to_int64(-value)
            case _:
                return super().interp_expr(expr, ctx)
