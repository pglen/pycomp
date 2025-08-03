
ANTLR=antlr4

#.PHONY:  expr

all:
	@echo Targets: clean gen calc C expr

gen:
	$(ANTLR) -Dlanguage=Python3 MarkupLexer.g4
	$(ANTLR) -Dlanguage=Python3 MarkupParser.g4

calc:
	$(ANTLR) -Dlanguage=Python3 -atn -visitor -o tmp calc.g4

C:
	$(ANTLR) -Dlanguage=Python3 -atn -visitor -o tmp C.g4

expr: expr/ExprParser.py

expr/ExprParser.py: Expr.g4
	antlr4 -Dlanguage=Python3 -o expr -visitor Expr.g4

clean:
	rm -f *.h *.cpp *.java *.tokens *.interp
	rm -f *Lexer.py  *Parser*.py *Listener*.py

#git:
#	git add .
#	git commit -m auto
#	#git push
#
# EOF
