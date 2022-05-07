from nltk.tree import Tree

def generate_tree(node):
    """
    input:parse_table中的node
    """
    if node.child2 is None:
        return f"[{node.parent} '{node.child1}']"
    return f"[{node.parent} {generate_tree(node.child1)} {generate_tree(node.child2)}]"

def table_to_visual(self):
    '''
    input:原代码中的self.grammer和self.parse_table
    output:多种形式的可视化句法树
    '''
    start_symbol = self.grammar[0][0]
    # final_nodes is the the cell in the upper right hand corner of the parse_table
    # we choose the node whose parent is the start_symbol
    final_nodes = [n for n in self.parse_table[0][-1] if n.parent == start_symbol]
    if final_nodes:
        write_trees = [generate_tree(node) for node in final_nodes]
        for x in write_trees:
            print(x)
            Tree.fromstring(x).draw()