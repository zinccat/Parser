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
            #print(j,word)
            if word in self.parse_dict:
                for item in self.parse_dict[word]:
                    self.parse_table[j][j].append(Node(item[0], self.cut_text[j],None, item[1]))
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
    
    def table_to_visual(self):
        '''
        input:原代码中的self.grammer和self.parse_table
        output:多种形式的可视化句法树
        '''
        start_symbol = 'S'
        # final_nodes is the the cell in the upper right hand corner of the parse_table
        # we choose the node whose parent is the start_symbol
        final_nodes = [n for n in self.parse_table[0][-1] if n.parent == start_symbol]
        if final_nodes:
            print("Possible parses:")
            nmax=0
            max_node=None
            for top_node in final_nodes:
                if nmax<top_node.pro:
                    nmax = max(nmax, top_node.pro)
                    max_node = top_node
            write_trees = [generate_tree(node) for node in final_nodes]
            for x in write_trees:
                print(x)
            write_tree = generate_tree(max_node)
            print(write_tree)
            Tree.fromstring(write_tree).draw()

def generate_tree(node):
    """
    input:parse_table中的node
    """
    if node.child_2 is None:
        return f"({node.parent} '{node.child_1}')"
    return f"({node.parent} {generate_tree(node.child_1)} {generate_tree(node.child_2)})"

if __name__ == '__main__':
    # CKY = Parser("./grammars/grammar_penn_nonlexical_prob_compressed.txt")
    CKY = Parser(k=2, full_output=False)
    CKY.parse("Colorless green ideas sleep furiously")
    # CKY.parse("The cat is on the mat")
    # CKY.parse("I like to eat")
    CKY.table_to_visual()
