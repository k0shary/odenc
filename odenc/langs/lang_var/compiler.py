from typing import List, Tuple

from odenc import Program
from odenc.ast import (
    Body,
    Block,
    Stmt,
    AssignStmt,
    PrintStmt,
    Expr,
    Constant,
    BinaryOp,
    FuncCall,
    VarValue,
)
from odenc.interpreter import UnexpectedAstNode


class Compiler:
    def __init__(self):
        self.unique_number = 0

    def get_unique_name(self, name: str = "__tmp") -> str:
        self.unique_number += 1
        return f"{name}_{self.unique_number}"

    ###### Remove complex operations
    def rco_program(self, prog: Program) -> Program:
        body = self.rco_body(prog.body)
        return Program(body)

    def rco_body(self, body: Body) -> Body:
        new_vars, new_block = self.rco_block(body.block)
        return Body(
            var_decls=body.var_decls + new_vars,
            fun_decls={},
            block=new_block,
        )

    def rco_block(self, block: Block) -> Tuple[List[str], Block]:
        new_vars = []
        new_stmts = []

        for stmt in block.stmts:
            vs, ss = self.rco_stmt(stmt)
            new_vars.extend(vs)
            new_stmts.extend(ss)

        return new_vars, Block(new_stmts)

    def rco_stmt(self, stmt: Stmt) -> Tuple[List[str], List[Stmt]]:
        match stmt:
            case PrintStmt(expr):
                new_vars, new_stmts, new_expr = self.rco_expr(expr, True)
                new_stmts.append(PrintStmt(new_expr))
                return new_vars, new_stmts

            case AssignStmt(name, expr):
                new_vars, new_stmts, new_expr = self.rco_expr(expr, False)
                new_stmts.append(AssignStmt(name, new_expr))
                return new_vars, new_stmts

            case _:
                raise UnexpectedAstNode

    def rco_expr(
        self, expr: Expr, need_atomic: bool
    ) -> Tuple[List[str], List[Stmt], Expr]:
        match expr:
            case VarValue(_):
                return [], [], expr

            case Constant(value):
                if need_atomic:
                    new_var = self.get_unique_name()
                    new_stmt = AssignStmt(new_var, Constant(value))
                    return [new_var], [new_stmt], VarValue(new_var)

                else:
                    return [], [], expr

            case BinaryOp(left, right):
                left_vars, left_stms, left_expr = self.rco_expr(left, True)
                right_vars, right_stms, right_expr = self.rco_expr(right, True)

                new_vars = left_vars + right_vars
                new_stmts = left_stms + right_stms

                new_expr = expr.with_new_arguments(left=left_expr, right=right_expr)

                if need_atomic:
                    tmp_var = self.get_unique_name()

                    new_vars.append(tmp_var)
                    new_stmts.append(AssignStmt(tmp_var, new_expr))

                    return new_vars, new_stmts, VarValue(tmp_var)

                else:
                    return new_vars, new_stmts, new_expr

            case FuncCall("input", []):
                if not need_atomic:
                    return [], [], expr

                new_var = self.get_unique_name()
                new_stmt = AssignStmt(new_var, expr)

                return [new_var], [new_stmt], VarValue(new_var)

            case _:
                raise UnexpectedAstNode(expr)
