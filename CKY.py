import nltk
from nltk.tokenize import word_tokenize
import argparse
import CFG2CNF

class Node:

    def __init__(self,parent,child_1,child_2):
        self.parent,self.child_1,self.child_2=parent,child_1,child_2

class Parser:

    def __init__(self,sen_file):
        with open(sen_file) as s_f:
            sentence=s_f.readline()
        self.cut_text=word_tokenize(sentence)
        self.sen_len = len(self.cut_text)
        #print(self.sen_len)
        self.parse_table=[[[] for j in range(self.sen_len)] for i in range(self.sen_len)]
        self.parse_dict=CFG2CNF.getCNF("exam_grammar.txt")
        #print(self.parse_dict)

    def parse(self):
        for j,word in enumerate(self.cut_text):
            for head in self.parse_dict.keys():
                for childs in self.parse_dict[head]:
                    #print(len(childs),childs[0])
                    if len(childs)==1 and childs[0]=='\''+word+'\'':
                        tmp_n=Node(head,word,None)
                        self.parse_table[j][j].append(Node(head,word,None))
                        #print(tmp_n)
            for i in range(j-1,-1,-1):
                for k in range(i,j):
                    ok=0
                    tmp_child_1=self.parse_table[i][k]
                    tmp_child_2=self.parse_table[k+1][j]
                    for head in self.parse_dict.keys():
                        for childs in self.parse_dict[head]: #a child is a pair of child nodes
                            child_1_node = [n for n in tmp_child_1 if n.parent == childs[0]]  # type node
                            if child_1_node:
                                child_2_node = [n for n in tmp_child_2 if n.parent == childs[1]]
                                if child_2_node:
                                    self.parse_table[i][j].extend(
                                        [Node(head, child1, child2) for child1 in child_1_node
                                         for child2 in child_2_node])

    def print_tree(self):
        start_symbol='S'
        top_nodes=[n for n in self.parse_table[0][self.sen_len-1] if n.parent==start_symbol]
        if top_nodes:
            print("Possible parses:")
            for top_node in top_nodes:
                #print(top_node.child_2)
                generate_tree(top_node)
                print("")
        else:
            print("No suitable parsing!")

def generate_tree(node):
    if node.child_2!=None:
        print('[',node.parent," ",end="")
        generate_tree(node.child_1)
        print(' ',end="")
        generate_tree(node.child_2)
        print(']',end="")
    else:
        print('[',node.parent, " \'",node.child_1,'\']',end="")

if __name__ == '__main__':
    CKY=Parser("sentence.txt")
    CKY.parse()
    CKY.print_tree()
