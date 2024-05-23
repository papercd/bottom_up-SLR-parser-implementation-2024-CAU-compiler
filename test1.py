# non-ambiguous CFG

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

# read file
input_file = 'C:/Users/shlee/Desktop/compiler/inputfile.txt'
with open(input_file, 'r', encoding='utf-8') as file:
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

        print("slr_table['action'][state] : ", slr_table['action'][state])
        if token not in slr_table['action'][state]: # 현재 읽은 토큰이 slr table action에 없을 경우
            print(f"Syntax error at token {token}")
            return False
        
        action = slr_table['action'][state][token]
        print("action: ", action)

        if action[0] == 's':  # Shift
            stack.append(token)
            stack.append(int(action[1:])) # Stack에 state 넣기
            print("stack: ", stack)
            index += 1

        elif action[0] == 'r':  # Reduce
            production = grammar[int(action[1:])]
            print("prodection: ", production)
            lhs, rhs = production
            
            for _ in rhs:
                stack.pop()
                stack.pop()
                print("stack: ", stack)
            goto_state = slr_table['goto'][stack[-1]][lhs]
            stack.append(lhs)
            stack.append(goto_state)

        elif action == 'acc':  # Accept action
            print("Input accepted.")
            return True

        else:
            print(f"Unexpected action {action}")
            return False

parse(tokens)

