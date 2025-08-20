''' Argument class globals. (For both Lexer and Parser) '''

import getopt, sys, os.path

class Cntx:

    ''' Class for incremented variable '''

    def __init__(self, cnt = 0):
        self.cnt = cnt
    def __add__(self, what):
        self.cnt += what
        return self
    def __repr__(self):
        return self.cnt
    def __int__(self):
        return self.cnt
    def __str__(self):
        return str(self.cnt)

# Adding default options here allows a template like operation

builtins = ( \
    ("help",     False,  "Show help. (this screen)"),
    ("Help2",    False,  "Show advanced help. (placeholder for now)"),
    ("debug",    0,      "Debug level. Def=0 0=>none 9=>noisy."),
    ("Version",  False,  "Print version number and build date."),
    ("verbose",  Cntx(), "Set verbosity level."),
    )

class Lpg():

    ''' Program control flags and arguments. Vars with the letters
        "opt_" for inclusion in the comline interface.
        I wanted to modernize it, (argparse) but this is closer
        to 'C' for porting. Also features like multiple defines
        and incremeted flags are not readily available in the library.
    '''

    def __init__(self, optlist = (), argv = ()):

        self.options = ""
        self.loptions = []
        self.helpdict = {}

        self.prestr  = "Program Help"
        self.poststr = "End Help"
        self.pad = 32                   # How far to padd comment

        # Options from this file
        for aa in builtins:
            oo = "opt_" + aa[0]
            setattr(self, oo, aa[1])
            self.helpdict[oo] = aa[2]
        # Add options from the command invocation
        for aa in optlist:
            oo = "opt_" + aa[0]
            setattr(self, oo, aa[1])
            self.helpdict[oo] = aa[2]
        #print("help", dir(self))
        #print("helpdict", self.helpdict)
        self._auto_opt()
        if argv:
            self.parse(argv)
        #for aa in self.iter_vars():
        #    print(aa, end = " ")

    def _xint(self, strx, defx = 0):
        ''' Convert to integer without exception.
            Return defx if it is an invalid integer. '''
        ret = defx
        try:
            ret = int(strx)
        except ValueError: pass
        except: print(sys.exc_info())
        return ret

    def warnif(self, aa):
        for bb in self.options:
            if bb == aa[4]:
                print("Warning: already has option", "'" + bb + "'", "=>", aa)

    def iter_vars(self):
        for aa in dir(self):
            if aa[:4] != "opt_":
                continue
            yield aa

    def _auto_opt(self):
        for aa in self.iter_vars():
            bb = getattr(self, aa)
            #print("vars:", "--" + aa[4:].lower(), "=", bb)

            self.warnif(aa)

            # Put bool as first, as it is derived from integer
            if isinstance(bb, bool):
                #print("bool", aa)
                self.options += aa[4]
                self.loptions.append(aa[4:].lower())
            elif isinstance(bb, type([]) ):
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            elif isinstance(bb, str):
                #print("str", aa)
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            elif isinstance(bb, int):
                #print("int", aa)
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            elif isinstance(bb, Cntx ):
                #print("counter", aa)
                self.options += aa[4]
                self.loptions.append(aa[4:].lower())
            else:
                pass
                print("Err: Unkown type", type(aa))

        #print("options:", self.options)
        #print("loptions:", self.loptions)
        #self.printme()

    def printme(self):
        for aa in self.iter_vars():
            if aa[:4] != "opt_":
                continue
            bb = self.helpdict.get(aa)
            print(aa, "=", "'" + str(getattr(self, aa)) + "'", "=>", bb)
        print()

    def helpstr(self):

        #print("dict", self.helpdict)
        strx = ""
        for aa in self.iter_vars():
            bb = "" ;
            #print("help:", "'" + cc + "'")
            try:
                bb = self.helpdict[aa]
                #print("help str:", bb)
            except KeyError:
                pass
            except:
                print("err helpstr", sys.exc_info())
                pass

            arg = " val"
            attr = getattr(self, aa)
            if isinstance(attr, type(False)) or \
                    isinstance(attr, Cntx):
                #print("bool", aa)
                arg = "    "
            head = "    -" + str(aa[4]) + arg + "  --" + str(aa[4:]).lower() + arg
            strx += head + " " * (self.pad - len(head)) + str(bb) + "\n"
        return strx

    def parse(self, argx):

        self.myname = os.path.basename(argx[0])
        self.setpre() ; self.setpost()

        try:
            opts, self.args = getopt.gnu_getopt(argx[1:], self.options, self.loptions)
        except getopt.GetoptError as err:
            print("Invalid option(s) on command line:", err)
            print("Use:", self.myname, "-h option for help.")
            sys.exit(1)
        #print("opts =", opts)

        for aa in opts:
            # Search for existing option vars
            for aaa in self.iter_vars():
                if aaa[4] == aa[0][1] or aaa[4:].lower() == aa[0][2:]:
                    attr = getattr(self, aaa)
                    #print("deal", aaa, "=", attr,  aa[1], type(attr))
                    if isinstance(attr, Cntx):
                        attr += 1
                    elif isinstance(attr, type([]) ):
                        getattr(self, aaa).append(aa[1])
                    elif isinstance(attr, type(True) ):
                        setattr(self, aaa, True)
                    elif isinstance(attr, type(0) ):
                        setattr(self, aaa, self._xint(aa[1]))
                    else:
                        setattr(self, aaa, aa[1])
    def help(self):
        print(self.prestr)
        print(self.helpstr(), end = "")
        print(self.poststr)

    def Help(self):
        print("Advanced help placeholder.")
        print("Under construction.")

    def setpre(self, strx = None):
        if strx:
            self.prestr = strx

    def setpost(self, strx = None):
        if strx:
            self.poststr = strx

def test_xint():
    lpg = Lpg()
    assert 0 == lpg._xint(0);
    assert 1 == lpg._xint(1);
    assert 0 == lpg._xint("a");
    assert 1 == lpg._xint("b", 1);

def test_cnt():
    ccc = Cntx(1)
    assert ccc.cnt == 1
    ccc += 2
    assert ccc.cnt == 3

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")

# EOF
