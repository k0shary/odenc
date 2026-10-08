from lark import v_args
import odenc.langs.lang_var.parser as parser_var

GRAMMAR = (
    parser_var.GRAMMAR
    + r"""
# TODO: ADD YOUR LARK GRAMMAR HERE
"""
)


@v_args(inline=True)
class Transformer(parser_var.Transformer):
    # TODO: ADD YOUR VISITORS HERE
    pass
