from lark import v_args, Transformer as LarkTransformer
from odenc.ast import (
    Program,
    Body,
    Block,
    PrintStmt,
    AddOp,
    SubOp,
    MulOp,
    DivOp,
    ModOp,
    FuncCall,
    Constant,
)

GRAMMAR = """ 
%import common.INT
%import common.SIGNED_INT
%import common.CNAME
%import common.SH_COMMENT
%import common.CPP_COMMENT
%import common.WS

%ignore SH_COMMENT
%ignore WS
%ignore CPP_COMMENT

?start: program

program: body                           -> program          

body: block                             -> body
block: stmt*                            -> block

stmt: "print" "(" expr ")" ";"          -> stmt_print

?expr: expr_add

?expr_add: expr "+" expr_mul            -> expr_add
    | expr "-" expr_mul                 -> expr_sub
    | expr_mul

?expr_mul: expr_mul "*" atom            -> expr_mul
    | expr_mul "/" atom                 -> expr_div
    | expr_mul "%" atom                 -> expr_mod
    | atom

?atom: num_literal                     
    | "input" "(" ")"                   -> expr_input
    | "(" expr ")"
    
?num_literal: /-?[0-9]+/                -> num_literal              
"""


@v_args(inline=True)
class Transformer(LarkTransformer):
    def program(self, body):
        return Program(body)

    def body(self, block):
        return Body([], {}, block)

    @v_args(inline=False)
    def block(self, stmts):
        return Block(stmts)

    def stmt_print(self, expr):
        return PrintStmt(expr)

    def expr_add(self, left, right):
        return AddOp(left, right)

    def expr_sub(self, left, right):
        return SubOp(left, right)

    def expr_mul(self, left, right):
        return MulOp(left, right)

    def expr_div(self, left, right):
        return DivOp(left, right)

    def expr_mod(self, left, right):
        return ModOp(left, right)

    def num_literal(self, value):
        value = int(value)

        if not -(1 << 63) <= value < (1 << 63):
            raise ValueError(f"Integer literal {value} is out of range")

        return Constant(value)

    def expr_input(self):
        return FuncCall("input", [])
