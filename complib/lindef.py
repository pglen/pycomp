#!/usr/bin/env python

''' Definitions for the linear parser

    We initialize parser variables in the context of the parser module.

      The parser will look up if current state in the list of parser states.
    If there is a match, the tokens are compared.
        If the tokens match, the new parser state is set to (new)state, and the
        specified parser (UP) function is executed.
    When the parser is popping from the state stack, the specified (DOWN)
    function is executed.

      This parser has limited need for backtracking, as the grammar has a
    sentence based construction. The termination of the sentence is either
    a new line, closing double parenthesis, closing bracket or a semi colon.

    Examples:
        u32 : varname = 0
        varname = 2 *( 3 + 2 )
        printf(("hello"))
        func callme((varname)) { }

       The parser will ignore white space, except where it recognizes a new line
    as a sentence (statement) terminator. Tab is skipped / ignored,
    new line and ';' is interpreted as a sequence terminator,

    See grammar spec for more details.
'''

from   complib.utils import *
from   complib.linfunc  import *
import complib.lexdef  as lexdef
import complib.linfunc  as linfunc

def defpvg(xpvg):
    global pvg ; pvg = xpvg

PUSH=True
NOPUSH=False
NOCALL=False

class Stamp:

    ''' The class that holds the token descriptions for the parser '''

    def __init__(self, statex, tokenx, nstatex, dncall, upcall, pushx, pushy,
                                groupx = False, flagsx = False):
        # Extend to array if a number is passed
        if type(statex) == type(0):
            self.state = (statex,)
            #print("type cast", self.state)
        else:
            self.state  = statex
        # Extend to array if a number was passed
        if type(tokenx) == type(""):
            self.tokens  = (tokenx,)
            #print("token type cast", self.token)
        else:
            self.tokens  = tokenx

        self.nstate  = nstatex ;  self.push   = pushx
        self.dncall  = dncall  ;  self.upcall = upcall
        self.group   = groupx  ;  self.flags  = flagsx
        self.prepush = pushy

    def dump(self):

        states =  ""
        for aa in self.state:
            states += ST.get(aa) + " "
        strx  =  "[ " + states + " "
        tokens = ""
        for aa in self.tokens:
            tokens += aa + " "
        strx +=  pp(tokens) + " "
        strx +=  ST.get(self.nstate) + " ]"
        return strx

    def __str__(self):

        states =  ""
        for aa in self.state:
            sss = ST.get(aa)
            if states: sss = " " + sss
            states += sss

        if self.upcall:
            fnameU = str(self.upcall.__name__)
        else:
            fnameU = "NoUPFunc"
        if self.dncall:
            fnameD = str(self.dncall.__name__)
        else:
            fnameD = "NoDNFunc"

        ttt = stringify(self.tokens)
        strx = "cState: " + pp(states) + " tok: "  + pp(ttt) \
                + " nState: " + ST.get(self.nstate) + " " + fnameD \
                + " " + fnameU + " " + str(self.push) + " " + str(self.prepush)
        return strx

# List of identities for declaration
IDEN = ("ident", "num", "num2", "str", "arr", "float", "dbl",  "dbl2", )
NUME = ("ident", "num", "num2",)

# List of identities for number declaration
FLOAT   = "float", "double", "quad",

# Changed to auto add new state (note: no dup checking)
ST = Xenum()
def C(vvv):
    return ST.val(vvv)

# def Compund states for matching multiple states
STBASE =  ( C("STATEINI"), C("SFUNBODY"), C("SFUNARG"),
            C("SFUNENT"), C("SFUNLEA"), C("STIFBODY"), C("STELBODY"),
            C("STIF2"), C("STELIF2"), C("STLOBODY"), C("SLOENT"),
            C("SLOLEA"),
        )

# Where parentheses phases are valid
PARENSTATE =  ( C("STARITH"), C("SFASSN"), C("SFADD"),
                C("SFSUB"), C("SFMUL"), C("STIF") )

# Parse tables consist of:
#       a.) Parser state or parse states
#       b.) Token definition or tokens definitions
#       c.) New parser state to change to
#       e.) Function to call on up (set) state
#       f.) Function to call on down (pop) state
#       g.) Push flag at the end  (after set state)
#       h.) Push flag at the beginning (before set state)
#
# To create a new (custom) rule, just add new tokens / states in
#   the definition section. the "D*" declarations are extracted subsections.
#
# The entries to be matched agains the parse array.
# state(s)  token(s)  newState  downFunction  upFunction  pushFlag pre-pushFlag
# -------   -------   --------  ------------- ----------- -------- ------------

