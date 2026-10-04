class UnexpectedAstNode(Exception):
    pass


class UnknownVariable(Exception):
    pass


class VariableAlreadyDeclared(Exception):
    pass


def to_int64(x: int) -> int:
    unsigned = x % (1 << 64)
    if unsigned >= (1 << 63):
        return unsigned - (1 << 64)
    return unsigned


def trunc_div(lhs: int, rhs: int) -> int:
    quotient = abs(lhs) // abs(rhs)
    return -quotient if (lhs < 0) != (rhs < 0) else quotient


def trunc_mod(lhs: int, rhs: int) -> int:
    return lhs - trunc_div(lhs, rhs) * rhs
