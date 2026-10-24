from odenc.ast import (
        AssignStmt,
        AstNode,
        BinaryOp,
        Block,
        Body,
        FuncCall,
        PrintStmt,
        Program,
        Constant,
        DivOp,
        Expr,
        ModOp,
        MulOp,
        Stmt,
        SubOp,
        AddOp 
        )
from odenc.interpreter import (
        to_int64,
        trunc_div,
        trunc_mod
        )

#Task 3a)
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


#Task 3b)
class PartialEval:

    ##new tree
    def pe_program(self, prog: Program) -> Program:
        return Program(body=self.pe_body(prog.body))

    def pe_body(self, body: Body) -> Body:
        return Body(var_decls=body.var_decls,
                    fun_decls=body.fun_decls,
                    block=self.pe_block(body.block)
                    )

    ##iterate through each statement one by one to optimize
    def pe_block(self, block: Block) -> Block:
        return Block(stmts=[self.pe_stmt(statement) for statement in block.stmts])

    ##only the expressions will be evaluated and collapsed
    def pe_stmt(self, stmt: Stmt) -> Stmt:
        if isinstance(stmt, PrintStmt):
            return PrintStmt(expr=self.pe_expr(stmt.expr))


        if isinstance(stmt, AssignStmt):
            return AssignStmt(name=stmt.name,
                              value=self.pe_expr(stmt.value))

        if isinstance(stmt, Block):
            return self.pe_block(stmt)

        return stmt 


    def pe_expr(self, expr:Expr) -> Expr:
        if isinstance(expr, BinaryOp):
            new_left = self.pe_expr(expr.left)
            new_right= self.pe_expr(expr.right)

            new = expr.with_new_arguments(left=new_left,
                                          right=new_right)

            if isinstance(new_left, Constant) and isinstance(new_right, Constant):
                result = self._evaluate(new,
                                        new_left.value,
                                        new_right.value)
                if result is not None:
                    return Constant(value=result)
            return new

        if isinstance(expr, FuncCall):
            return FuncCall(name=expr.name,
                            args=[self.pe_expr(a) for a in expr.args]
                            )
        return expr

    def _evaluate(self, node: BinaryOp, a: int, b: int) -> int | None:
        ##wrapping in int64 like the interpreter
        if isinstance(node, AddOp):
            return to_int64(a + b)


        if isinstance(node, SubOp):
            return to_int64(a - b)

        if isinstance(node, MulOp):
            return to_int64(a * b)

        #left to crash at runtime
        if b == 0:
            return None

        ##we round to zero in odenc
        if isinstance(node, DivOp):
            return to_int64(trunc_div(a , b))
        
        if isinstance(node, ModOp):
            return to_int64(trunc_mod(a , b))

        return None
