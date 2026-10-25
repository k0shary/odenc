import unittest
from tests import test_interpreters
from tests.utils import search_test_programs_for
from odenc.interpreter.io import MockIo
from odenc.langs import LangVar
from odenc.langs.lang_var.partial_eval import BinaryOpCounter, PartialEval

class PartialEvalTest(unittest.TestCase):
    def test_all_programs_match_test_lines(self):
        lang = LangVar()
        for path in search_test_programs_for(lang):
            with self.subTest(program=path):
                test_interpreters.InterpretersTest.program_test(
                    self, lang, path, PartialEval().pe_program
                )
