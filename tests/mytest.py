import os, string, random, sys

# Return a random string based upon length

allstr =  string.ascii_lowercase +  string.ascii_uppercase

def randstr(lenx):

    strx = ""
    for aa in range(lenx):
        ridx = random.randint(0, len(allstr)-1)
        rr = allstr[ridx]
        strx += str(rr)
    return strx

# ------------------------------------------------------------------------

test_dir = "test_data"

if not os.path.isdir(test_dir):
    os.mkdir(test_dir)

tmpfile = ""

#tmpfile = os.path.splitext(os.path.basename(__file__))[0]
#tmpfile = randstr(8)

# This one will get the last one
for mm in sys.modules:
    if "test_" in mm:
        #print("mod", mm)
        tmpfile = mm

#print("tmpfile", tmpfile)

baseall = os.path.join(test_dir, tmpfile)
print("baseall", baseall)
#assert 0

# ------------------------------------------------------------------------
# Support utilities

# Return a random string based upon length

def randbin(lenx):

    strx = ""
    for aa in range(lenx):
        ridx = random.randint(0, 255)
        strx += chr(ridx)
    return strx.encode("cp437", errors="ignore")


# EOF
