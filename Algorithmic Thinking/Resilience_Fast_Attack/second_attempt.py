# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 15:37:57 2016

@author: Administrator
"""

'''
project 4 
'''

from collections import deque



'''
project 4 
'''

# graph converter 
def graph_converter(graph):
    '''
    takes a graph and convert it from a set to a
    list of list 
    [head,[tails]]
    '''
    converted_graph = []
    for ele in graph:
        head = ele
        tails = list(graph[ele])
        converted_graph.append([head,tails])    
    return converted_graph

def find_neighbors(node,graph_list):
    '''
    find the neighbors for a node in a graph_list 
    '''
    output_neighbors = []
    for ele in graph_list:
        if ele[0] == node:
            output_neighbors = ele[1]         
    return output_neighbors 
         

# BFS
def bfs_visited(ungraph, start_node):
    '''
    takes the undirected graph and the node start_node
    and returns the set consisting of all nodes that 
    are visited by a bfs search starts from the start node
    '''
    converted_graph = graph_converter(ungraph)
    visited = set([start_node])
    queue = [start_node]
    while queue != []:
#        print queue
        neighbors = find_neighbors(queue[0],converted_graph)
        for neighbor in neighbors:
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
        queue.pop(0)
    return visited 

# BFS modified
def bfs_modified(converted_graph, start_node):
    '''
    this function is modified the graph after a visit
    '''
#    converted_graph = graph_converter(ungraph)
    visited = set([start_node])
    queue = [start_node]
    while queue != []:
        # add all neighbors to the queue 
        neighbors = list(find_neighbors(queue[0],converted_graph))
        # delete all the nodes that had been added to the queue
        # modify the ungraph_list  
        for neighbor in neighbors:
            queue += [neighbor]
            visited.add(neighbor)
            for ele in converted_graph:
                if neighbor in ele[1]:
                    ele[1].remove(neighbor) 
                elif queue[0] in ele[1]:
                    ele[1].remove(queue[0])    
        queue.pop(0)
    return visited


#test = {0:set([1]),1:set([0,2]),2:set([1,3]),3:set([2]),4:set([])}
#print bfs_modified(graph_converter(test),1)

# CC visited 
def cc_visited(ungraph):
    '''
    takes a ungraph and returns a list of sets 
    each set contains all the nodes in one connected component 
    '''
#    converted_graph = graph_converter(ungraph)
    connected_groups = []
    remain_nodes = set( ungraph.keys() )
    while remain_nodes != set():
        visited = bfs_visited(ungraph, list(remain_nodes)[0])
        connected_groups += [visited]
        remain_nodes.difference_update(visited)
    return connected_groups

def largest_cc_size(ungraph):
    '''
    takes a ungraph and returns the size of the largest component in ungraph
    '''
    size = 0
    for ele in cc_visited(ungraph):
        if len(ele) >= size :
            size = len(ele)
    return size
#print cc_visited(test)
#print bfs_visited(test,1)  

def compute_resilience(ungraph, attack_order):
    '''
    remove nodes in attack_order 
    returns a list of largest_cc_size
    '''
    ungraph_copy = copy_graph(ungraph)
    output_resilience = [ largest_cc_size(ungraph) ]
    for attack_node in attack_order:
        ini_time = time.time()
        head_node_list = ungraph_copy[attack_node]
        ungraph_copy.pop(attack_node)
#        print attack_node
#        print head_node_list
#        print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        for ele in head_node_list:
#            print ele 
#            print ungraph_copy[ele]
            ungraph_copy[ele].discard(attack_node)
        add_size = largest_cc_size(ungraph_copy)    
        output_resilience += [ add_size ]
        time_cost = time.time() - ini_time
        print time_cost 
        print add_size 
        print '================='
    return output_resilience 
        
        
        
        
#################################################################        
"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import random

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


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
    


###############################################################
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

###############################################################
    
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
    
########################################################################
"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""


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
            for each_node in add_set:
                ungraph[each_node].add(ele)
        return ungraph 

#############################################################################
def all_nodes_random(ungraph):
    '''
    takes a ungraph and returns all nodes in random order
    '''
    nodes_order = ungraph.keys()
    random.shuffle(nodes_order)
    return nodes_order

NETWORK_SET = load_graph(NETWORK_URL)
ER_GRAPH = er_graph(range(1239), 0.0039)   
UPA_GRAPH = UPATrial(3).generate(1239)


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


#ER_set = compute_plot_data(ER_GRAPH)
#NETWORK_set = compute_plot_data(NETWORK_SET)
#UPA_set = compute_plot_data(UPA_GRAPH)
#print '====================================='
#print ER_set
#print UPA_set
#print NETWORK_set 


# Question 3 
# fast attack order 
def fast_attack_order(ungraph):
    '''
    create a list degree sets whose kth element is the set of nodes of degree k
    after each attack the list: degree_sets is updated 
    input: a undirected graph
    output: a ordered list L of the nodes in the head nodes in decreasing order of 
    their degree
    '''
    ungraph_copy = copy_graph(ungraph)
    degree_set_len = len(ungraph_copy)
    degree_set = [ set() for _ in range(degree_set_len) ]
    for ele in ungraph_copy:
        degree_ele = len(ungraph_copy[ele])
        degree_set[degree_set_len - degree_ele - 1].add(ele)
    attack_order = []
#    print degree_set
    for max_set in degree_set:
        while max_set != set():
            max_node = max_set.pop()
            neighbors = ungraph_copy[max_node]
            for each_neighbor in neighbors:
                degree_neighbor = len( ungraph_copy[each_neighbor] )
                degree_set[degree_set_len - degree_neighbor - 1].remove(each_neighbor)
                degree_set[degree_set_len - degree_neighbor].add(each_neighbor)
                ungraph_copy[each_neighbor].remove(max_node)
            attack_order.append(max_node)
    return attack_order
    
def running_timer(function_name, input_graph_list):
    '''
    takes a function: either regular attack_order or fast_attack_order
    and a UPA graph with n in range(10,1000,10) and m = 5
    return: the running for each graph
    '''
    attack_order_list = []
    time_list = []
    for each_graph in input_graph_list:
        ini_time = time.time()        
        attack_order_list.append( function_name(each_graph) )
        time_cost = time.time() - ini_time
        time_list.append(time_cost)
    return time_list 

input_graph_list_test = [UPATrial(5).generate( node_num ) for node_num in range(10,1000,2)] 

def attack_time_dataset(time_list, node_range):
    '''
    takes a time_list and a node_range(ie range(10,1000,10) )
    returns dict for plot in codeskulptor
    '''
    output_dataset = {}
    for idx_range in range(len(node_range)):
        output_dataset[ node_range[idx_range] ] = time_list[idx_range]
    return output_dataset    

#time_list_normal = running_timer(targeted_order, input_graph_list_test)      
#time_list_fast = running_timer(fast_attack_order, input_graph_list_test) 

#print attack_time_dataset(time_list_normal, range(10,1000,2) )
#print attack_time_dataset(time_list_fast, range(10,1000,2) )  
      
def compute_plot_data_fast(ungraph):
    '''
    the attack order is randomized 
    '''
    attack_order = fast_attack_order(ungraph)
    resilience = compute_resilience(ungraph,attack_order)
    output_data_set = {}
    num_nodes_attacked = 0 
    for res in resilience:
        output_data_set[num_nodes_attacked] = res 
        num_nodes_attacked += 1 
    return output_data_set     

#print fast_attack_order(NETWORK_SET)  
#print targeted_order(NETWORK_SET)  

#test_graph = {1:set([2,3,4,5]),2:set([1]),3:set([1,6,7]),4:set([1,8]),5:set([1]),6:set([3]),7:set([3]),8:set([4])}
#print targeted_order(test_graph)    
#print fast_attack_order(test_graph)
ER_set = compute_plot_data_fast(ER_GRAPH)
print 'ok'
NETWORK_set = compute_plot_data_fast(NETWORK_SET)
print 'ok'
UPA_set = compute_plot_data_fast(UPA_GRAPH)
print 'ok'
print '====================================='
print ER_set
print UPA_set
print NETWORK_set       
#      
