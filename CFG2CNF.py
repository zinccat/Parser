
rdic = {}
flag = {}


def split2dic(rlist):
    for item in rlist:
        tmp = item.split("->")
        arg = tmp[0].strip()
        content = tmp[1].split("|")
        if not arg in rdic.keys():
            rdic[arg] = []
        for i in content:
            tmp = i.split()
            rdic[arg].append(tmp)
    print(rdic)


def isend(arg):
    tmp = arg.strip()
    if tmp[0] == "'" and tmp[len(tmp)-1] == "'":
        return True
    return False


def getCNF(readFile):
    rFile = open(readFile, "r")
    rlist = rFile.read().splitlines()
    print(rlist)
    split2dic(rlist)
    print(rdic)
    global edic
    edic = {}
    global cnt
    cnt = 0
    rdic["S0"] = [["S"]]
    dlist = []

    for arg in rdic.keys():
        for con in rdic[arg]:
            if con == [] and len(rdic[arg]) == 1:
                for narg in rdic.keys():
                    for ncon in rdic[narg]:
                        while arg in ncon:
                            rdic[narg].remove(ncon)
                        if arg in ncon:
                            ncon.remove(arg)
                            rdic[narg].append(ncon)
                rdic[arg].remove(con)
            elif con == []:
                for narg in rdic.keys():
                    for ncon in rdic[narg]:
                        if arg in ncon:
                            ncon.remove(arg)
                            rdic[narg].append(ncon)
                rdic[arg].remove(con)
        if len(rdic[arg]) == 0:
            dlist.append(arg)

    for arg in dlist:
        rdic.remove(arg)

    for arg in rdic.keys():
        dcon = []
        for con in rdic[arg]:
            if len(con) == 1 and not isend(con[0]):
                print(arg, con)
                if not arg in edic:
                    edic[arg] = []
                edic[arg].append(con[0])
                dcon.append(con)
        for con in dcon:
            rdic[arg].remove(con)

    adic = {}

    for arg in rdic.keys():
        for con in rdic[arg]:
            if len(con) > 2:
                rdic[arg].remove(con)
                while len(con) > 2:
                    narg = f"tmp{cnt}"
                    cnt = cnt+1
                    ncon = con[-2:]
                    adic[narg] = [ncon]
                    con = con[0:-2]+[narg]
                else:
                    rdic[arg].append(con)

    for arg in adic.keys():
        rdic[arg] = adic[arg]

    for arg in edic.keys():
        if not arg in flag.keys():
            equal(arg)

    wFile = open("new_grammar.txt", "w")
    for arg in rdic.keys():
        for con in rdic[arg]:
            res = f"{arg} -> "
            for item in con:
                res = res+f"{item} "
            print(res, file=wFile)
    return rdic


def equal(arg):
    flag[arg] = 1
    for narg in edic[arg]:
        if arg in rdic.keys() and narg in rdic.keys():
            if narg in edic.keys() and not narg in flag.keys():
                equal(narg)
            rdic[arg] = rdic[arg]+rdic[narg]
