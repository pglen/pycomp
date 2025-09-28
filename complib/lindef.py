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

class   Xenum():

    ''' Simple autofill enum to use in parser '''

    def __init__(self, *val):
        self.arr = [] ; self.narr = {}
        self.add(*val)

    def add(self, *val):
        for aa in val:
            self.narr[aa] = len(self.arr)
            self.arr.append(aa)

    def dump(self):
        strx = ""
        for cnt, aa in enumerate(self.arr):
            #print(cnt, aa)
            strx += str(cnt) + " = " + str(aa) + "\n"
        return strx

    def get(self, cnt):
        return self.arr[cnt]

    def val(self, name):
        try:
            ret = self.narr[name]
        except:
            if 0: #pvg.opt_verbose:
                print("Warn: adding:", name)
            self.add(name)
            ret = self.narr[name]
        return ret

def test_xenum():

    ''' Test Xenum class '''
    eee = Xenum("no", "yes",)
    eee.add( "maybe")
    assert eee.get(0) == "no"
    assert eee.get(1) == "yes"
    assert eee.val("no")  == 0
    assert eee.val("yes") == 1
    # Autogen
    assert eee.val("none") == 3

class Stamp:

    ''' The class that holds the token descriptions for the parser '''

    def __init__(self, statex, tokenx, nstatex, dncall, upcall, pushx, pushy,
                                groupx = None, flagsx = None):
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

        self.nstate = nstatex ;    self.push   = pushx
        self.prepush = pushy
        self.dncall = dncall  ;    self.upcall = upcall
        self.group  = groupx  ;    self.flags  = flagsx

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
            states += ST.get(aa) + " "
        if self.upcall:
            fnameU = str(self.upcall.__name__)
        else:
            fnameU = "NoUPFunc"
        if self.dncall:
            fnameD = str(self.dncall.__name__)
        else:
            fnameD = "NoDNFunc"

        strx = "cState: " + states + " "  + pp(str(self.tokens)) \
                + " nState: " + ST.get(self.nstate) + " " + fnameD \
                + " " + fnameU + " " + str(self.push) + " " + str(self.prepush)
        return strx

# List of identities for declaration
IDEN = ("ident", "num", "num2", "str", "arr", "float", "dbl",  "dbl2", )

# Changed to auto add new state (note: no dup checking)
ST = Xenum()
def C(vvv):
    return ST.val(vvv)

# Compund states for matching multiple states
STBASE =  ( C("STATEINI"), C("SFUNBODY"), C("SFUNARG"),
            C("SFUNENT"), C("SFUNLEA") )

# Where parentheses phases are valid
PARENSTATE =  C("STARITH"), C("SFASSN"), C("SFADD"),  C("SFSUB"), C("SFMUL")

# Parse tables consist of:
#       a.) Parser state or states
#       b.) Token definition or tokens
#       c.) New parser state
#       e.) Parser function to call on up state
#       f.) Parser function to call on down state
#       g.) Push flag at the end  (after set state)
#       h.) Push flag at the beginning (before stet state)
#
# To create a custom rule, just add new tokens / states in
#   the definition section. the D* declarations are extracted subsections.

# The entries to be matched agains the parse array.
# state(s)  token(s)  newState  downFunction  upFunction  pushFlag pre-pushFlag
# -------   -------   --------  ------------- ----------- -------- ------------

