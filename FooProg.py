operators = ["*", "/", "+", "-", "="]
#pri = {"*": 3, "/": 3, "+": 2, "-": 2,'<':1,'>':1,'>=':'1','<=':1,'==':1 ,"=": 0}
pri = {"*": 3, "/": 3, "+": 2, "-": 2,'==':1 ,"=": 0}
keywords = ["read ", "write ","do","while "]


def tokenize(code):
    code+=';'
    sentens = []
    words = []
    it = 0
    while it < len(code):
        if it < len(code):
            # print(it,code[it])
            if code[it] == "$":
                it += 1
                tmp = ""
                while code[it] != "$":
                    if code[it] != "$":
                        if (
                            code[it]
                            not in ";(){}"
                        ):
                            tmp += code[it]
                        else:
                            print(
                                "variable names can't be semicolons or brackets"
                                % code[it]
                            )
                            return 3
                    it += 1
                words += [(tmp, "var")]
            elif code[it] == ";":
                sentens.append(words[:])
                words = []
            elif code[it] in " \n\t":
                pass
            elif code[it] in "()":
                words.append((code[it], "bracket"))
            elif code[it] in "1234567890":
                if code[it] == "0":
                    if it==len(code)-1:
                        words += [("0", "number")]
                    elif code[it + 1] == "o":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        words += [(tmp, "oct")]
                    elif code[it + 1] == "x":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890ABCDEFabcdef":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        words += [(tmp.lower(), "hex")]
                    elif code[it + 1] == "b":
                        it += 2
                        tmp = ""
                        while code[it] in "1234567890":
                            tmp += code[it]
                            it += 1
                        it -= 1
                        words += [(tmp, "bin")]
                    else:
                        words += [("0", "number")]
                else:
                    tmp = ""
                    while it < len(code) and code[it] in "1234567890.":
                        tmp += code[it]
                        it += 1
                    it -= 1
                    words += [(tmp, "number")]
            elif code[it] == "#":
                while code[it] != "\n":
                    it += 1
            elif code[it] in "{}":
                words+=[(code[it],'lb')]
            else:
                tmpop = ""
                tmpkey = ""
                for kw1 in keywords:
                    # print(code[it])
                    flag = True
                    tmpit2 = it
                    kw = kw1
                    for i in range(len(kw)):
                        if kw[i] != code[tmpit2]:
                            flag = False
                            break
                        tmpit2 += 1
                    if flag:
                        tmpkey = kw
                        break
                for op in operators:
                    flag = True
                    tmpit = it
                    for i in range(len(op)):
                        if op[i] != code[tmpit]:
                            flag = False
                            break
                        tmpit += 1
                    if flag:
                        tmpop = op
                        break
                if tmpop == "" and tmpkey == "":
                    print(
                        "T1: Cannot match known operators or keywords to code in char %d"
                        % it
                    )
                    return 1
                if tmpop != "":
                    words += [(tmpop, "oper")]
                    # print(it,tmpit)
                    it = tmpit - 1
                if tmpkey != "":
                    words += [(tmpkey.strip(), "key")]
                    # print(it,tmpit)
                    it = tmpit2 - 1
                # print(it)
            it += 1
    return sentens


def tob(x):
    res = b""
    for i in range(8):
        res += bytes([x & 255])
        x >>= 8
    return res


