from lark import Transformer as LarkTransformer
from lark import v_args

from odenc.ast import (
    AddOp,
    Block,
    Body,
    Constant,
    DivOp,
    FuncCall,
    ModOp,
    MulOp,
    PrintStmt,
    Program,
    SubOp,
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
   

   ///TAsk 1
?num_literal: BINARY_LITERAL            -> num_literal
    |  DECIMAL_LITERAL                  -> num_literal  
    |  HEX_LITERAL                      -> num_literal 

    BINARY_LITERAL:          /-?0b[01]+(_?[01]+)*/
    DECIMAL_LITERAL:         /-?[0-9]+(_?[0-9]+)*/
    HEX_LITERAL:             /-?0x[0-9a-fA-F]+(_?[0-9a-fA-F]+)*/
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
        ##binary_literal
        text = str(value).replace("_", "")
        if text.startswith("-0b"):
            number = -int(text[3:], 2)
        elif text.startswith("0b"):
            number = int(text[2:], 2)

        ##hexadecimal
        elif text.startswith("-0x"):
            number = -int(text[3:], 16)
        elif text.startswith("0x"):
            number = int(text[2:], 16)
        ##decimal
        else:
            number = int(text, 10)

        if not -(1 << 63) <= number < (1 << 63):
            raise ValueError(f"Integer literal {value} is out of range")

        return Constant(number)

    def expr_input(self):
        return FuncCall("input", [])
