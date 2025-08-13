''' Argument class globals. (For both Lexer and Parser) '''

import getopt, sys, os.path

class Lpg():

    ''' Program control flags and arguments. Vars with the letters
        "opt_" for inclusion in the comline interface.
        I wanted to modernize it, (argparse) but this is closer
        to 'C' for porting.
    '''

    def __init__(self, optlist = (), argv = ()):

        self.options = ""
        self.loptions = []
        self.helpdict = {}

        self.prestr  = "Program Help"
        self.poststr = "End Help"
        self.pad = 32                   # How far to padd comment

        # May add options here or in the command invocation
        # Adding it here allows a template like operation

        self.opt_quiet = False
        self.opt_help = False;
        self.opt_outfile = ""
        self.opt_debug = 0;
        self.opt_Version = False;
        self.opt_verbose = False;
        self.opt_xshow_lexer = False;

        self.opt_workdir = "./tmp"

        # Add recurring options / template help
        self.helpdict["opt_help"]        = "Show help (this screen)"
        self.helpdict["opt_quiet"]       = "Set quiet, minimize output"
        self.helpdict["opt_verbose"]     = "Set verbosity"
        self.helpdict["opt_Version"]     = "Print Version number"
        self.helpdict["opt_debug"]       = "Debug level. Def=0 0=none 9=noisy"
        self.helpdict["opt_workdir"]     = "Directory for temp files. Def=./tmp"
        self.helpdict["opt_outfile"]     = "Name of output file"

        self.opt_xshow_lexer = False;

        # Options from user
        for aa in optlist:
            oo = "opt_" + aa[0]
            setattr(self, oo, aa[1])
            self.helpdict[oo] = aa[2]

        #for aa in dir(self):
        #    if aa[:4] != "opt_":
        #        continue
        #    aaa = getattr(self, aa)
        #    #print(aa, "=", aaa)

        #print("helpdict", self.helpdict)
        self._auto_opt()
        if argv:
            self.parse(argv)

    def _xint(self, strx, defx = 0):
        ''' Convert to integer without fault.
                Return defx if it is an invalid integer. '''
        ret = defx
        try:
            ret = int(strx)
        except ValueError:      pass
        except: print(sys.exc_info())
        return ret

    def warnif(self, aa):
        #print("warnif adding:", aa)
        for bb in self.options:
            if bb == aa[4]:
                print("Warning: already has option", "'" + bb + "'", "=>", aa)

    def _auto_opt(self):

        for aa in dir(self):
            if aa[:4] != "opt_":
                continue
            bb = getattr(self, aa)
            #print("vars:", "--" + aa[4:].lower(), "=", bb)

            if isinstance(bb, type([]) ):
                self.warnif(aa)
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            elif isinstance(bb, str):
                self.warnif(aa)
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            elif isinstance(bb, bool):
                self.warnif(aa)
                self.options += aa[4]
            elif isinstance(bb, int):
                self.warnif(aa)
                self.options += aa[4] + ":"
                self.loptions.append(aa[4:].lower() + "=")
            else:
                pass
                print("Unkown type", type(aa))

        #print("options:", self.options)
        #print("loptions:", self.loptions)
        #self.printme()

    def printme(self):
        for aa in dir(self):
            if aa[:4] != "opt_":
                continue
            bb = self.helpdict.get(aa)
            print(aa, "=", "'" + str(getattr(self, aa)) + "'", "=>", bb)
        print()

    def helpstr(self):

        #print("dict", self.helpdict)
        strx = ""
        for aa in dir(self):
            if aa[:4] != "opt_":
                continue
            bb = "" ;
            #print("help:", "'" + cc + "'")
            try:
                bb = self.helpdict[aa]
                #print("help str:", bb)
            except KeyError:
                pass
            except:
                #print("err helpstr", sys.exc_info())
                pass
            head = "        -" + str(aa[4]) + "  --" + str(aa[4:])
            strx += head + " " * (self.pad - len(head)) + str(bb) + "\n"
        return strx

    def parse(self, argx):

        self.myname = os.path.basename(argx[0])
        self.setpre() ; self.setpost()
        try:
            opts, self.args = getopt.gnu_getopt(argx[1:], self.options, self.loptions)
        except getopt.GetoptError as err:
            print ("Invalid option(s) on command line:", err)
            sys.exit(1)
        #print("opts =", opts)

        for aa in opts:
            # Search for existing option vars
            for aaa in dir(self):
                if aaa[:4] != "opt_":
                    continue
                if aaa[4] == aa[0][1] or aaa[4:].lower() == aa[0][2:]:
                    attr = getattr(self, aaa)
                    #print("deal", aaa, "=", attr,  aa[1], type(attr))
                    if type(attr) == type([]):
                        getattr(self, aaa).append(aa[1])
                    elif type(attr) == type(True):
                        setattr(self, aaa, True)
                    elif type(attr) == type(0):
                        setattr(self, aaa, self._xint(aa[1]))
                    else:
                        setattr(self, aaa, aa[1])
    def help(self):
        print(self.prestr)
        print(self.helpstr(), end = "")
        print(self.poststr)

    def setpre(self, strx = None):
        if strx:
            self.prestr = strx
        else:
            self.prestr = "PCOMP parallel compiler.\n"
            self.prestr += "Usage: " + self.myname + \
                            " [options] filename [ filename ] ... \n"
            self.prestr += "Available options:"

    def setpost(self, strx = None):
        if strx:
            self.poststr = strx
        else:
            self.poststr  = "Option values are identical for short form and long form.\n"
            self.poststr += "Def stands for 'default' value."

def test_xint():

    lpg = Lpg()

    assert 0 == lpg._xint(0);
    assert 1 == lpg._xint(1);
    assert 0 == lpg._xint("a");
    assert 1 == lpg._xint("b", 1);

# EOF












