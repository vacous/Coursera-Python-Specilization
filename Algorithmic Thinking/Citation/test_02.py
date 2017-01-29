# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# define the diagrams
EX_GRAPH0 = {0: set([1,2]), 1: set(), 2: set()}
EX_GRAPH1 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3]), 3: set([0]), 4: set([1]), 5: set([2]),
             6: set()}
EX_GRAPH2 = {0: set([1,4,5]), 1: set([2,6]), 2: set([3,7]), 3: set([7]), 4: set([1]),
             5: set([2]), 6: set(), 7: set([3]), 8: set([1,2]), 9: set([0,4,5,6,7,3])}
#DIAGRAMS = {EX_GRAPH0: DIAGRAM_0, EX_GRAPH1: DIAGRAM_1, EX_GRAPH2: DIAGRAM_2}

# define the functions 
def make_complete_graph(num_ndoes):
    '''
    takes the num of nodes and returns a disctionary corresponding to a complete directed graph
    '''
    # complete node list 
    nodes = range(num_ndoes)
    digraph = {}
    for node in nodes:
        temp_list = list(nodes)
        temp_list.remove(node)
        digraph[node] = set(temp_list)
    return digraph     
    
def compute_in_degrees(digraph):
    '''
    takes a digraph and returns the in-degree for each node
    '''
    in_degree = {}
    appear_time = []
    for ele in digraph:         
        if digraph[ele] != None:
            appear_time += list(digraph[ele])      
    for ele in digraph:
        in_degree[ele] = appear_time.count(ele)
    return in_degree
    
def in_degree_distribution(digraph):
    '''
    takee a digraph and return unnormalized distribution of the in degree
    '''
    in_degree = compute_in_degrees(digraph)
    distribution = {}
    appear_time = []
    for ele in in_degree:
        appear_time.append(in_degree[ele])
    for ele in appear_time:
        temp_count = appear_time.count(ele)
        distribution[ele] = temp_count 
    return distribution
    
print in_degree_distribution(EX_GRAPH2 )    
        
    