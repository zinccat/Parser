import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import argparse
import CFG2CNF

class Node:

    def __init__(self,parent,child_1,child_2):
        self.parent,child_1,child_2=parent,child_1,child_2

class Parser:

    def __init__(self,sen_file):
        with open(sen_file) as s_f:
            sentence=s_f.readline()
        self.sen_len=len(sentence)
        self.cut_text=pos_tag(word_tokenize(sentence))
        print(self.cut_text)
        self.parse_table=[[[] for j in range(self.sen_len)] for i in range(self.sen_len)]
        self.parse_dict=CFG2CNF.getCNF("grammar.txt")

    def parse(self):
        for j,word in enumerate(self.cut_text):
            self.parse_table[j][j].append(Node(word,None,None))
            for i in range(j-1,-1,-1):
                for k in range(i,j):
                    tmp_child_1=self.parse_table[i][k]
                    tmp_child_2=self.parse_table[k+1][j]
                    for head in self.parse_dict.keys():
                        for childs in self.parse_dict[head]: #childs is a list of child pairs
                            child_1_node=[n for n in tmp_child_1 if n.parent==childs[0]] #type: Node
                            if child_1_node:
                                child_2_node=[n for n in tmp_child_2 if n.parent==childs[1]]
                                if child_2_node:
                                    self.parse_table[i][j].extend([Node(head,child1,child2) for child1 in child_1_node
                                                                   for child2 in child_2_node])


if __name__ == '__main__':
    #nltk.download('punkt')
    CKY=Parser("sentence.txt")
