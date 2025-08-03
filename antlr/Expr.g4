grammar Expr;

/*    : expr ( WS* expr *) (EOF | WS*) */

start_
    : WS* assn *
    | WS* expr *
    ;
assn
    : WS* ID WS* '=' WS* expr WS*
    ;

expr
    :  atom
    |  ('+' | '-')   WS* expr
    |  expr WS* '**'  WS* expr
    |  expr WS* ('*' | '/')  WS* expr
    |  expr WS* ('+' | '-') WS* expr
    |  '('  WS* expr  WS* ')'
    ;

atom : INT | ID ;

PLUS : '+' ;
ID  : [a-zA-Z_]+  ;
/* ID2  : [a-zA-Z_][a-zA-Z0-9_]*  ; */
INT : [0-9]+ ;
WS  : [ \t\n\r]+ ; /*-> skip ; */