Dfuncx = ( \
    # Function Declaration
    Stamp(C("STATEANY"),  "func",   C("STFUNC"),    None,  None, False, False),
    Stamp(C("STFUNC"),    "ident",  C("STFUNC2"),   None,  funcs.start, False, False),
    Stamp(C("STFUNC2"),   "((",     C("SFUNARG"),   None,  funcs.args_start, True, False),

    Stamp(C("SFUNARG"),  "))",      C("STPOP"),     funcs.args_end, None, False, False),
    Stamp(C("SFUNARG2"), "))",      C("STPOP"),     funcs.args_end, None, False, False),

    Stamp(C("SFUNARG"),  "{",      C("SFUNBODY"),   None,  funcs.startbody, True, False),
    Stamp(C("SFUNBODY"), "}",      C("STATEINI"),   None,  funcs.endbody, False, False),

    Stamp(C("SFUNBODY"), "enter",  C("SFUNENT2"),   None,  None, False, True),
    Stamp(C("SFUNENT2"), "{",      C("SFUNENT"),    None,  funcs.enter, False, False),
    Stamp(C("SFUNENT"),  "}",      C("STPOP"),      funcs.enter_end, None, False, False),

    Stamp(C("SFUNBODY"), "leave",   C("SFUNLEA2"),  None,  None, False, True),
    Stamp(C("SFUNLEA2"), "{",       C("SFUNLEA"),   None,  funcs.leave, False, False),
    Stamp(C("SFUNLEA"),  "}",       C("STPOP"),     funcs.leave_end, None, False, False),

    Stamp(C("SFUNBODY"), "return", C("SFASSN"),     None,  funcs.ret, False, False),

    #Stamp(C("SFUNCRET"), "nl",     C("SFUNBODY"),   None,  None, False, False),
    #Stamp(C("SFUNCRET"), ";",      C("SFUNBODY"),   None,  None, False, False),
    #Stamp(C("SFUNCRET"), "num",    C("SFUNBODY"),   None,  None, False, False),
    #Stamp(C("SFUNCRET"), "ident",  C("SFUNBODY"),   None,  None, False, False),

)

Drassn  = (
    # Right side assignment
    #Stamp(C("STARITH"),  "=>",     C("STRASSN3"),  None,  None, False, False),
    #Stamp(C("STRASSN3"), "num",    C("STRASSN4"),  None,  assn.rassn, False, False),
    #Stamp(C("STRASSN3"), "num2",   C("STRASSN4"),  None,  assn.rassn, False, False),
    #Stamp(C("STRASSN3"), "ident",  C("STRASSN4"),  None,  assn.rassn, False, False),
    #Stamp(C("STRASSN4"),  ";",     C("STPOP"),     None,  assn.rassn_stop, False, False),
    #Stamp(C("STRASSN4"),  "nl",    C("STPOP"),     None,  assn.rassn_stop, False, False),
    )

Dfcall  = (
    # Function call
    Stamp(C("STARITH"),   "((",     C("CFUNC3"),  None, fcall.start, False, False),
    Stamp(STBASE,         "((",     C("CFUNC3"),  None, fcall.start, False, False),
    Stamp(C("CFUNC3"),    "num",    C("CFUNC4"),  None, fcall.val, False, False),
    Stamp(C("CFUNC3"),    "ident",  C("CFUNC4"),  None, fcall.val, False, False),
    Stamp(C("CFUNC3"),    "str",    C("CFUNC4"),  None, fcall.val, False, False),

    Stamp(C("CFUNC3"),    "))",      C("STPOP"), fcall.end, None, False, False),
    Stamp(C("CFUNC4"),    "))",      C("STPOP"), fcall.end, None, False, False),
    Stamp(C("CFUNC4"),    ",",      C("CFUNC3"), None, fcall.comma, False, False),
    Stamp(C("CFUNC4"),    "nl",     C("STPOP"),  fcall.end, None,  False, False),
    Stamp(C("CFUNC4"),    ";",      C("STPOP"),  fcall.end, None,  False, False),
    )

Dtest = (
    # Assignments / Start of arithmetic
)

