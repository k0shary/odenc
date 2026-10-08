from abc import abstractmethod, ABC
from importlib import import_module
from typing import Any

import odenc
from odenc import Program


class Language(ABC):
    @abstractmethod
    def name(self):
        pass

    def import_module(self, submodule: str | Any = None):
        path = f"odenc.langs.lang_{self.name()}"
        if submodule is not None:
            path += f".{submodule}"

        return import_module(path)

    def pretty(self, prog: Program) -> str:
        prettifier = self.import_module("pretty").PrettyPrinter()
        return prettifier.pretty(prog)

    def parse(self, code: str) -> Program:
        return odenc.parse(code, lang=self)

    def interpret(self, prog: str | Program, *args, **kwargs):
        if isinstance(prog, str):
            prog = self.parse(prog)

        return odenc.interpret(prog, lang=self, *args, **kwargs)


class LangInt(Language):
    def name(self):
        return "int"


class LangVar(Language):
    def name(self):
        return "var"
