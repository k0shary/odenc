from odenc.interpreter import VariableAlreadyDeclared, UnknownVariable


class Context:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = None

    def is_var_declared(self, name):
        return name in self.vars

    def declare_var(self, name):
        if name in self.vars:
            raise VariableAlreadyDeclared(name)

        self.vars[name] = 0

    def read_var(self, name):
        if name not in self.vars:
            if self.parent is None:
                raise UnknownVariable(name)

            return self.parent.read_var(name)

        return self.vars[name]

    def write_var(self, name, val):
        if name not in self.vars:
            if self.parent is None:
                raise UnknownVariable(name)

            self.parent.write_var(name, val)

        else:
            self.vars[name] = val
