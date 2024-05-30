

import sys 
import csv 

new_grammar = {
    0: ("CODE", ["VDECL", "CODE"]),
    1: ("CODE", ["FDECL", "CODE"]),
    2: ("CODE", [""]),
    
    3: ("VDECL", ["vtype", "id", "semi"]),
    4: ("VDECL", ["vtype", "ASSIGN", "semi"]),
    
    5: ("ASSIGN", ["id", "assign", "RHS"]),
    
    6: ("RHS", ["EXPR"]),
    7: ("RHS", ["literal"]),
    8: ("RHS", ["character"]),
    9: ("RHS", ["boolstr"]),
    
    10: ("EXPR", ["EXPR", "addsub", "TERM"]),
    11: ("EXPR", ["TERM"]),
    
    12: ("TERM", ["TERM", "multdiv", "FACTOR"]),
    13: ("TERM", ["FACTOR"]),
    
    14: ("FACTOR", ["lparen", "EXPR", "rparen"]),
    15: ("FACTOR", ["id"]),
    16: ("FACTOR", ["num"]),
    
    17: ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),
    
    18: ("ARG", ["vtype", "id", "MOREARGS"]),
    19: ("ARG", [""]),
    
    20: ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]),
    21: ("MOREARGS", [""]),
    
    22: ("STMT", ["VDECL"]),
    23: ("STMT", ["ASSIGN", "semi"]),
    24: ("STMT", ["IF_STMT"]),
    
    25: ("IF_STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE"]),
    
    26: ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
    27: ("ELSE", [""]),
    
    28: ("BLOCK", ["STMT", "BLOCK"]),
    29: ("BLOCK", [""]),
    
    30: ("COND", ["boolstr", "COND'"]),
    
    31: ("COND'", ["comp", "boolstr", "COND'"]),
    32: ("COND'", [""]),
    
    33: ("RETURN", ["return", "RHS", "semi"]),
}


action_index = 0 
goto_index = 0

generated_slr_table = {
    'action' : {},
    'goto' : {}
}

table_entry_dict= {}
terminal_n_non_terminal = []

#slr table 생성 

with open('new_parsing_table.csv', 'rt', encoding='UTF8') as file:
    csvFile = csv.reader(file)
    for i, line in enumerate(csvFile):
       
       #무슨 non-terminal과 terminal이 있는지 저장. 
        if i == 0:
            goto_index = len(line) - 1
            for j, entry in enumerate(line):
                if j != 0:
                    if entry == "$":
                        action_index = j
                    terminal_n_non_terminal.append(entry)
        else:
            #나머지 줄을 읽으면서 dictionary 채우기. 
            state = i - 1
            generated_slr_table['action'][state] = {}
            generated_slr_table['goto'][state] = {}
            for j, entry in enumerate(line):
                if j != 0 and entry != "":
                    # action
                    if j <= action_index:
                        generated_slr_table['action'][state][terminal_n_non_terminal[j-1]] = entry
                    # goto
                    else:
                        generated_slr_table['goto'][state][terminal_n_non_terminal[j-1]] = int(entry)


def print_parse_tree(root_node, indent=0):
    if root_node is None:
        return

    # Print the current node with appropriate indentation
   
    print("  " * indent + (root_node.node_type if root_node.node_type != None else " ") )

    # Recursively print children with increased indentation
    for child in root_node.children:
    
        print_parse_tree(child, indent + 1)


class ParseTreeNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

#인풋 스트링을 읽는 함수.


def read_input_file(file_path):
    try: 
        with open(file_path, 'r', encoding='utf-8') as file:
            tokens = file.read().split() # 띄어쓰기 단위로 토큰 분리
            
            return tokens
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾지 못했습니다.")
    except Exception as e: 
        print(f"오류가 발생했습니다:{e}")

def print_stack(stack):
    print("stack: [",end="")
    length = len(stack)
    for i,element in enumerate(stack): 
        print( element[1].node_type,",", element[0],end= '' if i == length-1 else ',')
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
                    #stack.pop()  # Pop states and tree nodes for the right-hand side symbols
                    _, child_node = stack.pop()
                    new_tree_node.children.insert(0, child_node)  # Insert children in reverse order
                   
            # Consult the goto table to find the next state
            
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
    print()
    print("error occured-----------------------")
    print("Parsing error:")
    print(error_report['message'])
    print("Token:", error_report['token'])
    print("Expected tokens:", error_report['expected_tokens'])
    print("Context:", error_report['context'])
else:
    print("done")
    print()
    print("parse tree---------------------------------")
    print()
    print_parse_tree(parse_tree_root)
    # Continue with successful parsing


