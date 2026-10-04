class InterpreterIo:
    def input_int(self):
        val = int(input())
        return val

    def print_int(self, x):
        print(x)


class MockIo(InterpreterIo):
    def __init__(self, inputs=None):
        self.inputs = inputs
        self.outputs = []

    def input_int(self):
        assert len(self.inputs) > 0
        val = self.inputs.pop(0)
        return val

    def print_int(self, x):
        assert isinstance(x, int)
        self.outputs.append(x)
