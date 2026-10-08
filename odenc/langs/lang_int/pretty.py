from __future__ import annotations

from typing import List

from odenc.ast import (
    Program,
    Body,
    Block,
    Stmt,
    AddOp,
    SubOp,
    MulOp,
    DivOp,
    ModOp,
    PrintStmt,
    AssignStmt,
    Constant,
    BinaryOp,
    VarValue,
    FuncCall,
    Expr,
)
from odenc.interpreter import UnexpectedAstNode

type Line = str


class Indented:
    INDENT = "    "

    def __init__(self, items: List[Line | Indented]):
        self.items = items

    def pretty_lines(self, indent="") -> list[str]:
        lines = []
        for item in self.items:
            if isinstance(item, Indented):
                lines += item.pretty_lines(self.INDENT + indent)
            else:
                lines.append(indent + str(item))

        return lines


class PrettyPrinter:
    def pretty(self, prog: Program):
        return "\n".join(self.pretty_program(prog).pretty_lines())

    def pretty_program(self, prog: Program):
        return self.pretty_body(prog.body)

    def pretty_body(self, body: Body) -> Indented:
        items = []
        if body.var_decls:
            items.append("var " + ", ".join(body.var_decls) + ";")

        return Indented(items + self.pretty_block(body.block))

    def pretty_block(self, block: Block):
        items = []
        for stmt in block.stmts:
            items += self.pretty_stmt(stmt)

        return items

    def pretty_stmt(self, stmt: Stmt):
        match stmt:
            case PrintStmt(expr):
                pretty_expr = self.pretty_expr(expr, False)
                return [f"print({pretty_expr});"]

            case AssignStmt(name, value):
                return [f"{name} = {self.pretty_expr(value, False)};"]

            case _:
                raise UnexpectedAstNode(stmt)

    def pretty_binop(self, op: BinaryOp) -> str:
        match op:
            case AddOp():
                return "+"

            case SubOp():
                return "-"

            case MulOp():
                return "*"

            case DivOp():
                return "/"

            case ModOp():
                return "%"

            case _:
                raise UnexpectedAstNode(op)

    def pretty_expr(self, expr: Expr, in_complex: bool) -> str:
        match expr:
            case Constant(val):
                return str(val)

            case VarValue(name):
                return name

            case BinaryOp(lhs, rhs):
                pretty_left = self.pretty_expr(lhs, True)
                pretty_right = self.pretty_expr(rhs, True)
                pretty_op = self.pretty_binop(expr)

                text = f"{pretty_left} {pretty_op} {pretty_right}"
                if in_complex:
                    return f"({text})"
                return text

            case FuncCall("input", []):
                return "input()"

            case _:
                raise UnexpectedAstNode(expr)