def tobk(val):  # 0 add 1 sub 2 mul 3 div 4 set 5 copy 6 read 7 write
    res = b""
    vals = {}
    buf = 0
    xxx=[]
    for st in val:
        s = []
        t = []
        wdi = 0
        while wdi < len(st):
            wd = st[wdi]
            if wd[1] in ["number", "hex", "bin", "oct", "var"]:
                ttt = 0
                if wd[1] == "var":
                    if wd[0] not in vals:
                        vals[wd[0]] = buf
                        buf += 1
                    ttt = vals[wd[0]]
                else:
                    if wd[1] == "number":
                        res += (
                            b"\x04"
                            + tob(buf)
                            + b"\x01"
                            + bytes(wd[0].encode())
                            + b"\x00"
                        )
                        ttt = buf
                        buf += 1
                    else:
                        m = 0
                        if wd[1] == "bin":
                            m = int(wd[0], 2)
                        elif wd[1] == "oct":
                            m = int(wd[0], 8)
                        elif wd[1] == "hex":
                            m = int(wd[0], 16)
                        res += b"\x04" + tob(buf) + b"\x00" + tob(m)
                        ttt = buf
                        buf += 1
                t.append(ttt)
            elif wd[1] == "oper":
                while not (not s or s[-1] == "(" or pri[s[-1]] < pri[wd[0]]):
                    x = s.pop()
                    u = t.pop()
                    v = t.pop()
                    if x == "+":
                        res += b"\x00" + tob(v) + tob(u) + tob(buf)
                    if x == "-":
                        res += b"\x01" + tob(v) + tob(u) + tob(buf)
                    if x == "*":
                        res += b"\x02" + tob(v) + tob(u) + tob(buf)
                    if x == "/":
                        res += b"\x03" + tob(v) + tob(u) + tob(buf)
                    if x == "=":
                        res += b"\x05" + tob(v) + tob(u)
                    if x != "=":
                        t.append(buf)
                        buf += 1
                    else:
                        t.append(v)
                s.append(wd[0])
            elif wd[0] == "(":
                s.append("(")
            elif wd[0] == ")":
                while not (s[-1] == "("):
                    x = s.pop()
                    u = t.pop()
                    v = t.pop()
                    if x == "+":
                        res += b"\x00" + tob(v) + tob(u) + tob(buf)
                    if x == "-":
                        res += b"\x01" + tob(v) + tob(u) + tob(buf)
                    if x == "*":
                        res += b"\x02" + tob(v) + tob(u) + tob(buf)
                    if x == "/":
                        res += b"\x03" + tob(v) + tob(u) + tob(buf)
                    if x == "=":
                        res += b"\x05" + tob(v) + tob(u)
                    if x != "=":
                        t.append(buf)
                        buf += 1
                    else:
                        t.append(v)
                s.pop()
            elif wd[1] == "key":
                f = wd[0]
                if wd[0] == "read":
                    wd2 = st[wdi + 1]
                    if wd2[1] != "var":
                        print("C1: Can only read variables")
                        return 1
                    if wd2[0] in vals:
                        res += b"\x06" + tob(vals[wd2[0]])
                    else:
                        res += b"\x06" + tob(buf)
                        vals[wd2[0]] = buf
                        buf += 1
                    wdi += 1
                elif wd[0] == "write":
                    wd2 = st[wdi + 1]
                    if wd2[1] == "var":
                        if wd2[0] not in vals:
                            print("C2: Cannot write non existent variables")
                            return 2
                        else:
                            res += b"\x07" + tob(vals[wd2[0]])
                        wdi += 1
                    else:
                        if wd2[1] not in ["number", "hex", "oct", "bin"]:
                            print("C6: Cannot write unknown literal type %s", wd2[1])
                            return 6
                        else:
                            match wd2[1]:
                                case "number":
                                    res += (
                                        b"\x04"
                                        + tob(buf)
                                        + b"\x01"
                                        + bytes(wd2[0].encode())
                                        + b'\x00'
                                    )
                                case "hex":
                                    res += (
                                        b"\x04"
                                        + tob(buf)
                                        + b"\x00"
                                        + bytes(int(wd2[0], 16))
                                    )
                                case "oct":
                                    res += (
                                        b"\x04"
                                        + tob(buf)
                                        + b"\x00"
                                        + bytes(int(wd2[0], 8))
                                    )
                                case "bin":
                                    res += (
                                        b"\x04"
                                        + tob(buf)
                                        + b"\x00"
                                        + bytes(int(wd2[0], 2))
                                    )
                            res += b"\x07" + tob(buf)
                            buf += 1
                    wdi += 1
                elif wd[0]=='do':
                    if st[wdi+1][0]!='{':
                        print('C3: "do" must be followed by {')
                        return 3
                    xxx.append(('do',len(res)))
                    wdi+=1
            elif wd[1]=='lb':
                if wd[0]=='}':
                    ppp=xxx.pop()
                    match ppp[0]:
                        case 'do':
                            if st[wdi+1][0]!='while':
                                print('C4: "do" without "while"')
                                return 4
                            if st[wdi+2][1]!='var':
                                print('C5: "while" only supports variables currently')
                                return 5
                            res+=b'\x08'+tob(vals[st[wdi+2][0]])+tob(ppp[1])
                            wdi+=2
            wdi += 1
        while s:
            if s:
                x = s.pop()
                u = t.pop()
                v = t.pop()
                if x == "+":
                    res += b"\x00" + tob(v) + tob(u) + tob(buf)
                if x == "-":
                    res += b"\x01" + tob(v) + tob(u) + tob(buf)
                if x == "*":
                    res += b"\x02" + tob(v) + tob(u) + tob(buf)
                if x == "/":
                    res += b"\x03" + tob(v) + tob(u) + tob(buf)
                if x == "=":
                    res += b"\x05" + tob(v) + tob(u)
                if x != "=":
                    t.append(buf)
                    buf += 1
                else:
                    t.append(v)
    return res


def bktoi(bk):
    res = 0
    n = 1
    for i in range(8):
        res += bk[i] * n
        n <<= 8
    return res


