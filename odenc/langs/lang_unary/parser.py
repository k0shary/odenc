from lark import v_args

from odenc.ast import Constant, NegOp
import odenc.langs.lang_var.parser as parser_var

GRAMMAR = (
    parser_var.GRAMMAR
    + r"""
// Unary minus has C precedence: tighter than *, /, % and +, -.
// The operand is an atom (not another unary expression), so --x is invalid.
%override expr_mul: expr_mul "*" expr_unary  -> expr_mul
    | expr_mul "/" expr_unary              -> expr_div
    | expr_mul "%" expr_unary              -> expr_mod
    | expr_unary                          -> expr_unary_passthrough

?expr_unary: INT64_MIN_LITERAL                 -> expr_int64_min
    | "-" atom                              -> expr_neg
    | atom

// LangInt allows signed numeric terminals. 
// In LangUnary, the sign is an operator instead.
INT64_MIN_LITERAL: /-9223372036854775808(?![0-9_])/
%override BINARY_LITERAL: /0b[01]+(_?[01]+)*/
%override DECIMAL_LITERAL: /[0-9]+(_?[0-9]+)*/
%override HEX_LITERAL: /0x[0-9a-fA-F]+(_?[0-9a-fA-F]+)*/
"""
)


@v_args(inline=True)
class Transformer(parser_var.Transformer):
    def expr_unary_passthrough(self, expr):
        return expr

    def expr_int64_min(self, _value):
        return Constant(-(1 << 63))

    def expr_neg(self, operand):
        return NegOp(operand)
