import sys 
import csv 


# Define grammar
new_grammar = {
    0: ("S'", ["CODE"]),
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
    11: ("EXPR", ["T_EXPR", "addsub", "EXPR"]),
    12: ("EXPR", ["T_EXPR"]),
    13: ("T_EXPR", ["F_EXPR", "multdiv", "T_EXPR"]),
    14: ("T_EXPR", ["F_EXPR"]),
    15: ("F_EXPR", ["lparen", "EXPR", "rparen"]),
    16: ("F_EXPR", ["id"]),
    17: ("F_EXPR", ["num"]),
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
    29: ("COND", ["boolstr", "COND_T"]),
    30: ("COND_T", ["comp", "boolstr", "COND_T"]),
    31: ("COND_T", [""]),
    32: ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
    33: ("ELSE", [""]),
    34: ("RETURN", ["return", "RHS", "semi"])
}


# Initialize SLR table
generated_slr_table = {
    'action': {},
    'goto': {}
}

terminal_n_non_terminal = []
action_index = 0
goto_index = 0

# Read the parsing table from CSV
with open('parsing table.csv', 'rt', encoding='UTF8') as file:
    csvFile = csv.reader(file)
    for i, line in enumerate(csvFile):
        if i == 0:
            goto_index = len(line) - 1
            for j, entry in enumerate(line):
                if j != 0:
                    if entry == "$":
                        action_index = j
                    terminal_n_non_terminal.append(entry)
        else:
            state = i - 1
            generated_slr_table['action'][state] = {}
            generated_slr_table['goto'][state] = {}
            for j, entry in enumerate(line):
                if j != 0 and entry != "":
                    if j <= action_index:
                        generated_slr_table['action'][state][terminal_n_non_terminal[j-1]] = entry
                    else:
                        generated_slr_table['goto'][state][terminal_n_non_terminal[j-1]] = int(entry)

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

def parse_with_error_reporting(tokens):
    stack = [(0, ParseTreeNode("CODE"))]  # Stack contains state and parse tree node
    index = 0  # Token index
    error_message = None

    while stack:
        print()
        state, tree_node = stack[-1]
        print("state: ", state)
        token = tokens[index] if index < len(tokens) else '$'
        print("token: ", token)
        print("slr_table['action'][state] : ", generated_slr_table['action'][state])

        if token not in generated_slr_table['action'][state]:
            # Syntax error detected
            expected_tokens = list(generated_slr_table['action'][state].keys())
            error_message = f"Syntax error at token '{token}'. Expected one of: {', '.join(expected_tokens)}"
            break

        action = generated_slr_table['action'][state][token]
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
                   
          
            
            next_state = generated_slr_table['goto'][stack[-1][0]][lhs]
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

tokens = read_input_file("test.txt")

parse_tree_root, error_report = parse_with_error_reporting(tokens)
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
    print("    S'")

    print_parse_tree(parse_tree_root,is_last_child=True)
