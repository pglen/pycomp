# Generated from Expr.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,11,142,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,5,0,10,8,0,10,0,12,
        0,13,9,0,1,0,5,0,16,8,0,10,0,12,0,19,9,0,1,0,5,0,22,8,0,10,0,12,
        0,25,9,0,1,0,5,0,28,8,0,10,0,12,0,31,9,0,3,0,33,8,0,1,1,5,1,36,8,
        1,10,1,12,1,39,9,1,1,1,1,1,5,1,43,8,1,10,1,12,1,46,9,1,1,1,1,1,5,
        1,50,8,1,10,1,12,1,53,9,1,1,1,1,1,5,1,57,8,1,10,1,12,1,60,9,1,1,
        2,1,2,1,2,1,2,5,2,66,8,2,10,2,12,2,69,9,2,1,2,1,2,1,2,5,2,74,8,2,
        10,2,12,2,77,9,2,1,2,1,2,5,2,81,8,2,10,2,12,2,84,9,2,1,2,1,2,3,2,
        88,8,2,1,2,1,2,5,2,92,8,2,10,2,12,2,95,9,2,1,2,1,2,5,2,99,8,2,10,
        2,12,2,102,9,2,1,2,1,2,1,2,5,2,107,8,2,10,2,12,2,110,9,2,1,2,1,2,
        5,2,114,8,2,10,2,12,2,117,9,2,1,2,1,2,1,2,5,2,122,8,2,10,2,12,2,
        125,9,2,1,2,1,2,5,2,129,8,2,10,2,12,2,132,9,2,1,2,5,2,135,8,2,10,
        2,12,2,138,9,2,1,3,1,3,1,3,0,1,4,4,0,2,4,6,0,3,2,0,2,2,8,8,1,0,4,
        5,1,0,9,10,160,0,32,1,0,0,0,2,37,1,0,0,0,4,87,1,0,0,0,6,139,1,0,
        0,0,8,10,5,11,0,0,9,8,1,0,0,0,10,13,1,0,0,0,11,9,1,0,0,0,11,12,1,
        0,0,0,12,17,1,0,0,0,13,11,1,0,0,0,14,16,3,2,1,0,15,14,1,0,0,0,16,
        19,1,0,0,0,17,15,1,0,0,0,17,18,1,0,0,0,18,33,1,0,0,0,19,17,1,0,0,
        0,20,22,5,11,0,0,21,20,1,0,0,0,22,25,1,0,0,0,23,21,1,0,0,0,23,24,
        1,0,0,0,24,29,1,0,0,0,25,23,1,0,0,0,26,28,3,4,2,0,27,26,1,0,0,0,
        28,31,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,33,1,0,0,0,31,29,1,
        0,0,0,32,11,1,0,0,0,32,23,1,0,0,0,33,1,1,0,0,0,34,36,5,11,0,0,35,
        34,1,0,0,0,36,39,1,0,0,0,37,35,1,0,0,0,37,38,1,0,0,0,38,40,1,0,0,
        0,39,37,1,0,0,0,40,44,5,9,0,0,41,43,5,11,0,0,42,41,1,0,0,0,43,46,
        1,0,0,0,44,42,1,0,0,0,44,45,1,0,0,0,45,47,1,0,0,0,46,44,1,0,0,0,
        47,51,5,1,0,0,48,50,5,11,0,0,49,48,1,0,0,0,50,53,1,0,0,0,51,49,1,
        0,0,0,51,52,1,0,0,0,52,54,1,0,0,0,53,51,1,0,0,0,54,58,3,4,2,0,55,
        57,5,11,0,0,56,55,1,0,0,0,57,60,1,0,0,0,58,56,1,0,0,0,58,59,1,0,
        0,0,59,3,1,0,0,0,60,58,1,0,0,0,61,62,6,2,-1,0,62,88,3,6,3,0,63,67,
        7,0,0,0,64,66,5,11,0,0,65,64,1,0,0,0,66,69,1,0,0,0,67,65,1,0,0,0,
        67,68,1,0,0,0,68,70,1,0,0,0,69,67,1,0,0,0,70,88,3,4,2,5,71,75,5,
        6,0,0,72,74,5,11,0,0,73,72,1,0,0,0,74,77,1,0,0,0,75,73,1,0,0,0,75,
        76,1,0,0,0,76,78,1,0,0,0,77,75,1,0,0,0,78,82,3,4,2,0,79,81,5,11,
        0,0,80,79,1,0,0,0,81,84,1,0,0,0,82,80,1,0,0,0,82,83,1,0,0,0,83,85,
        1,0,0,0,84,82,1,0,0,0,85,86,5,7,0,0,86,88,1,0,0,0,87,61,1,0,0,0,
        87,63,1,0,0,0,87,71,1,0,0,0,88,136,1,0,0,0,89,93,10,4,0,0,90,92,
        5,11,0,0,91,90,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,93,94,1,0,0,0,
        94,96,1,0,0,0,95,93,1,0,0,0,96,100,5,3,0,0,97,99,5,11,0,0,98,97,
        1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,1,0,0,0,101,103,1,
        0,0,0,102,100,1,0,0,0,103,135,3,4,2,5,104,108,10,3,0,0,105,107,5,
        11,0,0,106,105,1,0,0,0,107,110,1,0,0,0,108,106,1,0,0,0,108,109,1,
        0,0,0,109,111,1,0,0,0,110,108,1,0,0,0,111,115,7,1,0,0,112,114,5,
        11,0,0,113,112,1,0,0,0,114,117,1,0,0,0,115,113,1,0,0,0,115,116,1,
        0,0,0,116,118,1,0,0,0,117,115,1,0,0,0,118,135,3,4,2,4,119,123,10,
        2,0,0,120,122,5,11,0,0,121,120,1,0,0,0,122,125,1,0,0,0,123,121,1,
        0,0,0,123,124,1,0,0,0,124,126,1,0,0,0,125,123,1,0,0,0,126,130,7,
        0,0,0,127,129,5,11,0,0,128,127,1,0,0,0,129,132,1,0,0,0,130,128,1,
        0,0,0,130,131,1,0,0,0,131,133,1,0,0,0,132,130,1,0,0,0,133,135,3,
        4,2,3,134,89,1,0,0,0,134,104,1,0,0,0,134,119,1,0,0,0,135,138,1,0,
        0,0,136,134,1,0,0,0,136,137,1,0,0,0,137,5,1,0,0,0,138,136,1,0,0,
        0,139,140,7,2,0,0,140,7,1,0,0,0,21,11,17,23,29,32,37,44,51,58,67,
        75,82,87,93,100,108,115,123,130,134,136
    ]

