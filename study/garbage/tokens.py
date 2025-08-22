tok = \
         {
         "#define"  : punique(),
         "#undef"   : punique(),
         "#ifdef"   : punique(),
         "#elifdef" : punique(),
         "#else"    : punique(),
         "#endif"   : punique(),
         "#"        : punique(),

         "comma"    : punique(),
         "colon"    : punique(),
         "scolon"    : punique(),
         "num"    : punique(),
         "hex"    : punique(),
         "oct"    : punique(),
         "bin"    : punique(),

         "shex"    : punique(),

         # Basic types
         "char"      : punique(),       # 8
         "short"     : punique(),       # 16
         "int"       : punique(),       # 32
         "long"      : punique(),       # 64

         "uchar"      : punique(),
         "ushort"     : punique(),
         "uint"       : punique(),
         "ulong"      : punique(),

         "S8"        : punique(),       # 8
         "S16"       : punique(),       # 16
         "S32"       : punique(),       # 32
         "S64"       : punique(),       # 64
         "S128"      : punique(),       # 128

         "U8"        : punique(),
         "U16"       : punique(),
         "U32"       : punique(),
         "U64"       : punique(),
         "U128"      : punique(),

         "bs"       : punique(),
         "endif"    : punique(),
         "if"       : punique(),
         "quote"    : punique(),
         "ident"    : punique(),
         "str"      : punique(),
         "str2"     : punique(),
         "str3"     : punique(),
         "str4"     : punique(),
         "strx"     : punique(),
         "comm"     : punique(),
         "eq"       : punique(),
         "peq"       : punique(),
         "meq"       : punique(),
         "deq"       : punique(),
         "lt"       : punique(),
         "gt"       : punique(),
         "sp"       : punique(),
         "lbrack"   : punique(),
         "rbrack"   : punique(),
         "lbrace"   : punique(),
         "rbrace"   : punique(),
         "lcurl"   : punique(),
         "rcurl"   : punique(),
         "tab"      : punique(),
         "tab2"     : punique(),
         "eolnl"    : punique(),
         "nl"       : punique(),
         "n"        : punique(),
         "r"        : punique(),
         "a"        : punique(),
         "0"        : punique(),

         # Fall through
         "anyx"     : punique(),
         "any"      : punique(),
         }

