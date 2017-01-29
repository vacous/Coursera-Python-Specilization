# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 10:02:29 2016

@author: Administrator
"""
from collections import deque

# helper function 
def neighbors(node,edges):
    output = []    
    for ele in edges:
        if node in ele:
            ele_copy = ele.copy()
            ele_copy.remove(node)
            output.extend(list(ele_copy))
    return output 
def format_convert(ungraph):
    nodes = set([ele for ele in ungraph])
    edges = []
    for node in ungraph:
        for ele in ungraph[node]:
            edges.append(set([node,ele]))
    return [nodes,edges]        
# test case     
#graph = { 0 : set([1]),
#          1 : set([0, 2]),
#          2 : set([1]) }
#graph = format_convert(graph)     
#print graph    
# test case
#a = [set([1,2]),set([1,2]),set([2,4]),set([5,2])]
#n = 2 
#print neighbors(2,a)    
#print [ele for ele in a]
# Main functions 
def bfs_visited(ungraph, start_node):
    '''
    takes undirected graph and the start node, returns all nodes visited by BFS
    '''
    ungraph = format_convert(ungraph)
    visited = set()
    edges = list(ungraph[1])
    q = deque()
    visited.add(start_node)
    q.append(start_node)
    while q != deque():
        node1 = q[0]
        q.popleft()
        for node in neighbors(node1,edges):
            if node not in visited:
                visited.add(node)
                q.append(node)
    return visited                 
#a = [set([1,2,3,4,5,6]),[set([1,2]),set([1,3]),set([1,4]),set([3,4]),set([5,6])]]    
#print bfs_visited(a,1)        
def cc_visited(ungraph):
    '''
    takes a ungraph and returns all the connected components 
    '''
    ungraph_copy = dict(ungraph)
    ungraph = format_convert(ungraph)
#    print ungraph
    remain = ungraph[0].copy()
    cc = []
    while remain != set():
        i = list(remain)[0]
        w = set(bfs_visited(ungraph_copy,i))
        cc.append(w)
        remain.difference_update(w)
    return cc         
    
def largest_cc_size(ungraph):
    '''
    takes a ungraph and returns the size of the largest component in ungraph
    '''
    size = -1
    for ele in cc_visited(ungraph):
        if len(ele) >= size :
            size = len(ele)
    return size
       
def compute_resilience(ungraph,attack_order):
    '''
    takes a ungraph, a list of nodes attack_order, and returns largest cc size after attack
    '''
    size = [largest_cc_size(ungraph)]
    ungraph_copy = dict(ungraph)
    for na in attack_order:
        ungraph_copy.pop(na)
        for ele in ungraph_copy:
            if na in ungraph_copy[ele]:
                ungraph_copy[ele].remove(na)
        size.append(largest_cc_size(ungraph_copy))
    return size     
           
        
## test case 
GRAPH3 = {0: set([1, 2]),
          1: set([0]),
          2: set([0, 3]),
          3: set([2]),
          4: set([5]),
          5: set([4])  }
#print bfs_visited(GRAPH3,1)     
print compute_resilience(GRAPH3, [0,1,4])  