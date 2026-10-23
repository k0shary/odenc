from __future__ import annotations
from dataclasses import dataclass, replace
from typing import Self


@dataclass
class AstNode: ...


@dataclass
class Program(AstNode):
    body: Body


@dataclass
class Body(AstNode):
    var_decls: list
    fun_decls: dict
    block: Block


@dataclass
class VarDecls(AstNode):
    names: list[str]


@dataclass
class Stmt(AstNode): ...


@dataclass
class PrintStmt(Stmt):
    expr: Expr


@dataclass
class AssignStmt(Stmt):
    name: str
    value: Expr


@dataclass
class Block(Stmt):
    stmts: list[Stmt]


@dataclass
class Expr(AstNode): ...


@dataclass
class Constant(Expr):
    value: int


@dataclass
class VarValue(Expr):
    name: str


@dataclass
class FuncCall(Expr):
    name: str
    args: list[Expr]


@dataclass
class BinaryOp(Expr):
    left: Expr
    right: Expr

    def with_new_arguments(self, **kwargs) -> Self:
        return replace(self, **kwargs)


class ArithmeticOp(BinaryOp): ...


@dataclass
class AddOp(ArithmeticOp): ...


@dataclass
class SubOp(ArithmeticOp): ...


@dataclass
class MulOp(ArithmeticOp): ...


@dataclass
class DivOp(ArithmeticOp): ...


@dataclass
class ModOp(ArithmeticOp): ...






