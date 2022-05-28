import nltk
from nltk.corpus import treebank
from nltk.grammar import PCFG, CFG, Nonterminal
import collections

# tbank_productions = set(production for sent in treebank.parsed_sents()
#                         for production in sent.productions())
# tbank_grammar = CFG(Nonterminal('S'), list(tbank_productions))

tbank_prod = list(production for sent in treebank.parsed_sents()
                        for production in sent.productions())

counter=collections.Counter(tbank_prod)

def simplify(x):
    x = x.split(' ')
    l = []
    for w in x:
        if w[0] == '-':
            l.append(w)
        else:
            l.append(w.split('-')[0])
    return ' '.join(l)
compressed = {}
for w in counter.keys():
    if w.is_nonlexical():
        lhs, rhs = str(w).split(' -> ')
    # if w.is_nonlexical():
        lhs = simplify(lhs)
        rhs = simplify(rhs)
    if lhs == rhs:
        continue
    if lhs not in compressed:
        compressed[lhs] = {}
    if rhs not in compressed[lhs]:
        compressed[lhs][rhs] = counter[w]
    else:
        compressed[lhs][rhs] += counter[w]

for v in compressed.keys():
    # compressed[v] = list(set(compressed[v]))
    s = 0
    for w in compressed[v].keys():
        s += compressed[v][w]
    # for i in range(len(compressed[v])):
    #     compressed[v][i] = (compressed[v][i][0], compressed[v][i][1]/s)
    for w in compressed[v].keys():
        compressed[v][w] = compressed[v][w]/s
    # compressed[v].sort(key=lambda y: -y[1])


with open("./grammars/grammar_penn_nonlexical_simplified_prob_compressed_new.txt", 'w') as f:
    for w in sorted(compressed):
        list1 = []
        for x in compressed[w].keys():
            list1.append((x, compressed[w][x]))
        list1.sort(key=lambda y: -y[1])
        list2 = []
        for j in list1:
            list2.append(j[0]+' '+str(j[1]))
            # list2.append(j+' '+str(compressed[w][j]))
        f.write(w+' -> '+' / '.join(list2)+'\n')