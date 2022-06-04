import CFG2CNF
import utils
import heapq


class Node:

    def __init__(self, parent, child_1, child_2, probability):
        self.parent, self.child_1, self.child_2, self.pro = parent, child_1, child_2, probability

    def nprint(self):
        print(self.parent, self.child_1, self.child_2, self.pro)


class Parser:

    def __init__(self, k=2, full_output=True, grammar_file="./grammars/grammar_penn_nonlexical_simplified_prob_compressed_new.txt"): 
        self.parse_dict = CFG2CNF.getCNF(grammar_file, prob=True)
        self.k = k # control beam search size
        self.full_output = full_output

    def parse(self, sentence):
        '''
        fill in the self.parse_table
        input: None
        output: None
        :return:
        '''
        self.sentence = sentence
        self.cut_text, self.pos = utils.text_to_pos(sentence)
        self.sen_len = len(self.cut_text)
        self.parse_table = [
            [[] for j in range(self.sen_len)] for i in range(self.sen_len)]

        for j,word in enumerate(self.pos):
            self.parse_table[j][j].append(Node(word,self.cut_text[j],None,1.0))
            if word in self.parse_dict:
                for item in self.parse_dict[word]:
                    self.parse_table[j][j].append(Node(item[0], word, None, item[1]))
            # print(word)
            for i in range(j-1, -1, -1):
                for k in range(i, j):
                    tmp_child_1 = self.parse_table[i][k]
                    tmp_child_2 = self.parse_table[k + 1][j]
                    for item1 in tmp_child_1:
                        for item2 in tmp_child_2:
                            tmp = item1.parent+" "+item2.parent
                            if tmp in self.parse_dict:
                                list1 = self.parse_dict[tmp]
                                list2 = [Node(thead[0], item1, item2, thead[1]*item1.pro*item2.pro) for thead in list1]
                                # get the k largest elements in list2
                                list2 = heapq.nlargest(self.k, list2, key=lambda x: x.pro)
                                self.parse_table[i][j].extend(list2)
                                # exit(0)
                                # self.parse_table[i][j].extend(
                                    # [Node(thead[0], item1, item2, thead[1]*item1.pro*item2.pro) for thead in list1])

    def print_tree(self):
        start_symbol = 'S'
        top_nodes = [n for n in self.parse_table[0]
                     [self.sen_len-1] if n.parent == start_symbol]
        if self.full_output:
            print("Number of possible parses:", len(top_nodes))
        if top_nodes:
            if self.full_output:
                print("Possible parses:")
            nmax = 0
            max_node = None
            for top_node in top_nodes:
                if self.full_output:
                    generate_tree(top_node)
                    print(', with probability', top_node.pro)
                nmax = max(nmax, top_node.pro)
                max_node = top_node
            print("The most possible parse for '{}' is: ".format(self.sentence), end="")
            generate_tree(max_node)
            print(", and its possibility is", nmax)
        else:
            print("No suitable parsing!")


def generate_tree(node):
    if isinstance(node,Node):
        if node.child_2 != None:
            print('[', node.parent, " ", end="")
            generate_tree(node.child_1)
            print(' ', end="")
            generate_tree(node.child_2)
            print(']', end="")
        elif node.child_1!=None:
            print('[', node.parent, " ", end="")
            generate_tree(node.child_1)
            print(']', end="")
        else:
            print('[', node.parent, "]", end="")
    else:
        print('\'',node,'\'',end="")


if __name__ == '__main__':
    # CKY = Parser("./grammars/grammar_penn_nonlexical_prob_compressed.txt")
    CKY = Parser(k=2, full_output=False)
    CKY.parse("Colorless green ideas sleep furiously")
    # CKY.parse("The cat is on the mat")
    # CKY.parse("I like to eat")
    CKY.print_tree()
