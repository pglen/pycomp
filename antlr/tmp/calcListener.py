# Generated from calc.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .calcParser import calcParser
else:
    from calcParser import calcParser

# This class defines a complete listener for a parse tree produced by calcParser.
class calcListener(ParseTreeListener):

    # Enter a parse tree produced by calcParser#equation.
    def enterEquation(self, ctx:calcParser.EquationContext):
        pass

    # Exit a parse tree produced by calcParser#equation.
    def exitEquation(self, ctx:calcParser.EquationContext):
        pass


    # Enter a parse tree produced by calcParser#expression.
    def enterExpression(self, ctx:calcParser.ExpressionContext):
        pass

    # Exit a parse tree produced by calcParser#expression.
    def exitExpression(self, ctx:calcParser.ExpressionContext):
        pass


    # Enter a parse tree produced by calcParser#multiplyingExpression.
    def enterMultiplyingExpression(self, ctx:calcParser.MultiplyingExpressionContext):
        pass

    # Exit a parse tree produced by calcParser#multiplyingExpression.
    def exitMultiplyingExpression(self, ctx:calcParser.MultiplyingExpressionContext):
        pass


    # Enter a parse tree produced by calcParser#powExpression.
    def enterPowExpression(self, ctx:calcParser.PowExpressionContext):
        pass

    # Exit a parse tree produced by calcParser#powExpression.
    def exitPowExpression(self, ctx:calcParser.PowExpressionContext):
        pass


    # Enter a parse tree produced by calcParser#signedAtom.
    def enterSignedAtom(self, ctx:calcParser.SignedAtomContext):
        pass

    # Exit a parse tree produced by calcParser#signedAtom.
    def exitSignedAtom(self, ctx:calcParser.SignedAtomContext):
        pass


    # Enter a parse tree produced by calcParser#atom.
    def enterAtom(self, ctx:calcParser.AtomContext):
        pass

    # Exit a parse tree produced by calcParser#atom.
    def exitAtom(self, ctx:calcParser.AtomContext):
        pass


    # Enter a parse tree produced by calcParser#scientific.
    def enterScientific(self, ctx:calcParser.ScientificContext):
        pass

    # Exit a parse tree produced by calcParser#scientific.
    def exitScientific(self, ctx:calcParser.ScientificContext):
        pass


    # Enter a parse tree produced by calcParser#constant.
    def enterConstant(self, ctx:calcParser.ConstantContext):
        pass

    # Exit a parse tree produced by calcParser#constant.
    def exitConstant(self, ctx:calcParser.ConstantContext):
        pass


    # Enter a parse tree produced by calcParser#variable.
    def enterVariable(self, ctx:calcParser.VariableContext):
        pass

    # Exit a parse tree produced by calcParser#variable.
    def exitVariable(self, ctx:calcParser.VariableContext):
        pass


    # Enter a parse tree produced by calcParser#func_.
    def enterFunc_(self, ctx:calcParser.Func_Context):
        pass

    # Exit a parse tree produced by calcParser#func_.
    def exitFunc_(self, ctx:calcParser.Func_Context):
        pass


    # Enter a parse tree produced by calcParser#funcname.
    def enterFuncname(self, ctx:calcParser.FuncnameContext):
        pass

    # Exit a parse tree produced by calcParser#funcname.
    def exitFuncname(self, ctx:calcParser.FuncnameContext):
        pass


    # Enter a parse tree produced by calcParser#relop.
    def enterRelop(self, ctx:calcParser.RelopContext):
        pass

    # Exit a parse tree produced by calcParser#relop.
    def exitRelop(self, ctx:calcParser.RelopContext):
        pass



del calcParser