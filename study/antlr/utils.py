cdepth = 0

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

