import sys 
import csv 


# Define grammar
new_grammar = {
    0: ("CODE'", ["CODE"]),
1: ("CODE", ["VDECL", "CODE"]),
2: ("CODE", ["FDECL", "CODE"]),
3: ("CODE", [""]),
4: ("VDECL", ["vtype", "id", "semi"]),
5: ("VDECL", ["vtype", "ASSIGN", "semi"]),
6: ("ASSIGN", ["id", "assign", "RHS"]),
7: ("RHS", ["EXPR"]),
8: ("RHS", ["literal"]),
9: ("RHS", ["character"]),
10: ("RHS", ["boolstr"]),
11: ("EXPR", ["EXPR", "addsub", "TERM"]),
12: ("EXPR", ["TERM"]),
13: ("TERM", ["TERM", "multdiv", "FACTOR"]),
14: ("TERM", ["FACTOR"]),
15: ("FACTOR", ["lparen", "EXPR", "rparen"]),
16: ("FACTOR", ["id"]),
17: ("FACTOR", ["num"]),
18: ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),
19: ("ARG", ["vtype", "id", "MOREARGS"]),
20: ("ARG", [""]),
21: ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]),
22: ("MOREARGS", [""]),
23: ("BLOCK", ["STMT", "BLOCK"]),
24: ("BLOCK", [""]),
25: ("STMT", ["VDECL"]),
26: ("STMT", ["ASSIGN", "semi"]),
27: ("STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE"]),
28: ("STMT", ["while", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"]),
29: ("COND", ["boolstr", "COND'"]),
30: ("COND'", ["comp", "boolstr", "COND'"]),
31: ("COND'", [""]),
32: ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
33: ("ELSE", [""]),
34: ("RETURN", ["return", "RHS", "semi"]),
}



def create_parsing_table(filename):

    # Read the parsing table from CSV
    # Initialize SLR table
    slr_table = {
        'action': {},
        'goto': {}
    }

    labels = []
    action_index = 0
    #goto_index = 0
    with open(filename, 'rt', encoding='UTF8') as file:
        csvFile = csv.reader(file)
        for i, line in enumerate(csvFile):
            if i == 0:
                #goto_index = len(line) - 1
                for j, entry in enumerate(line):
                    if j != 0:
                        if entry == "$":
                            action_index = j
                        labels.append(entry)
            else:
                state = i - 1
                slr_table['action'][state] = {}
                slr_table['goto'][state] = {}
                for j, entry in enumerate(line):
                    if j != 0 and entry != "":
                        if j <= action_index:
                            slr_table['action'][state][labels[j-1]] = entry
                        else:
                            slr_table['goto'][state][labels[j-1]] = int(entry)
        return slr_table
    

class ParseTreeNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

def print_parse_tree(root_node, indent= [0], is_last_child=False):
    if root_node is None:
        return

    
    for el in indent: 
        if el == 0:
            print("    " , end="")    
        else:
            print("│   " , end="")

    if is_last_child:
        print("└── ", end="")
       
    else:
        print("├── ", end="")
    print(root_node.node_type)

    
    num_children = len(root_node.children) 
    for i, child in enumerate(root_node.children):
        is_last = i == num_children - 1
        if not is_last_child:
            indent.append(1)
        else:
            indent.append(0)
        print_parse_tree(child, indent , is_last)
        indent.pop()


def read_input_file(file_path):
    try: 
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().split()
            return tokens
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾지 못했습니다.")
    except Exception as e: 
        print(f"오류가 발생했습니다:{e}")

def print_stack(stack):
    print("stack: [", end="")
    length = len(stack)
    for i, element in enumerate(stack): 
        print(element[1].node_type, ",", element[0], end= '' if i == length-1 else ',')
    print("]")

def parse_with_error_reporting(tokens,slr_table):
    stack = [(0, ParseTreeNode("CODE"))]  # Stack contains state and parse tree node
    index = 0  # Token index
    error_message = None

    while stack:
        print()
        state, tree_node = stack[-1]
        print("state: ", state)
        token = tokens[index] if index < len(tokens) else '$'
        print("token: ", token)
        print("slr_table['action'][state] : ", slr_table['action'][state])

        if token not in slr_table['action'][state]:

            # Syntax error detected
            # if the table entry for the token and current state read does not exist, 
            # then that means there exists a syntax error within the input token sequence.

            expected_tokens = list(slr_table['action'][state].keys())
            error_message = f"Syntax error at token '{token}'. Expected one of: {', '.join(expected_tokens)}"
            break

        action = slr_table['action'][state][token]
        print("action: ", action)

        if action[0] == 's':  # Shift
            next_state = int(action[1:])
            new_tree_node = ParseTreeNode(token)
            stack.append((next_state, new_tree_node))
            index += 1
            print_stack(stack)

        elif action[0] == 'r':  # Reduce
            production = new_grammar[int(action[1:])]
            print("production: ", production)
            lhs, rhs = production
            new_tree_node = ParseTreeNode(lhs)
            for _ in rhs:
                if _ != "":
                    
                    _, child_node = stack.pop()
                    new_tree_node.children.insert(0, child_node)
                   
          
            
            next_state = slr_table['goto'][stack[-1][0]][lhs]
            stack.append((next_state, new_tree_node))
            print_stack(stack)

        elif action == 'acc':  # Accept action
            print("Input accepted.")
            return tree_node, None

        else:
            error_message = f"Unexpected action '{action}'"
            break

    # Error occurred, construct error report
    error_report = {
        'message': error_message,
        'token_position': index,
        'token': token,
        'expected_tokens': expected_tokens if expected_tokens else [],
        'context': tokens[max(0, index - 5):index + 5]  # Extract some context around the error
    }

    return None, error_report




if __name__ == "__main__":
    if len(sys.argv) != 2:

        print("Usage: python read_file.py <filename>")
        sys.exit(1)

    token_filename = sys.argv[1]
    tokens = read_input_file(token_filename)
    slr_parsing_table = create_parsing_table("parsing_table.csv")

    parse_tree_root, error_report = parse_with_error_reporting(tokens,slr_parsing_table)

    if error_report:
        print("\nError occurred -----------------------",end='\n\n')
        msg_length = len(error_report["message"])
        print("Parsing error " + "="*msg_length)
        print(error_report['message'])
        print("=" * (14+msg_length))
        print("Token Read:", error_report['token'])
        print("Expected tokens:", error_report['expected_tokens'])
        print("Error occured at:", error_report['context'])
    else:
        print("")
        print("-------------------------- Parse Tree ---------------------------------")
        print("    CODE'")
        print_parse_tree(parse_tree_root,is_last_child=True)