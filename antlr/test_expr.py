#!/usr/bin/env   python3

import sys

from antlr4 import *
from expr.ExprLexer import ExprLexer
from expr.ExprParser import ExprParser
from expr.ExprVisitor import ExprVisitor

cdepth = 0

def to_string_tree(root, symbolic_lexer_names, token_delimiter='"', show_token_types=True):
    builder = []
    _to_string_tree_traverse(root, builder, symbolic_lexer_names, token_delimiter, show_token_types)
    return ''.join(builder)

def _to_string_tree_traverse(tree, builder, symbolic_lexer_names, token_delimiter, show_token_types):
    child_list_stack = [[tree]]

    while len(child_list_stack) > 0:
        child_stack = child_list_stack[-1]

        if len(child_stack) == 0:
            child_list_stack.pop()
        else:
            tree = child_stack.pop(0)
            node = str(type(tree).__name__).replace('Context', '')
            node = '{0}{1}'.format(node[0].lower(), node[1:])

            indent = []

            for i in range(0, len(child_list_stack) - 1):
                indent.append('║  ' if len(child_list_stack[i]) > 0 else '   ')

            token_name = ''
            token_type = tree.getPayload().type if node.startswith('terminal') else 0

            if show_token_types and token_type > -1:
                token_name = ' ({0})'.format(symbolic_lexer_names[token_type])

            builder.extend(indent)
            builder.append('╚═ ' if len(child_stack) == 0 else '╠═ ')
            builder.append('{0}{1}{2}{3}'.format(token_delimiter, tree.getText(), token_delimiter, token_name)
                           if node.startswith('terminal') else node)
            builder.append('\n')

            if tree.getChildCount() > 0:
                children = []
                for i in range(0, tree.getChildCount()):
                    children.append(tree.getChild(i))
                child_list_stack.append(children)



def printclass(ccc, strx = "", depth = 1):

    global cdepth

    if cdepth >= 1:
        return

    cdepth += 1
    print(strx, ccc)
    for aa in dir(ccc):
        if aa[:2] == "__":
            continue
        bb = getattr(ccc, aa)
        if bb == None:
            continue

        #if  "builtin_function_or_method" in str(type(bb)):
        #     continue

        print("  " * depth, type(bb), aa, end = " ")
        if type(bb) == type(""):
            print("  " * depth, aa, "s=", bb, end = " ")
        elif type(bb) == type(0):
            print("  " * depth, aa, "i=", bb, end = " ")
        elif type(bb) == type(0.):
            print("  " * depth, aa, "f=", bb, end = " ")
        elif type(bb) == type([]):
            print("  " * depth, aa, "a=", bb, end = " ")
        elif type(bb) == type(()):
            print("  " * depth, aa, "t=", bb, end = " ")
        elif type(bb) == type(None):
            print("  " * depth, aa, "n=", bb, end = " ")
        else:
            try:
                print(" " * depth, aa, "o=", printclass(bb, "", 2), end = " ")
            except:
                pass
            pass
        print()

    cdepth -= 1
    print()

def roundit(ctx, depth = 0):

    if not ctx:
        return
    try:
        for i in range(0, ctx.getChildCount(), 1):
            #print("asssn chld", self.visit(ctx.getChild(i)))
            print(" " * depth, ctx.getChild(i))
            roundit(ctx.getChild(i, depth + 1))
    except:
        print(ctx, sys.exc_info())
        pass

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
            #print()
            print("  " * indent, end = " ")
        print("TOKEN = '{0}' ".format(tree.getText()), end = " ")

    else:
        if prev:
            prev = 0
            print()

        print("{0}{1} {2}:{3} {4}->{5} '{6}'".format("  " * indent,
                        rule_names[tree.getRuleIndex()], indent, cnt,
                                    tree.start, tree.stop, tree.getText()))
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
            chi = ctx.getChild(ii)
            ret = self.visit(chi)
            #print("  chi: '", chi, "'", "text: '",
            #                chi.getText(), "'", "ret:", ret)
            #for iii in range(chi.getChildCount()):
            #    chii = chi.getChild(iii)
            #    print("chii", ii, iii, chii, "text", chii.getText())

        #printclass(ctx, "context: post")

        return ret

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
        #for i in range(0, ctx.getChildCount(), 1):
        ##for i in range(0, ctx.getChildCount(), 2):
        #    print("start", self.visit(ctx.getChild(i)))
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
    #stream.fill()
    parser = ExprParser(stream)

    #print("tok size", stream.size())
    #for aa in stream.getTokens(0, 100):
    #    print("tok", aa)

    #parser.setTrace(True)

    #print(lexer.symbolicNames)
    #print(to_string_tree(parser.start_(), lexer.symbolicNames))

    #if parser.getNumberOfSyntaxErrors() > 0:
    #    print("syntax errors")
    #else:
    tree = parser.start_() # Call the root rule
    vinterp = VisitorInterp()
    vinterp.visit(tree)
    #print("tree:", tree.toStringTree(recog=parser))
    traverse(tree, parser.ruleNames)

#StringIO isinstance

if __name__ == '__main__':
    main(sys.argv)

# EOF
