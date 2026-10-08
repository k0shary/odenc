from odenc.ast import (
    Body,
    Stmt,
    Expr,
    AssignStmt,
    VarValue,
)

from odenc.interpreter.context import Context
import odenc.langs.lang_int.interpreter as interpreter_int


class Interpreter(interpreter_int.Interpreter):
    def interp_body(self, body: Body, ctx: Context | None):
        ctx = Context()
        for var in body.var_decls:
            ctx.declare_var(var)
        assert len(body.fun_decls) == 0
        self.interp_block(body.block, ctx)

    def continue_with_cont(self, cont, ctx: Context):
        if len(cont) == 0:
            return

        self.interp_stmt(cont[0], cont[1:], ctx)

    def interp_stmt(self, stmt: Stmt, cont: list[Stmt], ctx):
        match stmt:
            case AssignStmt(name, expr):
                value = self.interp_expr(expr, ctx)
                assert isinstance(value, int)
                ctx.write_var(name, value)
                self.continue_with_cont(cont, ctx)

            case _:
                super().interp_stmt(stmt, cont, ctx)

    def interp_expr(self, expr: Expr, ctx):
        match expr:
            case VarValue(value):
                return ctx.read_var(value)

            case _:
                return super().interp_expr(expr, ctx)
