# Task 2
from odenc import Program
from odenc.ast import (
    AssignStmt,
    PrintStmt,
    VarValue,
    BinaryOp,
)


class SemCheckUndeclaredVariable(Exception):
    pass


class SemCheckUninitializedVariable(Exception):
    pass


class SemCheck:
    def cvd_program(self, prog: Program):
        declared = set(prog.body.var_decls)

        ##verifies that every variable have been declared
        def check(expr):
            if isinstance(expr, VarValue):
                if expr.name not in declared:
                    raise SemCheckUndeclaredVariable(expr.name)

            elif isinstance(expr, BinaryOp):
                check(expr.left)
                check(expr.right)

        for stmt in prog.body.block.stmts:
            if isinstance(stmt, AssignStmt):
                if stmt.name not in declared:
                    raise SemCheckUndeclaredVariable(stmt.name)
                check(stmt.value)

            elif isinstance(stmt, PrintStmt):
                check(stmt.expr)

    def rbw_program(self, prog: Program):
        ##keeps track of variables that have received a value
        initialized = set()

        ##verifies that every variable have been initialized
        def check(expr):
            if isinstance(expr, VarValue):
                if expr.name not in initialized:
                    raise SemCheckUninitializedVariable(expr.name)

            elif isinstance(expr, BinaryOp):
                check(expr.left)
                check(expr.right)

        for stmt in prog.body.block.stmts:
            if isinstance(stmt, AssignStmt):
                check(stmt.value)
                initialized.add(stmt.name)

            elif isinstance(stmt, PrintStmt):
                check(stmt.expr)