Darith = (
    # Arithmetics (+ - * / sqr assn)
    #Stamp(C("c"), "=",        C("SFASSN"),    None,  arith.arithop, False, False),
    Stamp(C("SFASSN"),  "ident",    C("STARITH"),  None,  arith.assnexpr, False, False),
    Stamp(C("SFASSN"),  "num",      C("STARITH"),  None,  arith.assnexpr, False, False),
    Stamp(C("SFASSN"),  "num2",     C("STARITH"),  None,  arith.assnexpr, False, False),
    Stamp(C("SFASSN"),  "str",      C("STARITH"),  None,  arith.assnexpr, False, False),

    Stamp(PARENSTATE,   "(",        C("STIGN"),    None,   misc.parent, False, False),
    Stamp(PARENSTATE,   ")",        C("STIGN"),    None,   misc.parent, False, False),

    Stamp(C("STARITH"), "=",        C("SFASSN"),   None,  arith.arithop, False, False),

    Stamp(C("STARITH"), "=>",       C("SFPUT"),    None,  arith.arithop, False, False),
    Stamp(C("SFPUT"),   "ident",    C("STARITH"),  None,  arith.mulexpr, False, False),
    Stamp(C("SFPUT"),   "num",      C("STARITH"),  None,  arith.mulexpr, False, False),
    Stamp(C("SFPUT"),   "num2",      C("STARITH"),  None,  arith.mulexpr, False, False),

    Stamp(C("STARITH"), "expo",     C("SFSQR"),    None,  arith.arithop, False, False),
    Stamp(C("SFSQR"),   "ident",    C("STARITH"),  None,  arith.expexpr, False, False),
    Stamp(C("SFSQR"),   "num",      C("STARITH"),  None,  arith.expexpr, False, False),

    Stamp(C("STARITH"), "*",        C("SFMUL"),    None,  arith.arithop, False, False),
    Stamp(C("SFMUL"),   "ident",    C("STARITH"),  None,  arith.mulexpr, False, False),
    Stamp(C("SFMUL"),   "num",      C("STARITH"),  None,  arith.mulexpr, False, False),
    Stamp(C("SFMUL"),   "num2",     C("STARITH"),  None,  arith.mulexpr, False, False),

    Stamp(C("STARITH"), "+",        C("SFADD"),    None,  arith.arithop, False, False),
    Stamp(C("SFADD"),   "ident",    C("STARITH"),  None,  arith.addexpr, False, False),
    Stamp(C("SFADD"),   "num",      C("STARITH"),  None,  arith.addexpr, False, False),
    Stamp(C("SFMUL"),   "num2",     C("STARITH"),  None,  arith.mulexpr, False, False),

    Stamp(C("STARITH"), "/",        C("SFDIV"),    None,  arith.arithop, False, False),
    Stamp(C("SFDIV"),   "ident",    C("STARITH"),  None,  arith.divexpr, False, False),
    Stamp(C("SFDIV"),   "num",      C("STARITH"),  None,  arith.divexpr, False, False),

    Stamp(C("STARITH"), "%",        C("SFDIV"),    None,  arith.arithop, False, False),
    Stamp(C("SFDIV"),   "ident",    C("STARITH"),  None,  arith.divexpr, False, False),
    Stamp(C("SFDIV"),   "num",      C("STARITH"),  None,  arith.divexpr, False, False),

    Stamp(C("STARITH"), "-",        C("SFSUB"),     None, arith.arithop, False, False),
    Stamp(C("SFSUB"),   "ident",    C("STARITH"),   None, arith.subexpr, False, False),
    Stamp(C("SFSUB"),   "num",      C("STARITH"),   None, arith.subexpr, False, False),

    Stamp(C("STARITH"), "<<",       C("SFSHIFT"),  None,  arith.arithop, False, False),
    Stamp(C("SFSHIFT"), "ident",    C("STARITH"),  None,  arith.expr, False, False),
    Stamp(C("SFSHIFT"), "num",      C("STARITH"),  None,  arith.expr, False, False),

    Stamp(C("STARITH"),  ">>",      C("SFRSHIFT"), None,  arith.arithop, False, False),
    Stamp(C("SFRSHIFT"), "ident",   C("STARITH"),  None,  arith.expr, False, False),
    Stamp(C("SFRSHIFT"), "num",     C("STARITH"),  None,  arith.expr, False, False),

    # Down state to:
    Stamp(PARENSTATE,   "))",      C("STPOP"),    misc.dbldwn, None, False, False),
    #Stamp(C("STARITH"), "}",       C("STPOP"),    None,  arith.arith_stop, False, False),

    Stamp(C("STARITH"), ";",       C("STPOP"),    None,  arith.arith_stop, False, False),
    #Stamp(C("STARITH"), "nl",     C("STPOP"),    None,  arith.arith_stop, False, False),
    )

FLOAT   = "float", "double", "quad",

