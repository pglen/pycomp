#!/usr/bin/env   python3

import sys

from antlr4 import *
from expr.ExprLexer import ExprLexer
from expr.ExprParser import ExprParser
from expr.ExprVisitor import ExprVisitor

cnt = 0
prev = ""

def traverse(tree, rule_names, indent = 0):
    global cnt, prev
    cnt += 1
    if tree.getText() == "<EOF>":
        return
    #elif isinstance(tree, TerminalNodeImpl):
    elif isinstance(tree, TerminalNode):
        if not prev:
            prev = 1
            print("   " * indent, "TOKENS:", end = " ")
        print(" '{0}' ".format(tree.getText()), end = "")
    else:
        if prev:  prev = 0 ;  print()
        #print("{0}{1} {2}:{3} {4}->{5} '{6}'".format(" . " * indent,
        #                rule_names[tree.getRuleIndex()], indent, cnt,
        #                            tree.start, tree.stop, tree.getText()))
        print("{0}{1} {2}:{3} '{4}'".format("   " * indent,
                            rule_names[tree.getRuleIndex()], indent,
                                cnt, tree.getText()))
        for child in tree.children:
            traverse(child, rule_names, indent + 1)

class VisitorInterp(ExprVisitor):

    def visitAtom(self, ctx:ExprParser.AtomContext):
        #printclass(ctx, "Atom:")
        #print("Atom", ctx.getText())
        return int(ctx.getText())

    def visitExpr(self, ctx:ExprParser.ExprContext):

        #printclass(ctx, "context:")
        #print("Expr", "count", ctx.getChildCount())
        #print("expr", "text", ctx.getText())
        #print("expr", "ruleindex", ctx.getRuleIndex())
        #print(.getSymbol())
        #print("expr PLUS", ctx.PLUS())
        #print("ctx getRuleContext", ctx.getRuleContext())
        #print("ctx payload", ctx.getPayload().type)
        #print("ctx children", ctx.children)
        #print("ctx tokindex", ctx.tokenIndex)
        #print("gettokens", ctx.getTokens(expr))
        for ii in range(ctx.getChildCount()):
            #print("ii", ii)
            chi = ctx.getChild(ii)
            ret = self.visit(chi)
            #print(ii, "chi: '", chi, "'", "text: '",
            #                    chi.getText(), "'", "ret:", ret)
        #printclass(ctx, "context: post")

        return None

        #print(printclass(chi, "chi num = %d text = '%s'" % (ii, chi.getText())))
        #print("expr", i, "context:", printclass(ctx.getRuleContext()))
        #print("expr", i, "text", ctx.getText())
        #pass

        #if ctx.getChildCount() == 3:
        #    if ctx.getChild(0).getText() == "(":
        #        return self.visit(ctx.getChild(1))
        #    op = ctx.getChild(1).getText()
        #    v1 = self.visit(ctx.getChild(0))
        #    v2 = self.visit(ctx.getChild(2))
        #    if op == "+":
        #        return v1 + v2
        #    if op == "-":
        #        return v1 - v2
        #    if op == "*":
        #        return v1 * v2
        #    if op == "/":
        #        return v1 / v2
        #    return 0
        #if ctx.getChildCount() == 2:
        #    opc = ctx.getChild(0).getText()
        #    if opc == "+":
        #        return self.visit(ctx.getChild(1))
        #    if opc == "-":
        #        return - self.visit(ctx.getChild(1))
        #    return 0
        #if ctx.getChildCount() == 1:
        #    return self.visit(ctx.getChild(0))
        #
        #return 0

    def visitStart_(self, ctx:ExprParser.Start_Context):
        #print("Start", ctx.getChildCount())
        for i in range(0, ctx.getChildCount(), 1):
            ret = self.visit(ctx.getChild(i))
            #print("start", i, ret)
        #ans = ctx.getAncestors(ctx)
        #print("ans", ans)
        return 0

    def visitAssn(self, ctx:ExprParser.AssnContext):
        print("Assn", ctx.getChildCount())
        #print(dir(ctx))
        #print("assn", ctx.getText())
        #roundit(ctx)
        for i in range(0, ctx.getChildCount(), 1):
            print("asssn chld", self.visit(ctx.getChild(i)))
        #    print("asssn chld", ctx.getChild(i))

def main(argv):

    #fp = open(argv[1]); sss = fp.read(); fp.close()
    #input_stream = InputStream(sss)
    input_stream = FileStream(argv[1])
    lexer = ExprLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ExprParser(stream)

    #print(lexer.symbolicNames)
    #print(to_string_tree(parser.start_(), lexer.symbolicNames))

    #if parser.getNumberOfSyntaxErrors() > 0:
    #    print("syntax errors")
    #else:
    tree = parser.start_() # Call the root rule
    vinterp = VisitorInterp()
    vinterp.visit(tree)
    #print("tree:", tree.toStringTree(recog=parser))
    traverse(tree, parser.ruleNames, 0)
    print()

if __name__ == '__main__':
    main(sys.argv)

# EOF