def runbk(bk):
    it = 0
    buf = {}
    while it < len(bk):
        match bk[it]:
            case 0:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                # print(m,n,o,buf)
                resm, resn = 0, 0
                if m in buf:
                    resm = buf[m]
                if n in buf:
                    resn = buf[n]
                buf[o] = resm + resn
                # print(buf[o])
                it += 25
            case 1:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                resm, resn = 0, 0
                if m in buf:
                    resm = buf[m]
                if n in buf:
                    resn = buf[n]
                buf[o] = resm - resn
                it += 25
            case 2:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                resm, resn = 0, 0
                if m in buf:
                    resm = buf[m]
                if n in buf:
                    resn = buf[n]
                buf[o] = resm * resn
                it += 25
            case 3:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                resm, resn = 0, 0
                if m in buf:
                    resm = buf[m]
                if n in buf:
                    resn = buf[n]
                buf[o] = resm / resn
                it += 25
            case 4:
                m = bk[it + 1 : it + 9]
                m = bktoi(m)
                n = bk[it + 9]
                match n:
                    case 0:
                        buf[m] = bktoi(bk[it + 10 : it + 18])
                        it += 18
                    case 1:
                        it1 = it + 10
                        resk = ""
                        while bk[it1]:
                            resk += chr(bk[it1])
                            it1 += 1
                        buf[m] = float(resk)
                        it = it1 + 1
            case 5:
                m, n = bk[it + 1 : it + 9], bk[it + 9 : it + 17]
                m, n = bktoi(m), bktoi(n)
                resm = 0
                if n in buf:
                    resm = buf[n]
                buf[m] = resm
                it += 17
            case 6:
                try:
                    x = float(input())
                except ValueError:
                    print('R1: The input is not a valid value for FooProg type "number"')
                    return 1
                m = bk[it + 1 : it + 9]
                buf[bktoi(m)] = x
                it += 9
            case 7:
                m = bk[it + 1 : it + 9]
                print(buf[bktoi(m)])
                it += 9
            case 8:
                m,n=bk[it+1:it+9],bk[it+9:it+17]
                m,n=bktoi(m),bktoi(n)
                resm=0
                if m in buf:
                    resm=buf[m]
                if resm!=0:
                    it=n
                else:
                    it+=17
    return buf
def disasm(bk):
    it=0
    res=[]
    while it<len(bk):
        match bk[it]:
            case 0:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                res.append((f'add {m},{n} -> {o}',it,it+24))
                it+=25
            case 1:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                res.append((f'sub {m},{n} -> {o}',it,it+24))
                it+=25
            case 2:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                res.append((f'mul {m},{n} -> {o}',it,it+24))
                it+=25
            case 3:
                m, n, o = (
                    bk[it + 1 : it + 9],
                    bk[it + 9 : it + 17],
                    bk[it + 17 : it + 25],
                )
                m, n, o = bktoi(m), bktoi(n), bktoi(o)
                res.append((f'div {m},{n} -> {o}',it,it+24))
                it+=25
            case 4:
                m = bk[it + 1 : it + 9]
                m = bktoi(m)
                n = bk[it + 9]
                match n:
                    case 0:
                        res.append((f'set {m},{bktoi(bk[it + 10 : it + 18])}:uint',it,it+18))
                        it += 18
                    case 1:
                        it1 = it + 10
                        resk = ""
                        while bk[it1]:
                            resk += chr(bk[it1])
                            it1 += 1
                        res.append((f'set {m},{resk}:float',it,it1+1))
                        it = it1 + 1
            case 5:
                m, n = bk[it + 1 : it + 9], bk[it + 9 : it + 17]
                m, n = bktoi(m), bktoi(n)
                res.append((f'copy {m},{n}',it,it+16))
                it += 17
            case 6:
                m = bk[it + 1 : it + 9]
                res.append((f'read {bktoi(m)}',it,it+9))
                it += 9
            case 7:
                m = bk[it + 1 : it + 9]
                res.append((f'write {bktoi(m)}',it,it+9))
                it += 9
            case 8:
                m,n=bk[it+1:it+9],bk[it+9:it+17]
                m,n=bktoi(m),bktoi(n)
                res.append((f'jif {m} -> {n}',it,it+17))
                it+=17
            case _:
                print(f'Disassembly failed: invalid character {bk[it]} on {it}')
                return None
    return res
#print(disasm(tobk(tokenize('$a$=1;do{write 1;}while $a$;'))))
#print(disasm(tobk(tokenize('$a$=0xFF;do{write $a$;$a$=$a$-1;}while $a$;'))))
#print(disasm(tobk(tokenize('read $a$;read $b$;$c$=$a$+$b$;write $c$;$d$=$c$+$a$;write $d$;'))))
