import urllib2
import matplotlib.pyplot as plt

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

citation_graph = load_graph(CITATION_URL)


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
        distribution[ele] = float(temp_count/len(digraph))
    return distribution
    
distribution = in_degree_distribution(citation_graph)
print distribution