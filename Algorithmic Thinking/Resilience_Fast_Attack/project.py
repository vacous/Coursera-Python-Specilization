# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 23:22:07 2016

@author: Administrator
"""

"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt
###########################################
# codes from application section
from collections import deque

# helper function 
def neighbors(node,edges):
    '''
    find neighbors
    '''
    output = []    
    for ele in edges:
        if node in ele:
            ele_copy = ele.copy()
            ele_copy.remove(node)
            output.extend(list(ele_copy))
    return output 
    
def format_convert(ungraph):
    '''
    convert input format
    '''
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
    queue = deque()
    visited.add(start_node)
    queue.append(start_node)
    while queue != deque():
        node1 = queue[0]
        queue.popleft()
        for node in neighbors(node1,edges):
            if node not in visited:
                visited.add(node)
                queue.append(node)
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
    connect = []
    while remain != set():
        node_start = list(remain)[0]
        group = set(bfs_visited(ungraph_copy,node_start))
        connect.append(group)
        remain.difference_update(group)
    return connect         
    
       
def compute_resilience(ungraph,attack_order):
    '''
    takes a ungraph, a list of nodes attack_order, and returns largest cc size after attack
    '''
    size = [largest_cc_size(ungraph)]
    ungraph_copy = dict(ungraph)
#    print attack_order
    for node_attack in attack_order:
        ungraph_copy.pop(node_attack)
        for ele in ungraph_copy:
            if node_attack in ungraph_copy[ele]:
                ungraph_copy[ele].remove(node_attack)
        size.append(largest_cc_size(ungraph_copy))
    return size     

############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

NETWORK_SET = load_graph(NETWORK_URL)

# prepare 
# ER and UPA
def er_graph(nodes,prob_cut):
    output_ungraph = {}
    for node1 in nodes:
        output_ungraph[node1] = set()
    for node1 in nodes:
        nodes_copy = list(nodes)
        nodes_copy.remove(node1)
        for node2 in nodes_copy:
            prob_rand = random.random()
            if prob_rand < prob_cut:
                output_ungraph[node1].add(node2)
                output_ungraph[node2].add(node1)
    return output_ungraph
# test case 1 
#a = [1,2,3,4]
#print er_graph(a,0.1)     
    
# helper function for UPA
def make_complete_graph(node_num):
    '''
    complete ungraph with given nodes
    '''
    nodes = range(node_num)
    ungraph = {}
    for node1 in nodes:
        nodes_copy = list(nodes)
        nodes_copy.remove(node1)
        ungraph[node1] = set(nodes_copy)
    return ungraph 
# test case 
#a = [1,2,3]
#print make_complete_graph(a)
    
class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    def generate(self,fin_num_nodes):
        ini_num_nodes = self._num_nodes
        ungraph = make_complete_graph(ini_num_nodes)
        # run m times trials from m to n 
        for ele in range(self._num_nodes,fin_num_nodes):
            add_set = self.run_trial(ini_num_nodes)
            ungraph[ele] = add_set
        return ungraph 
        
# test case  
#result_print = []        
#for ele in er_graph(range(1239),0.0020).values():
#    result_print += list(ele)
#print len(result_print)     
# p_cut for  er_graph = 0.0020
#a = UPATrial(3)
#simulate_result = a.generate(1239)
#result_print = []
#for ele in simulate_result.values():
#    result_print += list(ele)
#print len(result_print)
# UPA parms = 3, 1239

def all_nodes_random(ungraph):
    '''
    takes a ungraph and returns all nodes in random order
    '''
    nodes_order = ungraph.keys()
    random.shuffle(nodes_order)
    return nodes_order 
# simulate attacks for original graph,ER_graph and UPA_graph
# NETWORK_SET
ER_GRAPH = er_graph(range(2000),0.1)   
UPA_GRAPH = UPATrial(3).generate(1239)
GRAPHS = [NETWORK_SET, ER_GRAPH, UPA_GRAPH]


def compute_plot_data(ungraph):
    '''
    the attack order is randomized 
    '''
    attack_order = all_nodes_random(ungraph)
    resilience = compute_resilience(ungraph,attack_order)
    output_data_set = {}
    num_nodes_attacked = 0 
    for res in resilience:
        output_data_set[num_nodes_attacked] = res 
        num_nodes_attacked += 1 
    return output_data_set

ER_set = compute_plot_data(ER_GRAPH)


# compute resilience
#resilience = []
#for ungraph in GRAPHS:
#    attack_order = all_nodes_random(ungraph)
#    attack_result = compute_resilience(ungraph,attack_order)
#    resilience.append(attack_result)
#print resilience     
#sim_result = resilience
#

#
#def legend_example():
#    """
#    Plot an example with two curves with legends
#    """
#    xvals = range(1240)
#    yvals1 = sim_result[0]
#    yvals2 = sim_result[1]
#    yvals3 = sim_result[2]
#
#    plt.plot(xvals, yvals1, '-b', label='NETWORK')
#    plt.plot(xvals, yvals2, '-r', label='ER p=0.004')
#    plt.plot(xvals, yvals3, '-g', label='UPA m=3')
#    plt.legend(loc='upper right')
#    plt.xlabel('nodes removed')
#    plt.ylabel('resilience')
#    plt.show()
#
#legend_example()    
#    

