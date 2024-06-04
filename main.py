"""

compiler term project SLR parser implementation 


"""

# thinking... -------------------------------------------

#recap on how the SLR implementation is supposed to work:
 
#1. check whether a left substring is a viable prefix or not 

#2. make a decision 

# 인풋 스트링은 파일 형식으로 주어진다. 
# 인풋 스트링 스플리터 - 인풋 스트링을 split(), token을 나누고 이걸 리스트에 저장. 스플리터 위치는 
# 인덱싱으로 표현. 
 
#LR parsing 프로그램은 스택 메모리, 인풋, 그리고 action으로 나눌 수 있다. 

#파싱 테이블 lookup 방법 생각하면서 설계. 

# 구현 방법----------------------------------------------------

#스테이트 -  production rules 

#스택 메모리 attributes:
# current state

#인풋 (리스트) attributes: 
#splitter position? 
#next input symbol. 


#initialization:

# push the start state into the stack. 

#program process : 

#1 : LOOKUP parsing table with current state and next input symbol data.
#Current state from stack memory, symbol data from the input string data. 

#2 : if table_entry ==  S(state_num) , 
#      push state_num into the stack, move the splitter to the right (인풋 스트링 데이터)
#
#    if table entry == R(state_num) , 
#       reduce by state_num prod. state_num에 해당되는 production rule을 찾고, reduce 한다. 
#       스택에서 reduction production rule의 RHS의 길이만큼 pop한다. 
#       table lookup,  GOTO(current_state) 를 스택에 푸쉬한다. 
#
#accept action에 도달하면 accept output. reject 되는 경우는? 인풋 스트링을 다 읽었는데 할게 없다거나
#실행 가능한 action이 없으면 reject. 

import sys 
import csv 


#SLR parsing table을 어떻게 구현할까...
#일단 파싱 테이블이 큰거는 쩔수인듯. 이걸 csv 파일로 읽어올까?
#스크립트 내에서 일일이 다 입력하는 건 너무... 힘들어.

#인풋 스트링을 읽는 함수.
def read_input_file(file_path):
    try: 
        with open(file_path,'r') as file: 
            input_file_content  = file.read()
            return input_file_content
        
    except FileNotFoundError:
        print(f"{file_path} 파일을 찾지 못했습니다.")
    except Exception as e: 
        print(f"오류가 발생했습니다:{e}")


#파싱 table lookup 함수. 
def look_up_parsing_table(parsing_table,stack,input_string,splitter_pos):
    pass
             


#cmd 창에서 스크립트 실행 형식이 맞지 않을 때 error handling. 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python read_file.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    #스택 메모리 
    stack = []

    #인풋 스트링을 읽어온다 
    input_string = read_input_file(filename)
    
    
    #인풋 스트링을 토큰 단위로 나눈다. 
    input_string_list = input_string.strip().split(' ')

    #인풋 스트링의 symbol 개수와 스플리터 위치를 저장하는 변수.
    len_input_string_list = len(input_string_list)
    splitter_pos = 0 
    
    
    #파싱 테이블에서
    #무슨 터미널과 non-터미널이 있는지 저장.
    #테이블 entry action 은 next symbol과 state을 key로 하는 dictionary 형태로 저장.
    terminal_n_non_terminal = []
    table_entry_dict = {}
    

    #파싱 테이블을 가져온다 
    with open('parsing table.csv','rt',encoding= 'UTF8') as file: 
        csvFile = csv.reader(file)
        for i,line in enumerate(csvFile):

            #terminal과 non-terminal row 읽어오기  
            if i == 0:
                for j,entry in enumerate(line):
                    #[0,0] 자리에 있는 entry는 NONE이기 때문에 스킵한다. 
                    if j != 0 :
                        terminal_n_non_terminal.append(entry)
            else: 
                #그 이후로 오는 row 데이터는 dictionary에 저장. (state_num,terminal_n_non_terminal) : action 형태로. 
                for j,entry in enumerate(line):
                    
                    if j != 0 and entry != "":
                        table_entry_dict[(i-1,terminal_n_non_terminal[j-1])] = entry
                
    print(table_entry_dict)
        
                 
        
    #initialization: 스택에 초기 state를 푸쉬.
    stack.append('0')

    
    #program process: 
    """
    while splitter_pos <= len_input_string_list:
        pass
    """