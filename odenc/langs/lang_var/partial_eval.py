from odenc.ast import (
    AssignStmt, AstNode, BinaryOp, Block, Body, FuncCall, PrintStmt, Program, 
)
#Task 3
class BinaryOpCounter:
    def count(self, node: AstNode) -> int:
        if isinstance(node, BinaryOp):
            return (
                1 + self.count(node.left) + self.count(node.right)
            )

        if isinstance(node, Program):
            return self.count(node.body)

        if isinstance(node, Body):
            return self.count(node.block)


        if isinstance(node, Block):
            return sum(self.count(stmt) for stmt in node.stmts)


        if isinstance(node, PrintStmt):
            return self.count(node.expr)


        if isinstance(node, AssignStmt):
            return self.count(node.value)


        if isinstance(node, FuncCall):
            return sum(self.count(arg) for arg in node.args)
        
        return 0


