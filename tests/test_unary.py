import unittest

from lark.exceptions import UnexpectedInput

from odenc.ast import AddOp, Constant, MulOp, NegOp, SubOp, VarValue
from odenc.interpreter.io import MockIo
from odenc.langs import LangUnary, LangVar


class UnaryOperationsTest(unittest.TestCase):
    def setUp(self):
        self.lang = LangUnary()

    def expression(self, text):
        return self.lang.parse(f"print({text});").body.block.stmts[0].expr

    def evaluate(self, source, inputs=None):
        io = MockIo(list(inputs or []))
        self.lang.interpret(source, io=io)
        return io.outputs

    def test_unary_minus_ast_for_constant(self):
        self.assertEqual(self.expression("-5"), NegOp(Constant(5)))

    def test_unary_minus_ast_for_variable(self):
        self.assertEqual(self.expression("-x"), NegOp(VarValue("x")))

    def test_unary_minus_ast_for_parenthesized_expression(self):
        self.assertEqual(
            self.expression("-(1 + 2)"),
            NegOp(AddOp(Constant(1), Constant(2))),
        )

    def test_unary_minus_precedes_multiplication(self):
        self.assertEqual(
            self.expression("-2 * 3"),
            MulOp(NegOp(Constant(2)), Constant(3)),
        )

    def test_unary_minus_can_follow_binary_subtraction(self):
        self.assertEqual(
            self.expression("1 - -1"),
            SubOp(Constant(1), NegOp(Constant(1))),
        )
        self.assertEqual(self.evaluate("print(1 - -1);"), [2])

    def test_chained_unary_minus_is_rejected(self):
        for expression in ("--1", "- -1", "--x", "- -x"):
            with self.subTest(expression=expression):
                with self.assertRaises(UnexpectedInput):
                    self.expression(expression)

    def test_parenthesized_nested_negation_is_allowed(self):
        self.assertEqual(
            self.expression("-(-1)"), NegOp(NegOp(Constant(1)))
        )
        self.assertEqual(self.evaluate("print(-(-1));"), [1])

    def test_variable_and_input_runtime(self):
        self.assertEqual(
            self.evaluate("var x; x = -input(); print(-x);", [8]), [8]
        )

    def test_signed_64bit_overflow_wraps(self):
        self.assertEqual(
            self.evaluate("print(-(-9223372036854775808));"),
            [-(1 << 63)],
        )

    def test_out_of_range_literals_are_rejected(self):
        for number in ("9223372036854775808", "-9223372036854775809"):
            with self.subTest(number=number):
                with self.assertRaises(ValueError):
                    self.expression(number)

    def test_pretty_print_round_trip(self):
        for code in (
            "var x; x = 3; print(-(x + 1) * -2);",
            "print(1 - -1);",
            "print(-(-1));",
            "print(-(-9223372036854775808));",
        ):
            with self.subTest(code=code):
                ast = self.lang.parse(code)
                rendered = self.lang.pretty(ast)
                self.assertEqual(self.lang.parse(rendered), ast)

    def test_langvar_rejects_minus_on_variable(self):
        with self.assertRaises(UnexpectedInput):
            LangVar().parse("var x; x = 7; print(-x);")


if __name__ == "__main__":
    unittest.main()
