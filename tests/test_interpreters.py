import unittest
from pathlib import Path
from typing import Callable

from odenc.langs import Language, LangInt
from odenc.interpreter.io import MockIo
from odenc import Program
from tests.utils import search_test_programs_for, load_test_program


class InterpretersTest(unittest.TestCase):
    def test_int(self):
        self.interpreter_test(LangInt())

    def interpreter_test(self, lang: Language):
        prog_files = search_test_programs_for(lang)
        assert len(prog_files) > 0, "No programs found"

        for prog_path in prog_files:
            with self.subTest(language=lang.name(), program=prog_path):
                self.program_test(lang, prog_path, lambda x: x)

            with self.subTest(
                language=lang.name(), program=prog_path, modifier="pretty"
            ):
                self.program_test(lang, prog_path, lambda p: lang.parse(lang.pretty(p)))

    def program_test(
        self, lang: Language, prog_path: Path, modifier: Callable[[Program], Program]
    ):
        prog = load_test_program(prog_path)
        io = MockIo(prog["in"][:])

        try:
            ast = lang.parse(prog["code"])
            ast = modifier(ast)
            lang.interpret(ast, io=io)
            self.assertIsNone(prog.get("expected_err"), prog)

        except Exception as exception:
            self.assertEqual(
                type(exception).__name__, prog.get("expected_err"), (exception, prog)
            )
            return

        self.assertIsNone(prog.get("expected_err"), prog)
        self.assertEqual(io.outputs, prog["expected_out"], prog)
