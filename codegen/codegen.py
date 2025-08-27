#!/usr/bin/env python3
#

''' Codegen '''

#///////////////////////////////////////////////////////////////////////////
#//
#// Code generator for FASM output
#//

prolstr = '''\
'''

epilstr = '''
   \nEND_CODE:\n    ;End of program\n\n
'''

if __name__ == "__main__":
    #print ("This module was not meant to operate as main.")
    print(prolstr)
    print(epilstr)


# EOF
