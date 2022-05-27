import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from yaml import parse
import CFG2CNF
import utils


class Node:

    def __init__(self, parent, child_1, child_2, probability):
        self.parent, self.child_1, self.child_2, self.pro = parent, child_1, child_2, probability

    def nprint(self):
        print(self.parent, self.child_1, self.child_2, self.pro)


class Parser:

    def __init__(self, grammar_file="./grammars/grammar_penn_nonlexical_simplified_prob_compressed.txt"): 
        self.parse_dict = CFG2CNF.getCNF(grammar_file, prob=True)
        # print(self.parse_dict)

    def parse(self, sentence):
        '''
        fill in the self.parse_table
        input: None
        output: None
        :return:
        '''
        self.cut_text, self.pos = utils.text_to_pos(sentence)
        print(self.pos)
        self.sen_len = len(self.cut_text)
        self.parse_table = [
            [[] for j in range(self.sen_len)] for i in range(self.sen_len)]

        for j, word in enumerate(self.pos):
            for head in self.parse_dict.keys():
                if head == word:
                    for item in self.parse_dict[head]:
                        self.parse_table[j][j].append(Node(item[0], word, None, item[1]))
            # print(word)
            for i in range(j-1, -1, -1):
                for k in range(i, j):
                    tmp_child_1 = self.parse_table[i][k]
                    tmp_child_2 = self.parse_table[k + 1][j]
                    for item1 in tmp_child_1:
                        for item2 in tmp_child_2:
                            tmp = item1.parent+" "+item2.parent
                            # print(i,j,tmp)
                            if tmp in self.parse_dict:
                                list1 = self.parse_dict[tmp]
                                self.parse_table[i][j].extend(
                                    [Node(thead[0], item1, item2, thead[1]*item1.pro*item2.pro) for thead in list1])
                for tnode in self.parse_table[i][j]:
                    for head in self.parse_dict.keys():
                        if head == tnode.parent:
                            # print(head)
                            for item in self.parse_dict[head]:
                                self.parse_table[i][j].append(Node(item[0], tnode.parent, None, item[1]*tnode.pro))

    def print_tree(self):
        start_symbol = 'S'
        top_nodes = [n for n in self.parse_table[0]
                     [self.sen_len-1] if n.parent == start_symbol]
        print(len(top_nodes))
        if top_nodes:
            print("Possible parses:")
            nmax = 0
            max_node = None
            for top_node in top_nodes:
                generate_tree(top_node)
                print(', pro=', top_node.pro)
                nmax = max(nmax, top_node.pro)
                max_node = top_node
            print("")
            print("The most possible parse is: ", end="")
            generate_tree(max_node)
            print(", and its possibility is", nmax)
        else:
            print("No suitable parsing!")


def generate_tree(node):
    if isinstance(node, Node):
        if node.child_2 != None:
            print('[', node.parent, " ", end="")
            generate_tree(node.child_1)
            print(' ', end="")
            generate_tree(node.child_2)
            print(']', end="")
        else:
            print('[', node.parent, " ", end="")
            generate_tree(node.child_1)
            print(']', end="")
    else:
        print('\'', node, '\'', end="")


if __name__ == '__main__':
    from time import time
    a = time()
    CKY = Parser()
    b = time()
    print("time:", b-a)
    CKY.parse("i love you")
    c = time()
    print("time:", c-b)
    CKY.print_tree()
