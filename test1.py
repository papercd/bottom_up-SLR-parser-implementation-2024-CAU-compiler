# non-ambiguous CFG
import sys
import csv 

"""
grammar = {
    0: ("CODE", ["VDECL", "CODE"]),
    1: ("CODE", ["FDECL", "CODE"]),
    2: ("CODE", [""]),
    
    3: ("VDECL", ["vtype", "id", "semi"]),
    4: ("VDECL", ["vtype", "ASSIGN", "semi"]),

    5: ("ASSIGN", ["id", "assign", "RHS"]),

    6: ("RHS", ["EXPR", "literal", "character", "boolstr"]),
    7: ("EXPR", ["EXPR", "addsub", "TERM"]), 
    8: ("EXPR", ["TERM"]),

    9: ("EXPR'", ["addsub", "TERM", "EXPR"]), 
    10: ("EXPR'", [""]),

    11: ("TERM", ["FACTOR","TERM'"]),

    12: ("TERM'", ["multdiv", "FACTOR", "TERM"]),
    13: ("TERM'", [""]),

    14: ("FACTOR", ["lparen","EXPR","rparen"]), 
    15: ("FACTOR", ["id"]),
    16: ("FACTOR", ["num"]),

    17: ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),

    18: ("ARG", ["vtype", "id", "MOREARGS"]),
    19: ("ARG", [""]),

    20: ("MOREARGS", ["comma", "vtype", "id", "MOREARGS"]), 
    21: ("MOREARGS", [""]),

    22: ("STMT", ["VDECL"]), 
    23: ("STMT", ["ASSIGN","semi"]), 
    24: ("STMT", [ "IF_STMT"]),

    25: ("IF_STMT", ["if","lparen", "COND","rparen", "lbrace", "BLOCK", "rbrace", "ELSE"]), 
    26: ("IF_STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"]),
    
    27: ("ELSE", ["else", "lbrace", "BLOCK", "rbrace"]),
    28: ("ELSE", [""]),

    29: ("BLOCK", ["STMT","BLOCK"]), 
    30: ("BLOCK", [""]),

    31: ("COND", ["boolstr", "COND'"]),

    32: ("COND'", ["comp", "boolstr", "COND'"]), 
    33: ("COND'", [""]),
    
    34: ("RETURN", ["return", "RHS", "semi"])
}
"""

