    #(INI_STATE, "char",     "char"         ,  STATE_NOCH, ),
    #(INI_STATE, "short",    "short"         , STATE_NOCH, ),
    #(INI_STATE, "int"  ,    "int"           , STATE_NOCH, ),
    #(INI_STATE, "long" ,    "long"          , STATE_NOCH, ),
    #(INI_STATE, "uchar" ,   "uchar"         , STATE_NOCH, ),
    #(INI_STATE, "ushort",   "ushort"        , STATE_NOCH, ),
    #(INI_STATE, "uin"  ,    "uint"          , STATE_NOCH, ),
    #(INI_STATE, "ulon" ,    "ulong"         , STATE_NOCH, ),

'''
        # Move to sub item
        statex = 0; typey = "" ; typex = "" ; lab = ""; val = "";
        orgline = 0
        #for aa in arithstack:
        for aa in stackstack:
            if self2.arrx[aa].flag:
                continue
            #if self2.arrx[aa].stamp.xstr == "sp":
            #    self2.arrx[aa].flag = 1
            #    continue
            strx = ""
            if pvg.opt_debug > 7:
                print("st:", statex, pp(self2.arrx[aa].stamp.xstr), self2.arrx[aa].mstr)
            if statex == 0:
                #if self2.arrx[aa].stamp.xstr == "decl":
                if self2.arrx[aa].stamp.xstr in numtypes:
                    statex = 1
                    typey = self2.arrx[aa].mstr
                    typex = linpool.pctona(self2.arrx[aa].mstr)
                if self2.arrx[aa].stamp.xstr == "ident":
                    statex = 4
                    orgline =  self2.arrx[aa].linenum
                    lab = scopestack.peek() + self2.arrx[aa].mstr
            elif statex == 1:
                if self2.arrx[aa].stamp.xstr == "ident":
                    lab = scopestack.peek() + self2.arrx[aa].mstr
                    statex = 2
            elif statex == 2:
                if self2.arrx[aa].stamp.xstr == "ident":
                    strx = lab + " : " + typex + " "  + " 0 " + \
                            "; line: " + str(orgline+1) + \
                            " generated from " + pp(lab) + "\n"
                    codegen.emitdata(strx)
                    statex = 1
                if self2.arrx[aa].stamp.xstr == "=":
                    statex = 3
            elif statex == 3:
                val = self2.arrx[aa].mstr
                linenum = self2.arrx[aa].linenum
                linpool.add2pool(self2, typey, lab, val, linenum)
                statex = 0
                # output decl opeartion
                #print("typex :", typex, "typey:", typey, "lab =", pp(lab), "val =", val)
                if typey.lower() in int_types:
                    #print("int type", lab, typex, val)
                    if arithstack.getlen() <= 4:
                        # patch missing declaration argument with zero /empty
                        strx += " 0 "
                    else:
                        strx +=  lab + " : " + typex + " " + val + "\n"
                elif typey.lower() in float_types:
                    #print("float type", lab, typex, val)
                    if arithstack.getlen() <= 3:
                        # patch missing declaration argument with zero /empty
                        strx += " 0 "
                    else:
                        strx +=  lab + " : " + typex + " " + val + "\n"
                else:
                    #print("other type", typex)
                    error(self2, "No type specified")
                codegen.emitdata(strx)

            elif statex == 4:
                if self2.arrx[aa].stamp.xstr == "num":
                    state = 0
                    tpi = linpool.lookpool(self2, lab)
                    if not tpi:
                        error(self2, "Undefined variable", )
                    typex = linpool.pctona(tpi.typex)
                    typey = tpi.typex
                    val = self2.arrx[aa].mstr
                    # output assn opeartion
                    ttt = linpool.pctocast(typey)
                    #print("ttt", ttt)
                    strx += "   mov   " + ttt + " [" + lab + "], " + val + "\n"
                    codegen.emit(strx)
            else:
                pass
                print("Warn: invalid state", __file__, __line__)

        if statex == 1:
            # Comma operator left this incomplete
            #print("left over:", lab, typex, val)
            strx = self2.arrx[aa].mstr + " : " + typex + " 0 " + "; line: " \
                                        + str(self2.arrx[aa].linenum+1) \
                                        + " -- generated from " \
                                        + self2.arrx[aa].mstr + "\n"
            codegen.emitdata(strx)
        '''

