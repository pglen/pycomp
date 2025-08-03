# Generated from calc.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .calcParser import calcParser
else:
    from calcParser import calcParser

# This class defines a complete generic visitor for a parse tree produced by calcParser.

class calcVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by calcParser#equation.
    def visitEquation(self, ctx:calcParser.EquationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#expression.
    def visitExpression(self, ctx:calcParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#multiplyingExpression.
    def visitMultiplyingExpression(self, ctx:calcParser.MultiplyingExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#powExpression.
    def visitPowExpression(self, ctx:calcParser.PowExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#signedAtom.
    def visitSignedAtom(self, ctx:calcParser.SignedAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#atom.
    def visitAtom(self, ctx:calcParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#scientific.
    def visitScientific(self, ctx:calcParser.ScientificContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#constant.
    def visitConstant(self, ctx:calcParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#variable.
    def visitVariable(self, ctx:calcParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#func_.
    def visitFunc_(self, ctx:calcParser.Func_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#funcname.
    def visitFuncname(self, ctx:calcParser.FuncnameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by calcParser#relop.
    def visitRelop(self, ctx:calcParser.RelopContext):
        return self.visitChildren(ctx)



del calcParser