Dloop = ( \
    Stamp(STBASE,       "loop",     C("STLOOP"),    NOCALL,  loop.start, PUSH, NOPUSH),
    Stamp(C("STLOOP"),   "{",       C("STLOBODY"),  NOCALL,  NOCALL, PUSH, NOPUSH),

    Stamp(C("STLOBODY"), "enter",   C("STLOOP2"),   NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STLOOP2"), "{",        C("SLOENT"),    NOCALL,  loop.enter, PUSH, NOPUSH),
    Stamp(C("SLOENT"),  "}",        C("STPOP"),     loop.enter_end, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STLOBODY"), "leave",   C("STLOOP3"),   NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STLOOP3"), "{",        C("SLOLEA"),    NOCALL,  loop.leave, PUSH, NOPUSH),
    Stamp(C("SLOLEA"),  "}",        C("STPOP"),     loop.leave_end, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STLOBODY"), "break",   C("STLOBODY"),  NOCALL,  loop.breakx, NOPUSH, NOPUSH),
    Stamp(C("STLOBODY"), "}",       C("STPOP2"),    loop.end,  NOCALL, NOPUSH, NOPUSH),
)

Dif = ( \
    Stamp(STBASE,       "if",       C("STIF"),     NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STIF"),    "((",       C("STIF2"),    NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STIF2"),   "))",       C("STPOP"),    misc.ifx,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STIF"),    "{",        C("STIFBODY"), NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STIFBODY"), "break",   C("STIGN"),    NOCALL,  loop.breakx, NOPUSH, NOPUSH),
    Stamp(C("STIFBODY"), "}",       C("STPOP"),    misc.if_end,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STIFBODY"), "}}",      C("STPOP2"),   misc.if_end,  NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STIF"),     "elif",    C("STELIF"),   NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STELIF"),    "((",     C("STELIF2"),  NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STELIF2"),   "))",     C("STPOP"),    misc.elifx,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STELIF"),    "{",      C("STELIFBD"), NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STELIFBD"),  "break",  C("STIGN"),    NOCALL,  loop.breakx, NOPUSH, NOPUSH),
    Stamp(C("STELIFBD"),  "}",      C("STPOP"),    misc.elifx_end,  NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STIF"),      "else",   C("STELSE"),   NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STELSE"),    "{",      C("STELBODY"), NOCALL,  NOCALL, PUSH, NOPUSH),
    Stamp(C("STELBODY"),  "break",  C("STIGN"),    NOCALL,  loop.breakx, NOPUSH, NOPUSH),
    Stamp(C("STELBODY"),  "}",      C("STPOP2"),   misc.if_body_end,  NOCALL, NOPUSH, NOPUSH),
)

Dfuncx = ( \
    # Function Declaration
    Stamp(C("STATEANY"), "func",    C("STFUNC2"), NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STFUNC2"),  "ident",   C("STFUNC"),  NOCALL,  funcs.start, PUSH, NOPUSH),
    Stamp(C("STFUNC"),   "((",      C("SFUNARG"), NOCALL,  funcs.args_start, PUSH, NOPUSH),

    Stamp(C("SFUNARG"),  "))",      C("STPOP"),    funcs.args_end, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STARITH"),  "))",      C("STPOP"),    funcs.args_end, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STFUNC"),   "{",       C("SFUNBODY"),  NOCALL,  funcs.startbody, PUSH, NOPUSH),
    Stamp(C("SFUNBODY"), "}",       C("STPOP2"),    funcs.endbody, NOCALL,   NOPUSH, NOPUSH),

    Stamp(C("SFUNBODY"), "enter",   C("SFUNENT2"),  NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("SFUNENT2"), "{",       C("SFUNENT"),   NOCALL,  funcs.enter, PUSH, NOPUSH),
    Stamp(C("SFUNENT"),  "}",       C("STPOP"),     funcs.enter_end, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("SFUNBODY"), "leave",   C("SFUNLEA2"), NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("SFUNLEA2"), "{",       C("SFUNLEA"),  NOCALL,  funcs.leave, PUSH, NOPUSH),
    Stamp(C("SFUNLEA"),  "}",       C("STPOP"),    funcs.leave_end, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("SFUNBODY"), "return",  C("SFRET"),    NOCALL,  funcs.ret_start, PUSH, NOPUSH),
    Stamp(C("SFRET"),    "ident",   C("STARITH"),  NOCALL,  funcs.ret_id, NOPUSH, NOPUSH),
    Stamp(C("SFRET"),    "num",     C("STARITH"),  NOCALL,  funcs.ret_id, NOPUSH, NOPUSH),
    #Stamp(C("SFRET"),    ";",       C("STPOP"),    funcs.ret_end, NOCALL, NOPUSH, NOPUSH),

)

