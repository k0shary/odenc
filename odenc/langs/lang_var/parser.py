from lark import v_args
from odenc.ast import Body, AssignStmt, VarValue
import odenc.langs.lang_int.parser as parser_int

GRAMMAR = (
    parser_int.GRAMMAR
    + r"""
ident: /(_[a-zA-Z]|[a-zA-Z])[_a-zA-Z0-9]*/ -> ident              
var_decl: "var" ident ("," ident)* ";"     -> var_decl

%override body: var_decl? block            -> body

%extend stmt: ident "=" expr ";"           -> stmt_assign
%extend atom: ident                        -> expr_var_value
"""
)


@v_args(inline=True)
class Transformer(parser_int.Transformer):
    def body(self, *children):
        if len(children) == 1:
            var_decls = []
            block = children[0]
        else:
            var_decls, block = children

        return Body(var_decls=var_decls, fun_decls={}, block=block)

    @v_args(inline=False)
    def var_decl(self, vars):
        return list(vars)

    def stmt_assign(self, name: str, rhs):
        return AssignStmt(name, rhs)

    def expr_var_value(self, name: str):
        return VarValue(name)

    def ident(self, x):
        return str(x)
