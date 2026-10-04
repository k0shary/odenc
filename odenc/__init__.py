from lark import Lark
from lark.exceptions import VisitError

from odenc.ast import Program
from odenc.langs import Language


def parse(text: str, lang: Language):
    parser_mod = lang.import_module("parser")
    parser = Lark(
        parser_mod.GRAMMAR,
        parser="lalr",
        start="program",
    )

    try:
        tree = parser.parse(text)
        return parser_mod.Transformer().transform(tree)
    except VisitError as error:
        raise error.orig_exc
    except Exception as e:
        raise e


def interpret(prog: Program, lang: Language, *args, **kwargs):
    inter_mod = lang.import_module("interpreter")
    return inter_mod.Interpreter(*args, **kwargs).interp_program(prog)


def interpret_code(text: str, lang: Language, *args, **kwargs):
    ast = parse(text, lang)
    return interpret(ast, lang, *args, **kwargs)
