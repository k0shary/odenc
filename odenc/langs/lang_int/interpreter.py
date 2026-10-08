from odenc.ast import (
    Program,
    Body,
    Block,
    Stmt,
    PrintStmt,
    AddOp,
    SubOp,
    MulOp,
    DivOp,
    ModOp,
    Expr,
    BinaryOp,
    FuncCall,
    Constant,
)
from odenc.interpreter import UnexpectedAstNode, to_int64, trunc_div, trunc_mod
from odenc.interpreter.context import Context
from odenc.interpreter.io import InterpreterIo


class Interpreter:
    def __init__(self, io: InterpreterIo = InterpreterIo()):
        self.io = io

    def interp_program(self, prog: Program):
        self.interp_body(prog.body, None)

    def interp_body(self, body: Body, ctx: Context | None):
        assert len(body.var_decls) == 0
        assert len(body.fun_decls) == 0
        self.interp_block(body.block, ctx)

    def interp_block(self, block: Block, ctx):
        if len(block.stmts) == 0:
            return

        self.interp_stmt(block.stmts[0], block.stmts[1:], ctx)

    def continue_with_cont(self, cont, ctx: Context):
        if len(cont) == 0:
            return

        self.interp_stmt(cont[0], cont[1:], ctx)

    def interp_stmt(self, stmt: Stmt, cont: list[Stmt], ctx):
        match stmt:
            case PrintStmt(expr):
                value = self.interp_expr(expr, ctx)
                assert isinstance(value, int)
                self.io.print_int(value)
                self.continue_with_cont(cont, ctx)

            case _:
                raise UnexpectedAstNode(stmt)

    def interp_expr(self, expr: Expr, ctx):
        match expr:
            case Constant(val):
                return to_int64(val)

            case BinaryOp(left, right):
                value_left = self.interp_expr(left, ctx)
                value_right = self.interp_expr(right, ctx)

                assert isinstance(value_left, int)
                assert isinstance(value_right, int)

                match expr:
                    case AddOp(_, _):
                        return to_int64(value_left + value_right)
                    case SubOp(_, _):
                        return to_int64(value_left - value_right)
                    case MulOp(_, _):
                        return to_int64(value_left * value_right)
                    case DivOp(_, _):
                        return to_int64(trunc_div(value_left, value_right))
                    case ModOp(_, _):
                        return to_int64(trunc_mod(value_left, value_right))
                    case _:
                        raise UnexpectedAstNode(expr)

            case FuncCall("input", []):
                value = self.io.input_int()
                if not -(1 << 63) <= value < (1 << 63):
                    raise ValueError(f"Input {value} is out of signed 64bit range")

                return value

            case _:
                raise UnexpectedAstNode(expr)
