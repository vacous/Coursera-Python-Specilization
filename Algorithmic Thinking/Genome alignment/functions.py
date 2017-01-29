'''
four helper functions 
'''
import random

## two types of matrices 
# 1. alignment matrices, type: list list 
# 2. scoring matrices, type: dict dict 

def build_scoring_matrix(alph,diag_score,off_diag_score,dash_score):
    '''
    alpha: SET of characters 
    output: a dictionary of dictionaries whose entries are indexed by pairs of chars in alph
    '''
    scoring_matrix = {}
    alph_dash = alph.copy()
    alph_dash.add('-')
    for char in alph_dash:
        scoring_matrix[char] = {}
        for char2 in alph_dash:
            if char == char2 and char != '-':
                scoring_matrix[char][char2] = diag_score
            elif char != char2 and char != '-' and char2 != '-':
                scoring_matrix[char][char2] = off_diag_score
            elif char == char2 and char == '-':
                scoring_matrix[char][char2] = dash_score
            else:
                scoring_matrix[char][char2] = dash_score 
    return scoring_matrix 


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    '''
    takes: seq_x and seq_y which share the same alph using the scoring_matrix 
    returns: alignment matrix for seq_x and seq_y 
    if the global flag is True each entry of the alignment matrix is computed 
    using the method in Question 8 
    else using the method in Question 12 
    '''
    alig_matrix = [ [ None for _ in range( len(seq_y) + 1 ) ] for _ in range( len(seq_x) + 1 )]
    x_len = len(seq_x)
    y_len = len(seq_y)
    alig_matrix[0][0] = 0 
    for idx in range(1,x_len+1):
        score = alig_matrix[idx-1][0] + scoring_matrix[seq_x[idx-1]]['-']
        if global_flag == False and score < 0:        
            alig_matrix[idx][0] = 0
        else:
            alig_matrix[idx][0] = score
    for jdx in range(1,y_len+1):
        score = alig_matrix[0][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]]
        if global_flag == False and score < 0:        
            alig_matrix[0][jdx] = 0
        else:
            alig_matrix[0][jdx] = score
    for idx in range(1,x_len+1):
        for jdx in range(1,y_len+1):
            score = max( alig_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]],
                              alig_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-']
                              ,alig_matrix[idx][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]])  
            if global_flag == False and score < 0:        
                alig_matrix[idx][jdx] = 0
            else:
                alig_matrix[idx][jdx] = score                  
    return alig_matrix 

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    takes the seq_x and seq_y the scoring matrix and alignment_matrix 
    returns the global alignment of x and y 
    '''
    idx = len(seq_x)
    jdx = len(seq_y)
    x_str = ''
    y_str = ''
    while idx != 0 and jdx != 0:
        if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]]:
            x_str = seq_x[idx-1] + x_str
            y_str = seq_y[jdx-1] + y_str
            idx -= 1 
            jdx -= 1 
        else:
            if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-']:
                x_str = seq_x[idx-1] + x_str
                y_str = '-' + y_str
                idx -= 1 
            else:
                x_str = '-' + x_str
                y_str = seq_y[jdx-1] + y_str 
                jdx -= 1 
    while idx != 0:
        x_str = seq_x[idx-1] + x_str
        y_str = '-' + y_str                
        idx -= 1 
    while jdx != 0:
        y_str = seq_y[jdx-1] + y_str
        x_str = '-' + x_str 
        jdx -= 1 
    return (alignment_matrix[-1][-1], x_str, y_str)   


def score_calculate(seq_x, seq_y, scoring_matrix):
    '''
    returns the total score base on the scoring_matrix 
    '''
    score = 0
    for idx in range(len(seq_x)):
        score += scoring_matrix[seq_x[idx]][seq_y[idx]]
    return score

def max_in_alig_matrix(alig_matrix):
    '''
    takes a alig matrix and returns the locations where the max appears 
    in [(value, idx1, jdx1), (value, idx2, jdx2)]
    '''
    score = float('-inf')
    for idx in range(len(alig_matrix)):
        for jdx in range(len(alig_matrix[idx])):
            temp_score = alig_matrix[idx][jdx]
            if temp_score > score:
                score = temp_score
                index = (idx,jdx)
                
    return (score, index)            
                
def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    '''
    find the best local alignment by finding the max alig_matrix cell
    '''
    (score, (idx_limit, jdx_limit)) = max_in_alig_matrix(alignment_matrix)
    alig_cut = []    
    for num_iter in range(idx_limit+1):
        alig_cut.append(alignment_matrix[num_iter][: jdx_limit+1])
#    print alig_cut
    (_, strx, stry) = compute_global_alignment(seq_x[:idx_limit], seq_y[:jdx_limit], scoring_matrix, alig_cut)
    [str_x_result, str_y_result] = take_away_dash(strx,stry,scoring_matrix)
    return (score, str_x_result, str_y_result)



#def all_possible_str(seq_x, seq_y, scoring_matrix, alignment_matrix):
#    '''
#    returns all possible x_str and y_str
#    '''
#    idx_ini = len(seq_x)
#    jdx_ini = len(seq_y)
#    x_str = ''
#    y_str = ''
#    result_pairs = set([((x_str,y_str),idx_ini,jdx_ini)])
#    while max([ min(pair[1:2]) for pair in result_pairs ]) != 0:
##        print len(result_pairs)
##        print max([ min(pair[1:2]) for pair in result_pairs ])
##        print '=========='
#        pairs_copy = result_pairs.copy()
#        replacement = set()
#        for ele in pairs_copy:
#            idx = ele[1]
#            jdx = ele[2]
#            x_str = ele[0][0]
#            y_str = ele[0][1]
#            if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx-1] + scoring_matrix[seq_x[idx-1]][seq_y[jdx-1]]:
#                x_str_1 = seq_x[idx-1] + str(x_str)
#                y_str_1 = seq_y[jdx-1] + str(y_str)
#                idx_copy_1 = int(idx) - 1  
#                jdx_copy_1 = int(jdx) - 1
#                result_1 = ((x_str_1,y_str_1),idx_copy_1,jdx_copy_1)
#                replacement.add( result_1 )
#            if alignment_matrix[idx][jdx] == alignment_matrix[idx-1][jdx] + scoring_matrix[seq_x[idx-1]]['-']:
#                x_str_2 = seq_x[idx-1] + str(x_str)
#                y_str_2 = '-' + str(y_str)
#                idx_copy_2 = int(idx) - 1 
#                jdx_copy_2 = int(jdx)
#                result_2 = ((x_str_2,y_str_2),idx_copy_2,jdx_copy_2)
#                replacement.add( result_2 )
#            if alignment_matrix[idx][jdx] == alignment_matrix[idx][jdx-1] + scoring_matrix['-'][seq_y[jdx-1]]:
#                x_str_3 = '-' + str(x_str)
#                y_str_3 = seq_y[jdx-1] + str(y_str) 
#                idx_copy_3 = int(idx)
#                jdx_copy_3 = int(jdx) - 1 
#                result_3 = ((x_str_3,y_str_3),idx_copy_3,jdx_copy_3)
#                replacement.add( result_3 )
#        if len(replacement) == 0:
#            return result_pairs
#        else:
#            result_pairs = replacement                
#    return result_pairs
    

def take_away_dash(str1,str2,scoring_matrix):
    '''
    take away the front and end dashes 
    '''
    # front 
    if len(str1) == 0 or len(str2) == 0:
        return [str1,str2]
    while scoring_matrix[str1[0]][str2[0]] < 0:
        str1 = str1[1:]
        str2 = str2[1:]
    while scoring_matrix[str1[-1]][str2[-1]] < 0: 
        str1=str1[:-1]
        str2=str2[:-1]
    return [str1,str2] 

#def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
#    '''
#    takes the seq_x and seq_y the scoring matrix and alignment_matrix 
#    returns the global alignment of x and y 
#    '''
#    str_pairs = all_possible_str(seq_x, seq_y, scoring_matrix, alignment_matrix)
#    score = 0
#    x_result = ''
#    y_result = ''
#    for pair in str_pairs:
#        [str_x,str_y] = take_away_dash(pair[0][0],pair[0][1],scoring_matrix)
#        temp_score = score_calculate(str_x, str_y, scoring_matrix) 
#        if temp_score > score:
#            score = temp_score
#            x_result = str_x
#            y_result = str_y
#    return (score, x_result, y_result)    

#str1 = 'abcd'
#str2 = 'efabcdcdgh'
#scoring_test = build_scoring_matrix(set(['a','b','c','d','e','f','g','h']),4,1,-1)
#ali_test = compute_alignment_matrix(str1, str2, scoring_test, False)
#for ele in ali_test:
#    print ele
#global_best = compute_global_alignment(str1, str2, scoring_test, ali_test)
#print global_best 
#local_best = compute_local_alignment(str1, str2, scoring_test, ali_test)
#print local_best 
#trial_local = compute_local_alignment_global(str1, str2, scoring_test, ali_test)
#print trial_local

def shuffle_str(str1):
    '''
    randomly shuffle a str 
    '''
    str_list = [char for char in str1]
    random.shuffle(str_list)
    output_str = ''
    for char in str_list:
        output_str += char 
    return output_str