Drassn  = (
    # Right side assignment
    #Stamp(C("STARITH"),  "=>",     C("STRASSN3"),  NOCALL,  NOCALL, NOPUSH, NOPUSH),
    #Stamp(C("STRASSN3"), "num",    C("STRASSN4"),  NOCALL,  assn.rassn, NOPUSH, NOPUSH),
    #Stamp(C("STRASSN3"), "num2",   C("STRASSN4"),  NOCALL,  assn.rassn, NOPUSH, NOPUSH),
    #Stamp(C("STRASSN3"), "ident",  C("STRASSN4"),  NOCALL,  assn.rassn, NOPUSH, NOPUSH),
    #Stamp(C("STRASSN4"),  ";",     C("STPOP"),     NOCALL,  assn.rassn_stop, NOPUSH, NOPUSH),
    #Stamp(C("STRASSN4"),  "nl",    C("STPOP"),     NOCALL,  assn.rassn_stop, NOPUSH, NOPUSH),
    )

Dfcall  = (
    # Function call
    Stamp(C("STARITH"),   "((",     C("CFUNC3"),  NOCALL, fcall.start, NOPUSH, NOPUSH),
    Stamp(STBASE,         "((",     C("CFUNC3"),  NOCALL, fcall.start, NOPUSH, NOPUSH),
    Stamp(C("CFUNC3"),    "num",    C("CFUNC4"),  NOCALL, fcall.val, NOPUSH, NOPUSH),
    Stamp(C("CFUNC3"),    "ident",  C("CFUNC4"),  NOCALL, fcall.val, NOPUSH, NOPUSH),
    Stamp(C("CFUNC3"),    "str",    C("CFUNC4"),  NOCALL, fcall.val, NOPUSH, NOPUSH),

    Stamp(C("CFUNC3"),    "))",     C("STPOP"), fcall.end, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("CFUNC4"),    "))",     C("STPOP"), fcall.end, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("CFUNC4"),    ",",      C("CFUNC3"), NOCALL, fcall.comma, NOPUSH, NOPUSH),
    Stamp(C("CFUNC4"),    "nl",     C("STPOP"),  fcall.end, NOCALL,  NOPUSH, NOPUSH),
    Stamp(C("CFUNC4"),    ";",      C("STPOP"),  fcall.end, NOCALL,  NOPUSH, NOPUSH),
    )

Dcond = (
    Stamp(C("STARITH"), "==",        C("SFEQEQ"),   NOCALL,  arith.eqeq_start, NOPUSH, NOPUSH),
    Stamp(C("SFEQEQ"),  NUME,        C("STARITH"),  NOCALL,  arith.eqeq, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "or",        C("SFOR"),   NOCALL,  arith.orx_start, NOPUSH, NOPUSH),
    Stamp(C("SFOR"),  NUME,          C("STARITH"),NOCALL,  arith.orx, NOPUSH, NOPUSH),
)