new_grammar = {
0: ("CODE", ["CODE_BLOCK"]),
1: ("CODE", [""]),

2: ("CODE_BLOCK", ["VDECL", "CODE_BLOCK"]),
3: ("CODE_BLOCK", ["FDECL", "CODE_BLOCK"]),
4: ("CODE_BLOCK", ["STMT", "CODE_BLOCK"]),

5: ("VDECL", ["vtype", "id", "vdecl_tail", "semi"]),

6: ("vdecl_tail", [""]),
7: ("vdecl_tail", ["ASSIGN"]),

8: ("ASSIGN", ["id", "assign", "RHS"]),

9: ("RHS", ["EXPR"]),
10: ("RHS", ["literal"]),
11: ("RHS", ["character"]),
12: ("RHS", ["boolstr"]),

13: ("EXPR", ["EXPR", "addsub", "TERM"]),
14: ("EXPR", ["TERM"]),

15: ("TERM", ["TERM", "multdiv", "FACTOR"]),
16: ("TERM", ["FACTOR"]),

17: ("FACTOR", ["lparen", "EXPR", "rparen"]),
18: ("FACTOR", ["id"]),
19: ("FACTOR", ["num"]),

20: ("FDECL", ["vtype", "id", "lparen", "ARG", "rparen", "lbrace", "BLOCK", "RETURN", "rbrace"]),

21: ("ARG", ["ARG_LIST"]),
22: ("ARG", [""]),

23: ("ARG_LIST", ["vtype", "id"]),
24: ("ARG_LIST", ["vtype", "id", "comma", "ARG_LIST"]),

25: ("BLOCK", ["STMT", "BLOCK"]),
26: ("BLOCK", []),

27: ("STMT", ["VDECL", "semi"]),
28: ("STMT", ["ASSIGN", "semi"]),
29: ("STMT", ["IF_STMT"]),
30: ("STMT", ["WHILE_STMT"]),

31: ("IF_STMT", ["if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE_STMT"]),

32: ("ELSE_STMT", ["else", "if", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace", "ELSE_STMT"]),
33: ("ELSE_STMT", ["else", "lbrace", "BLOCK", "rbrace"]),

34: ("WHILE_STMT", ["while", "lparen", "COND", "rparen", "lbrace", "BLOCK", "rbrace"]),

35: ("COND", ["EXPR", "comp", "EXPR"]),
36: ("COND", ["boolstr"]),

37: ("RETURN", ["return", "RHS", "semi"]),

}

"""
#SLR parsing table 
slr_table = {
    'action': {
        0: {'vtype': 's2'},
        1: {'vtype': 's5', '$' : 'r2'},
        2: {'id' : 's6'},
        3: {'$': 'acc'},
        4: {'vtype' : 's5', '$' : 'r2'},
        5: {'id' : 's9'},
        6: {'semi' : 's10', 'assign' : 's11'},
        7: {'semi' : 's12'},
        8: {'$' : 'r1'},
        9: {'semi' : 's10', 'assign' : 's11', 'lparen' : 's13'},
        10: {'vtype' : 'r3', 'id' : 'r3', 'rbrace' : 'r3', 'if' : 'r3', 'return' : 'r3', '$' : 'r3'},        
        11: {'id' : 's22', 'literal' : 's16', 'character' : 's17', 'boolstr' : 's18', 'lparen' : 's21', 'num' : 's23'},
        12: {'vtype' : 'r4', 'id' : 'r4', 'rbrace' : 'r4', 'if' : 'r4', 'return' : 'r4', '$' : 'r4'},
        13: {'vtype' : 's25', 'rparen' : 'r21'},
        14: {'semi' : 'r5'},
        15: {'semi' : 'r6'},
        16: {'semi' : 'r7'},
        17: {'semi' : 'r8'},
        18: {'semi' : 'r9'},
        19: {'semi' : 'r12', 'addsub' : 's27', 'rparen' : 'r12'}
    },
    'goto': {
        0: {'VDECL': 1}, 
        1: {'CODE': 3, 'VDECL' : 1, 'FDECL' : 4},
        2: {'ASSIGN' : 7},
        4: {'CODE': 8, 'VDECL' : 1, 'FDECL' : 4},
        5: {'ASSIGN' : 7},
        6: {},
        7: {},
        8: {},
        9: {},
        10: [],
        11: {'RHS' : 14, 'EXPR' : 15, 'TERM' : 19, 'FACTOR' : 20},
        12: {},
        13: {'ARG' : 24},
        14: {},
        15: {},
        16: {},
        17: {},
        18: {},
        19: {"EXPR'" : 26},
        20: {"TERM'" : 28},
        21: {'EXPR' : 30, 'TERM' : 19, 'FACTOR' : 20},
        22: {},
        23: {},
        24: {},
        25: {},
        26: {},
        27: {'TERM' : 33, 'FACTOR' : 20},
        28: {},
        29: {'FACTOR' : 34}
    }
}
"""

action_index = 0 
goto_index = 0
generated_slr_table = {
    'action' : {},

    'goto' : {}
}

table_entry_dict= {}
terminal_n_non_terminal = []

#slr table 생성 

with open('parsing table.csv', 'rt', encoding='UTF8') as file:
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


# read file

with open('test.txt', 'r', encoding='utf-8') as file:
    tokens = file.read().split() # 띄어쓰기 단위로 토큰 분리




# parse input tokens

def parse(tokens):
    stack = [0]  # Stack initially contains the start state
    index = 0  # Start from the first token

    while True:
        state = stack[-1]
        print()
        print("state: ", state)
        token = tokens[index] if index < len(tokens) else '$'
        print("token: ", token)

        print("slr_table['action'][state] : ", generated_slr_table['action'][state])
        if token not in generated_slr_table['action'][state]: # 현재 읽은 토큰이 slr table action에 없을 경우
            print(f"Syntax error at token {token}")
            return False
        
        action = generated_slr_table['action'][state][token]
        print("action: ", action)

        if action[0] == 's':  # Shift
            stack.append(token)
            stack.append(int(action[1:])) # Stack에 state 넣기
            print("stack: ", stack)
            index += 1

        elif action[0] == 'r':  # Reduce
            production = new_grammar[int(action[1:])]
            print("production: ", production)
            lhs, rhs = production
            
            #empty string 이 아니면 pop하는 걸로 수정. 

            for _ in rhs:
                if _ != "":
                    stack.pop()
                    stack.pop()
                    print("stack: ", stack)
            goto_state = generated_slr_table['goto'][stack[-1]][lhs]
            stack.append(lhs)
            stack.append(goto_state)
            print("stack: ", stack)

        elif action == 'acc':  # Accept action
            print("Input accepted.")
            return True

        else:
            print(f"Unexpected action {action}")
            return False
        




"""



            
class ParseTreeNode:
    def __init__(self, node_type, value=None):
        self.node_type = node_type
        self.value = value
        self.children = []

def parse_with_tree(tokens):
    stack = [(0, ParseTreeNode("CODE"))]  # Stack contains state and parse tree node
    index = 0  # Token index

    while stack:
        state, tree_node = stack[-1]
        print()
        print("state: ", state)
        token = tokens[index] if index < len(tokens) else '$'
        print("token: ", token)

        if token not in generated_slr_table['action'][state]:
            print(f"Syntax error at token {token}")
            return None

        action = generated_slr_table['action'][state][token]

        if action[0] == 's':  # Shift
            next_state = int(action[1:])
            new_tree_node = ParseTreeNode(token)
            stack.append((next_state, new_tree_node))
            index += 1
            print("stack: ", stack)

        elif action[0] == 'r':  # Reduce
            production = new_grammar[int(action[1:])]
            print("production: ", production)
            lhs, rhs = production
            new_tree_node = ParseTreeNode(lhs)
            for _ in rhs:
                if _ != "":
                    stack.pop()  # Pop states and tree nodes for the right-hand side symbols
                    _, child_node = stack.pop()
                    new_tree_node.children.insert(0, child_node)  # Insert children in reverse order
                    print("stack: ", stack)
            # Consult the goto table to find the next state
            next_state = generated_slr_table['goto'][stack[-1][0]][lhs]
            stack.append((next_state, new_tree_node))
            print("stack: ", stack)

        elif action == 'acc':  # Accept action
            print("Input accepted.")
            return tree_node

        else:
            print(f"Unexpected action {action}")
            return None
"""
# Usage

#parse_tree_root = parse_with_tree(tokens)


parse(tokens)

