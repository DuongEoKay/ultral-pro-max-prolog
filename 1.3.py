def load_knowledge_base(file_name):
    knowledge_base = {}  # Initialize knowledge base as an empty dictionary
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line.startswith('%') and len(line) > 0:
                    # Remove parentheses and trailing punctuation
                    line = line.rstrip('.').rstrip(',')
                    if line.endswith(':-'):
                        line += ' true.'
                    try:
                        assert line.count(':-') == 1
                        head, body = line.split(':-')
                        head = head.strip()
                        body = body.strip()
                        if ',' in body:
                            body = body.split(',')
                            for b in body:
                                if head not in knowledge_base:
                                    knowledge_base[head] = set()
                                knowledge_base[head].add(b.strip())
                        else:
                            if head not in knowledge_base:
                                knowledge_base[head] = set()
                            knowledge_base[head].add(body)
                    except AssertionError:
                        if line not in knowledge_base:
                            knowledge_base[line] = set()
        print("Loaded Knowledge Base:")

        for key, values in knowledge_base.items():
            print(key)
        return knowledge_base  
    except:
        return None  

def forward_reasoning(knowledge_base, query):
    inferred_facts = set()
    new_facts = True
    while new_facts:
        new_facts = False
        for rule in knowledge_base.keys():
            antecedent, consequent = rule.split(':-')
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            if antecedent in knowledge_base and consequent not in knowledge_base:
                subqueries = antecedent.split(',')
                if all(sq in knowledge_base for sq in subqueries):
                    inferred_facts.add(consequent)
                    knowledge_base[consequent] = set()
                    for sq in subqueries:
                        knowledge_base[consequent].add(sq)
                    new_facts = True
    return query in inferred_facts

def backward_reasoning(query, premises, knowledge_base):
    if query in premises:
        return True
    for premise in premises:
        if premise in knowledge_base:
            return True
        if ':-' in premise:
            antecedent, consequent = premise.split(':-')
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            if consequent == query:
                subqueries = antecedent.split(',')
                subqueries = [sq.strip() for sq in subqueries]
                results = []
                for subquery in subqueries:
                    result = backward_reasoning(subquery, premises, knowledge_base)
                    results.append(result)
                if all(results):
                    return True
    return False

if __name__ == "__main__":
    file_path = 'KBEngland.pl'
    premises = load_knowledge_base(file_path)
    query = "nephew(james_viscount_serven,prince_charles)"

    result = backward_reasoning(query, premises, premises)
    if result:
        print("The query is true.")
    else:
        print("The query is false.")