Darith = (
    # Arithmetics (+ - * / sqr assn)
    Stamp(C("STARITH"), "=",        C("SFASSN"),   NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFASSN"),  NUME,       C("STARITH"),  NOCALL,  arith.assnexpr, NOPUSH, NOPUSH),
    Stamp(C("SFASSN"),  "str",      C("STARITH"),  NOCALL,  arith.assnexpr, NOPUSH, NOPUSH),

    Stamp(PARENSTATE,   "(",        C("STIGN"),    NOCALL,   misc.parent, NOPUSH, NOPUSH),
    Stamp(PARENSTATE,   ")",        C("STIGN"),    NOCALL,   misc.parent, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "=>",       C("SFPUT"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFPUT"),   NUME,    C("STARITH"),  NOCALL,  arith.mulexpr, NOPUSH, NOPUSH),
    #Stamp(C("SFPUT"),   "num",      C("STARITH"),  NOCALL,  arith.mulexpr, NOPUSH, NOPUSH),
    #Stamp(C("SFPUT"),   "num2",      C("STARITH"), NOCALL,  arith.mulexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "expo",     C("SFSQR"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFSQR"),   NUME,    C("STARITH"),  NOCALL,  arith.expexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "*",        C("SFMUL"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFMUL"),   NUME,    C("STARITH"),  NOCALL,  arith.mulexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "+",        C("SFADD"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFADD"),   NUME,    C("STARITH"),  NOCALL,  arith.addexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "/",        C("SFDIV"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFDIV"),   NUME,    C("STARITH"),  NOCALL,  arith.divexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "%",        C("SFDIV"),    NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFDIV"),   NUME,    C("STARITH"),  NOCALL,  arith.divexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "-",        C("SFSUB"),     NOCALL, arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFSUB"),   NUME,    C("STARITH"),   NOCALL, arith.subexpr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "<<",       C("SFSHIFT"),  NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFSHIFT"), NUME,    C("STARITH"),  NOCALL,  arith.expr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), ">>",      C("SFRSHIFT"), NOCALL,  arith.arithop, NOPUSH, NOPUSH),
    Stamp(C("SFRSHIFT"),NUME,   C("STARITH"),  NOCALL,  arith.expr, NOPUSH, NOPUSH),

    Stamp(C("STARITH"), ",",       C("DECL3"),    NOCALL,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("STARITH"), ";",       C("STPOP"),    NOCALL,  arith.arith_stop, NOPUSH, NOPUSH),
    Stamp(C("STARITH"), "nl",      C("STPOP"),    NOCALL,  arith.arith_stop, NOPUSH, NOPUSH),
    )

Ddecl = (
    # Declarations
    Stamp(STBASE,   "decl",     C("DECL2"),   NOCALL,   decl.start,   NOPUSH, PUSH),
    Stamp(STBASE,   FLOAT,      C("DECL2"),   NOCALL,   decl.start,   NOPUSH, PUSH),
    Stamp(STBASE,   "arr",      C("DECLA"),   NOCALL,   adecl.astart, NOPUSH, PUSH),

    Stamp(C("DECL2"),   ":",     C("DECL3"),   NOCALL,   decl.col,    NOPUSH, NOPUSH),
    Stamp(C("DECL3"),   "ident", C("STARITH"), NOCALL,   decl.ident,  NOPUSH, NOPUSH),
    Stamp(C("STARITH"), ",",     C("DECL3"),   NOCALL,   decl.comma,  NOPUSH, NOPUSH),

    Stamp(C("STARITH"), "nl",    C("STPOP"),   decl.down, NOCALL,     NOPUSH, NOPUSH),
    Stamp(C("STARITH"), ";",     C("STPOP"),   decl.down, NOCALL,     NOPUSH, NOPUSH),

    # String operations
    Stamp(C("DECLA"),   ":",     C("DECLA2"),  NOCALL,   adecl.acol,   NOPUSH, NOPUSH),
    Stamp(C("DECLA2"),  "ident", C("STTARI"),  NOCALL,   adecl.aident, NOPUSH, NOPUSH),
    Stamp(C("STTARI"),  "=",     C("STTARI2"), NOCALL,   adecl.aeq,    NOPUSH, NOPUSH),
    Stamp(C("STTARI2"), "str",   C("STTARI3"), NOCALL,   adecl.astr,   NOPUSH, NOPUSH),

    Stamp(C("STTARI3"), ",",     C("DECLA2"),  NOCALL,   adecl.acomma, NOPUSH, NOPUSH),
    Stamp(C("STTARI3"), "+",     C("STTARI2"), NOCALL,   adecl.aadd,   NOPUSH, NOPUSH),
    Stamp(C("STTARI3"), "*",     C("STTARI4"), NOCALL,   adecl.amul,   NOPUSH, NOPUSH),
    Stamp(C("STTARI4"), "num",   C("STTARI3"), NOCALL,   adecl.anum,   NOPUSH, NOPUSH),

    Stamp(C("STTARI3"), ";",     C("STPOP"),   adecl.adown, NOCALL,    NOPUSH, NOPUSH),
    Stamp(C("STTARI3"), "nl",    C("STPOP"),   adecl.adown, NOCALL,    NOPUSH, NOPUSH),
)

# ------------------------------------------------------------------------
# Main stamps definition

stamps =  (
    Stamp(STBASE,        "ident",   C("STARITH"),  NOCALL,  arith.arithstart, PUSH, NOPUSH),
    Stamp(C("STATEINI"), "extern",  C("EXTERN"),   NOCALL,  exter.extern, PUSH, NOPUSH),
    Stamp(C("EXTERN"),   "ident",   C("EXTERN2"),  NOCALL,  exter.extadd, NOPUSH, NOPUSH),
    Stamp(C("EXTERN"),   "str",     C("EXTERN2"),  NOCALL,  exter.extadd, NOPUSH, NOPUSH),
    Stamp(C("EXTERN2"),  ",",       C("EXTERN"),   NOCALL,  exter.extcomma, NOPUSH, NOPUSH),
    Stamp(C("EXTERN2"),  ";",       C("STPOP"),    exter.exdn,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("EXTERN2"),  "nl",      C("STPOP"),    exter.exdn,  NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STATEINI"), "global",  C("GLOBAL"),   NOCALL,  exter.glob, PUSH, NOPUSH),
    Stamp(C("GLOBAL"),   "ident",   C("GLOBAL2"),  NOCALL,  exter.globadd, NOPUSH, NOPUSH),
    Stamp(C("GLOBAL"),   "str",     C("GLOBAL2"),  NOCALL,  exter.globadd, NOPUSH, NOPUSH),
    Stamp(C("GLOBAL2"),  ",",       C("GLOBAL"),   NOCALL,  exter.globcomma, NOPUSH, NOPUSH),
    Stamp(C("GLOBAL2"),  ";",       C("STPOP"),    exter.gldn,  NOCALL, NOPUSH, NOPUSH),
    Stamp(C("GLOBAL2"),  "nl",      C("STPOP"),    exter.gldn,  NOCALL, NOPUSH, NOPUSH),

    Stamp(C("STATEINI"), "asm",     C("ASSEM"),    NOCALL,  exter.assem, PUSH, NOPUSH),

    Stamp(C("ASSEM"),   "{",        C("ASSEM3"),   NOCALL,  exter.asm_start, PUSH, NOPUSH),
    # These are the tokens that one can include in asm.
    # If a character is not allowed, embed it in a string.
    # If you want to put a string in assembler, use string in string like: "'hello'"
    Stamp(C("ASSEM3"),  "ident",    C("ASSEM3"),   NOCALL, exter.asm_item, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  "num",      C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  "str",      C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  ",",        C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  ";",        C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  ":",        C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  "[",        C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),
    Stamp(C("ASSEM3"),  "]",        C("ASSEM3"),   NOCALL, exter.asm_item, NOCALL, NOPUSH, NOPUSH),

    Stamp(C("ASSEM3"),  "}",        C("STPOP2"),   exter.asm_end, NOCALL, NOPUSH, NOPUSH),

    #Stamp(C("ASSEM2"),  "nl",      C("STPOP"),    exter.asmdn,  NOCALL, NOPUSH, NOPUSH),

    # Include sub systems
    *Ddecl,    *Darith,      *Dfcall,
    *Dif,      *Dfuncx,      *Drassn,
    *Dloop,    *Dcond,

    # This will ignore comments
    Stamp(C("STATEANY"), "comm2",   C("STIGN"),   NOCALL,  misc.comment, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "comm2d",  C("STIGN"),   NOCALL,  misc.dcomment, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "comm3",   C("STIGN"),   NOCALL,  misc.comment, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "comm3d",  C("STIGN"),   NOCALL,  misc.dcomment2, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "comm4",   C("STIGN"),   NOCALL,  misc.comment, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "comm4d",  C("STIGN"),   NOCALL,  misc.dcomment3, NOPUSH, NOPUSH),

    # This will ignore white spaces (fall through)
    Stamp(C("STATEANY"), "tab",     C("STIGN"),   NOCALL,  misc.tab, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "sp",      C("STIGN"),   NOCALL,  misc.space, NOPUSH, NOPUSH),
    Stamp(C("STATEANY"), "nl",      C("STIGN"),   NOCALL,  misc.nl, NOPUSH, NOPUSH),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF