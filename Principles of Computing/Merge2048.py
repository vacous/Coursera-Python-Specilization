"""
Merge function for 2048 game.
"""


def reshape(line):
    '''
    Reshape the line: 
    For example [2,2,0,2] ==> [2,2,2,0]
    '''
    tail_list = []
    while 0 in line:
        line.remove(0)
        tail_list.append(0)
    
    line.extend(tail_list) 


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result_line = list(line) 
    reshape(result_line)

    temp_index = 0 
    while temp_index + 1 < len(result_line):
        if result_line[temp_index] == result_line[temp_index +1]:
            result_line[temp_index] = 2 * result_line[temp_index]
            result_line[temp_index+1] = 0 
        temp_index += 1         
                
    reshape(result_line)        

    return result_line