# Question 3:
# Fast attack 
#def fast_target_order(ungraph):
#    '''
#    takes a ungraph and find the order that makes most cc attacked
#    '''
#    ungraph_copy = dict(ungraph)
#    nodes = ungraph_copy.keys()
#    degree_set = {}
#    for node in nodes:
#        degree = len(ungraph_copy[node])
#        if degree in degree_set:
#            degree_set[degree].append(node)
#        else:
#            degree_set[degree] = [node]   
#    attack_list = []
#    degree_list = degree_set.keys()
#    for idx in range(max(degree_list)):
#        if idx not in degree_list:
#            degree_set[idx] = []
#    degree_list = sorted(degree_set.keys())        
#    while degree_set != {}:
#        target = degree_list[-1] 
##        print 'target: ' + str(target)
##        print 'degree_set:' + str(degree_set) 
##        print 'degree list: ' + str(degree_list)
#        while degree_set[target] != []:
#            remove_node = degree_set[target][0]
#            attack_list.append(remove_node)
##            print 'ungraph: ' + str(ungraph)        
##            print 'remove node: ' + str(remove_node)
#            for neighbor in ungraph[remove_node]:
#                neighbor_degree = len(ungraph[neighbor])
##                print 'neighbor: ' + str(neighbor)
##                print 'neighbor_degree: ' + str(neighbor_degree)
#                degree_set[neighbor_degree].remove(neighbor)
#                degree_set[neighbor_degree-1].append(neighbor)
#                ungraph[neighbor].remove(remove_node)
#            degree_set[target].pop(0)
#        degree_list.pop()
#        degree_set.pop(target)
##        print '============'    
#    return attack_list   
#duration = []    
#for nodes in range(100,5000,100):    
#    ER_GRAPH = er_graph(range(nodes),0.1)  
#    start_time = time.time()
#    fast_target_order(ER_GRAPH)                      
#    duration += [time.time()-start_time]
#print duration  
#plt.plot(range(100,5000,100), [0.0009999275207519531, 0.002000093460083008, 0.006000041961669922, 0.009000062942504883, 0.016000032424926758, 0.023000001907348633, 0.031000137329101562, 0.046000003814697266, 0.05900001525878906, 0.0709998607635498, 0.0839998722076416, 0.10100007057189941, 0.12100005149841309, 0.14100003242492676, 0.16499996185302734, 0.19000005722045898, 0.21700000762939453, 0.254000186920166, 0.2850000858306885, 0.33500003814697266, 0.36699986457824707, 0.40799999237060547, 0.4440000057220459, 0.4849998950958252, 0.5590000152587891, 0.5950000286102295, 0.6470000743865967, 0.6989998817443848, 0.7639999389648438, 0.8210000991821289, 0.874000072479248, 0.937999963760376, 1.0209999084472656, 1.071000099182129, 1.1370000839233398, 1.2309999465942383, 1.2939999103546143, 1.3629999160766602, 1.4769999980926514, 1.6749999523162842, 1.6579999923706055, 1.749000072479248, 1.8540000915527344, 1.933000087738037, 2.118000030517578, 2.13700008392334, 2.236999988555908, 2.3519999980926514, 2.4640002250671387])
#
#    
#start_time = time.time()           
#print targeted_order(ER_GRAPH)            
#duration = time.time()-start_time
#print duration         
        
                