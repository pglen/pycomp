def pvar(var):

    ''' return variable description string as name => val
        this is near USELESS
    '''
    #print("pvar =", var)
    import inspect
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    strx = ""
    for aa in callers_local_vars:
        if aa[1] is var:
            if isinstance(aa[1], (type(()), type([])) ):
                strx += str(aa[0]) + " -> "
                for bb in aa[1]:
                    strx += str(bb)
            else:
                strx += str(aa[0]) + " => " + str(aa[1]) + " "
            #break
    return strx

