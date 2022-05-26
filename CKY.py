import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import CFG2CNF
import utils

class Node:

    def __init__(self,parent,child_1,child_2):
        self.parent,self.child_1,self.child_2=parent,child_1,child_2

    def nprint(self):
        print(self.parent,self.child_1,self.child_2)

class Parser:

    def __init__(self,sen_file):
        with open(sen_file) as s_f:
            sentence=s_f.readline()
        self.cut_text=word_tokenize(sentence)
        self.posed_text=nltk.pos_tag(self.cut_text)
        self.cut_text,self.pos=utils.text_to_pos(sentence)
        #print(self.pos)
        self.sen_len = len(self.cut_text)
        self.parse_table=[[[] for j in range(self.sen_len)] for i in range(self.sen_len)]
        self.parse_dict=CFG2CNF.getCNF("grammar_penn_nonlexical_compressed.txt",prob=0)
        #print(self.parse_dict)

    def parse(self):
        '''
        fill in the self.parse_table
        input: None
        output: None
        :return:
        '''
        for j,word in enumerate(self.pos):
            for head in self.parse_dict.keys():
                if head == word:
                    #print(head)
                    for item in self.parse_dict[head]:
                        self.parse_table[j][j].append(Node(item[0], word, None))
            #print(word)
            for i in range(j-1,-1,-1):
                for k in range(i,j):
                    tmp_child_1 = self.parse_table[i][k]
                    tmp_child_2 = self.parse_table[k + 1][j]
                    for item1 in tmp_child_1:
                        for item2 in tmp_child_2:
                            tmp=item1.parent+" "+item2.parent
                            #print(i,j,tmp)
                            if tmp in self.parse_dict:
                                list1 = self.parse_dict[tmp]
                                self.parse_table[i][j].extend([Node(thead[0], item1, item2) for thead in list1])

    def print_tree(self):
        start_symbol='S'
        top_nodes=[n for n in self.parse_table[0][self.sen_len-1] if n.parent==start_symbol]
        print(len(top_nodes))
        if top_nodes:
            print("Possible parses:")
            for top_node in top_nodes:
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
