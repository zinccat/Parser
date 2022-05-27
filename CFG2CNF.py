rdic = {}
flag = {}
tmpdic = {}

endtype = [
    "$", "''", "(", ")", ",", "--", ".", ":", "CC", "CD", "DT", "EX", "FW",
    "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT",
    "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB",
    "VBD", "VBG", "VBN", "VBP", "VBZ", "WDT", "WP", "WP$", "WRB", "``"
]


def split2dic(rlist, prob):
    for idx, item in enumerate(rlist):
        tmp = item.split("->")
        arg = tmp[0].strip()
        content = tmp[1].split("/")
        if not arg in rdic.keys():
            rdic[arg] = []
        for i in content:
            tmp = i.split()
            if prob:
                rdic[arg].append((tmp[0:-1], float(tmp[-1])))
            else:
                rdic[arg].append((tmp, 0))


def isend(arg):
    tmp = arg.strip()
    return tmp in endtype

def toStr(tmp):
    strans=""
    for i in tmp:
        strans=strans+i
    return strans

def getCNF(readFile, prob=True,unique=True):
    global wFile
    global edic
    global cnt

    rFile = open(readFile, "r")

    rlist = rFile.read().splitlines()
    split2dic(rlist, prob)
    edic = {}
    cnt = 0
    rdic["S0"] = [(["S"], 1.0)]
    dlist = []

    for arg in rdic.keys():
        for con in rdic[arg]:
            if con[0] == [] and len(rdic[arg]) == 1:
                for narg in rdic.keys():
                    for ncon in rdic[narg]:
                        while arg in ncon[0]:
                            rdic[narg].remove(ncon)
                        if arg in ncon[0]:
                            ncon[0].remove(arg)
                            rdic[narg].append(ncon)
                rdic[arg].remove(con)
            elif con[0] == []:
                for narg in rdic.keys():
                    for ncon in rdic[narg]:
                        if arg in ncon[0]:
                            ncon[0].remove(arg)
                            rdic[narg].append(ncon)
                rdic[arg].remove(con)
        if len(rdic[arg]) == 0:
            dlist.append(arg)

    for arg in dlist:
        rdic.remove(arg)

    for arg in rdic.keys():
        dcon = []
        for con in rdic[arg]:
            if len(con[0]) == 1 and not isend(con[0][0]):
                if not arg in edic:
                    edic[arg] = []
                edic[arg].append(con)
                dcon.append(con)
        for con in dcon:
            rdic[arg].remove(con)

    adic = {}

    for arg in rdic.keys():
        dcon = []
        for con in rdic[arg]:
            tmp = con[0]
            if len(tmp) > 2:
                dcon.append(con)
                tmpstr = ""
                while len(tmp) > 2:
                    ncon = tmp[-2:]
                    tmpstr=toStr(ncon)
                    if tmpstr in tmpdic.keys() and unique:
                        narg = tmpdic[tmpstr]
                        tmp = tmp[0:-2]+[narg]
                        continue
                    narg = f"tmp{cnt}"
                    cnt = cnt+1
                    tmpdic[tmpstr] = narg
                    adic[narg] = [(ncon, 1.0)]
                    tmp = tmp[0:-2] + [narg]
                else:
                    rdic[arg].append((tmp, con[1]))
        for con in dcon:
            rdic[arg].remove(con)

    for arg in adic.keys():
        rdic[arg] = adic[arg]

    for arg in edic.keys():
        if not arg in flag.keys():
            equal(arg)

    tdic = {}

    for arg in rdic.keys():
        for con in rdic[arg]:
            index = ""
            for item in con[0]:
                index = index + item + " "
            index = index.strip()
            if index in tdic.keys():
                tflag = True
                for (x,y) in tdic[index]:
                    if x == arg :
                        tdic[index].remove((x,y))
                        tdic[index].append((x,y+con[1]))
                        tflag=False
                        break
                if tflag :
                    tdic[index].append((arg, con[1]))
            else:
                tdic[index] = [(arg, con[1])]
    return tdic


def equal(arg):
    flag[arg] = 1
    for narg in edic[arg]:
        tmpt = narg[0][0]
        if tmpt == arg:
            continue
        if arg in rdic.keys() and tmpt in rdic.keys():
            if tmpt in edic.keys() and not tmpt in flag.keys():
                equal(tmpt)
            for con in rdic[tmpt]:
                tmp = con[0]
                rdic[arg].append((tmp, con[1]*narg[1]))

if __name__ == '__main__':
    wfile=open('tmpout.txt',"w")
    tmdic = getCNF('grammar.txt')
    for i in tmdic:
        print(f"{i}:\n{tmdic[i]}",file=wfile)
    wfile.close()