Ddecl = (
    # Declarations
    Stamp(STBASE,   "decl",     C("DECL2"),   None,   decl.start,   False, True),
    Stamp(STBASE,   FLOAT,      C("DECL2"),   None,   decl.start,   False, True),
    Stamp(STBASE,   "arr",      C("DECLA"),   None,   adecl.astart, False, True),

    Stamp(C("DECL2"),   ":",     C("DECL3"),   None,   decl.col,    False, False),
    Stamp(C("DECL3"),   "ident", C("STARITH"), None,   decl.ident,  False, False),
    Stamp(C("STARITH"), ",",     C("DECL3"),   None,   decl.comma,  False, False),
    Stamp(C("STARITH"), "nl",    C("STPOP"),   decl.down, None,     False, False),
    Stamp(C("STARITH"), ";",     C("STPOP"),   decl.down, None,    False, False),

    # String operations
    Stamp(C("DECLA"),   ":",     C("DECLA2"),  None,   adecl.acol,   False, False),
    Stamp(C("DECLA2"),  "ident", C("STTARI"),  None,   adecl.aident, False, False),
    Stamp(C("STTARI"),  "=",     C("STTARI2"), None,   adecl.aeq,    False, False),
    Stamp(C("STTARI2"), "str",   C("STTARI3"), None,   adecl.astr,   False, False),

    Stamp(C("STTARI3"), ",",     C("DECLA2"),  None,   adecl.acomma, False, False),
    Stamp(C("STTARI3"), "+",     C("STTARI2"), None,   adecl.aadd,   False, False),
    Stamp(C("STTARI3"), "*",     C("STTARI4"), None,   adecl.amul,   False, False),
    Stamp(C("STTARI4"), "num",   C("STTARI3"), None,   adecl.anum,   False, False),

    Stamp(C("STTARI3"), ";",     C("STPOP"),   adecl.adown, None,    False, False),
    Stamp(C("STTARI3"), "nl",    C("STPOP"),   adecl.adown, None,    False, False),
)

# Main stamps definition

stamps =  (  \

    #Stamp(C("STATEINI"), "ident",   C("STARITH"),  None,  arith.arithstart, True, False),
    Stamp(STBASE,        "ident",   C("STARITH"),  None,  arith.arithstart, True, False),
    Stamp(C("STATEINI"), "extern",  C("EXTERN"),   None,  misc.extern, True, False),
    Stamp(C("EXTERN"),   "ident",   C("EXTERN2"),  None,  misc.extadd, False, False),
    Stamp(C("EXTERN"),   "str",     C("EXTERN2"),  None,  misc.extadd, False, False),
    Stamp(C("EXTERN2"),  ",",       C("EXTERN"),   None,  misc.extcomma, False, False),
    Stamp(C("EXTERN2"),  ";",       C("STPOP"),    misc.exdn,  None, False, False),
    Stamp(C("EXTERN2"),  "nl",      C("STPOP"),    misc.exdn,  None, False, False),

    # Include sub systems
    *Ddecl,
    *Darith,
    *Dfcall,
    *Dfuncx,
    *Drassn,

    # This will ignore comments
    Stamp(C("STATEANY"), "comm2",   C("STIGN"),   None,  misc.comment, False, False),
    Stamp(C("STATEANY"), "comm2d",  C("STIGN"),   None,  misc.dcomment, False, False),
    Stamp(C("STATEANY"), "comm3",   C("STIGN"),   None,  misc.comment, False, False),
    Stamp(C("STATEANY"), "comm3d",  C("STIGN"),   None,  misc.dcomment2, False, False),
    Stamp(C("STATEANY"), "comm4",   C("STIGN"),   None,  misc.comment, False, False),
    Stamp(C("STATEANY"), "comm4d",  C("STIGN"),   None,  misc.dcomment3, False, False),

    # This will ignore white spaces (fall through)
    Stamp(C("STATEANY"), "tab",     C("STIGN"),   None,  misc.tab, False, False),
    Stamp(C("STATEANY"), "sp",      C("STIGN"),   None,  misc.space, False, False),
    Stamp(C("STATEANY"), "nl",      C("STIGN"),   None,  misc.nl, False, False),
    )

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
