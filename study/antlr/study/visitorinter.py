import sys
from antlr4 import *

from expr.ExprParser import ExprParser
from expr.ExprVisitor import ExprVisitor

class VisitorInterp(ExprVisitor):

    def visitAtom(self, ctx:ExprParser.AtomContext):
        #print("Atom")
        return int(ctx.getText())

    def visitExpr(self, ctx:ExprParser.ExprContext):

        print("Expr", "cont", ctx.getChildCount())
        print("expr", "text", ctx.getText())
        #print(dir(ctx))
        #print(ctx.getTokens())
        for i in range(0, ctx.getChildCount(), 1):
            print("expr", i, ctx.expr(i))
        #print("expr", "expr" ctx.expr(0)

        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == "(":
                return self.visit(ctx.getChild(1))
            op = ctx.getChild(1).getText()
            v1 = self.visit(ctx.getChild(0))
            v2 = self.visit(ctx.getChild(2))
            if op == "+":
                return v1 + v2
            if op == "-":
                return v1 - v2
            if op == "*":
                return v1 * v2
            if op == "/":
                return v1 / v2
            return 0
        if ctx.getChildCount() == 2:
            opc = ctx.getChild(0).getText()
            if opc == "+":
                return self.visit(ctx.getChild(1))
            if opc == "-":
                return - self.visit(ctx.getChild(1))
            return 0
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        return 0

    def visitStart_(self, ctx:ExprParser.Start_Context):
        print("Start", ctx.getChildCount())
        for i in range(0, ctx.getChildCount(), 1):
        #for i in range(0, ctx.getChildCount(), 2):
            print("start", self.visit(ctx.getChild(i)))
        return 0

    def visitAssn(self, ctx:ExprParser.AssnContext):
        print("Assn", ctx.getChildCount())
        #print(dir(ctx))
        print("assn", ctx.getText())

        for i in range(0, ctx.getChildCount(), 1):
            #print("asssn chld", self.visit(ctx.getChild(i)))
            print("asssn chld", ctx.getChild(i))
# EOF