class ExprParser ( Parser ):

    grammarFileName = "Expr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'='", "'-'", "'**'", "'*'", "'/'", "'('", 
                     "')'", "'+'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "PLUS", "ID", "INT", "WS" ]

    RULE_start_ = 0
    RULE_assn = 1
    RULE_expr = 2
    RULE_atom = 3

    ruleNames =  [ "start_", "assn", "expr", "atom" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    PLUS=8
    ID=9
    INT=10
    WS=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class Start_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(ExprParser.WS)
            else:
                return self.getToken(ExprParser.WS, i)

        def assn(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.AssnContext)
            else:
                return self.getTypedRuleContext(ExprParser.AssnContext,i)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprParser.ExprContext,i)


        def getRuleIndex(self):
            return ExprParser.RULE_start_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart_" ):
                listener.enterStart_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart_" ):
                listener.exitStart_(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart_" ):
                return visitor.visitStart_(self)
            else:
                return visitor.visitChildren(self)




    def start_(self):

        localctx = ExprParser.Start_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start_)
        self._la = 0 # Token type
        try:
            self.state = 32
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 11
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 8
                        self.match(ExprParser.WS) 
                    self.state = 13
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

                self.state = 17
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==9 or _la==11:
                    self.state = 14
                    self.assn()
                    self.state = 19
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 23
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11:
                    self.state = 20
                    self.match(ExprParser.WS)
                    self.state = 25
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 29
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 1860) != 0):
                    self.state = 26
                    self.expr(0)
                    self.state = 31
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssnContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(ExprParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(ExprParser.ExprContext,0)


        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(ExprParser.WS)
            else:
                return self.getToken(ExprParser.WS, i)

        def getRuleIndex(self):
            return ExprParser.RULE_assn

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssn" ):
                listener.enterAssn(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssn" ):
                listener.exitAssn(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssn" ):
                return visitor.visitAssn(self)
            else:
                return visitor.visitChildren(self)




    def assn(self):

        localctx = ExprParser.AssnContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_assn)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 37
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 34
                self.match(ExprParser.WS)
                self.state = 39
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 40
            self.match(ExprParser.ID)
            self.state = 44
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 41
                self.match(ExprParser.WS)
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 47
            self.match(ExprParser.T__0)
            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==11:
                self.state = 48
                self.match(ExprParser.WS)
                self.state = 53
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 54
            self.expr(0)
            self.state = 58
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 55
                    self.match(ExprParser.WS) 
                self.state = 60
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(ExprParser.AtomContext,0)


        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprParser.ExprContext,i)


        def PLUS(self):
            return self.getToken(ExprParser.PLUS, 0)

        def WS(self, i:int=None):
            if i is None:
                return self.getTokens(ExprParser.WS)
            else:
                return self.getToken(ExprParser.WS, i)

        def getRuleIndex(self):
            return ExprParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9, 10]:
                self.state = 62
                self.atom()
                pass
            elif token in [2, 8]:
                self.state = 63
                _la = self._input.LA(1)
                if not(_la==2 or _la==8):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 67
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11:
                    self.state = 64
                    self.match(ExprParser.WS)
                    self.state = 69
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 70
                self.expr(5)
                pass
            elif token in [6]:
                self.state = 71
                self.match(ExprParser.T__5)
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11:
                    self.state = 72
                    self.match(ExprParser.WS)
                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 78
                self.expr(0)
                self.state = 82
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==11:
                    self.state = 79
                    self.match(ExprParser.WS)
                    self.state = 84
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 85
                self.match(ExprParser.T__6)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 136
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,20,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 134
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
                    if la_ == 1:
                        localctx = ExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 89
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 93
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 90
                            self.match(ExprParser.WS)
                            self.state = 95
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 96
                        self.match(ExprParser.T__2)
                        self.state = 100
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 97
                            self.match(ExprParser.WS)
                            self.state = 102
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 103
                        self.expr(5)
                        pass

                    elif la_ == 2:
                        localctx = ExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 104
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 108
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 105
                            self.match(ExprParser.WS)
                            self.state = 110
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 111
                        _la = self._input.LA(1)
                        if not(_la==4 or _la==5):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 115
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 112
                            self.match(ExprParser.WS)
                            self.state = 117
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 118
                        self.expr(4)
                        pass

                    elif la_ == 3:
                        localctx = ExprParser.ExprContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 119
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 123
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 120
                            self.match(ExprParser.WS)
                            self.state = 125
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 126
                        _la = self._input.LA(1)
                        if not(_la==2 or _la==8):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 130
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        while _la==11:
                            self.state = 127
                            self.match(ExprParser.WS)
                            self.state = 132
                            self._errHandler.sync(self)
                            _la = self._input.LA(1)

                        self.state = 133
                        self.expr(3)
                        pass

             
                self.state = 138
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(ExprParser.INT, 0)

        def ID(self):
            return self.getToken(ExprParser.ID, 0)

        def getRuleIndex(self):
            return ExprParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = ExprParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_atom)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            _la = self._input.LA(1)
            if not(_la==9 or _la==10):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         




