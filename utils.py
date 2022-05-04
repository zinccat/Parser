import nltk

def text_to_pos(text):
    """
    Convert text to POS tags.
    input: text
    output: split: list of splitted text, tags: list of POS tags
    """
    lower_case = text.lower()
    tokens = nltk.word_tokenize(lower_case)
    split, tags = [], []
    postags = nltk.pos_tag(tokens)
    for w, tag in postags:
        split.append(w)
        tags.append(tag)
    return split, tags

def grammar_generation(save_path, non_lexical=True):
    """
    Get grammar from penn treebank.
    input: path to file
    output: grammar
    """
    import nltk
    from nltk.corpus import treebank
    from nltk.grammar import PCFG, CFG, Nonterminal

    tbank_productions = set(production for sent in treebank.parsed_sents()
                        for production in sent.productions())
    tbank_grammar = CFG(Nonterminal('S'), list(tbank_productions))

    # compress grammar
    compressed = {}
    for w in tbank_grammar.productions():
        if non_lexical and w.is_lexical():
            continue
        lhs, rhs = str(w).split(' -> ')
        if lhs not in compressed:
            compressed[lhs] = []
        compressed[lhs].append(rhs)
    for g in compressed.keys():
        compressed[g] = list(set(compressed[g]))
        compressed[g].sort()
    with open(save_path, 'w') as f:
        for w in sorted(compressed):
            f.write(w+' -> '+' | '.join(compressed[w])+'\n')

if __name__ == '__main__':
    text = 'Colorless green ideas sleep furiously.'
    print(text_to_pos(text))