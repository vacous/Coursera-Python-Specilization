import urllib2
import matplotlib.pyplot as plt
import random 

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
        distribution[ele] = temp_count/float(len(digraph))
    return distribution
   
## Question 1    
#result = in_degree_distribution(citation_graph)
#print result 
#
#x = sorted(result.keys())[1:]
#y = [result[k] for k in x]
#plt.yscale('log') # set the x and y scale 
#plt.xscale('log')
#plt.scatter(x,y)
#plt.title('In degree distribution in loglog')
#plt.xlabel('citataions')
#plt.ylabel('normailzed distribution')
## to save the figure 
#fig = plt.gcf() # get the current figure 
#fig.savefig('good.png', dpi = 200)
## save the fig with defined dpi 
#plt.show()
   
# Question 2
# To save memory digraph list insted of set is used 
# all 3 major function are reconstructed 
def er_alg(nodes,prob_cut):
    digraph_list = []
    for ele_1 in nodes:
        nodes_copy = list(nodes)
        nodes_copy.remove(ele_1)
        add_value = [ele_1]
        for ele_2 in nodes_copy:
            prob_rand = random.random()
            if prob_rand < prob_cut:
                add_value.append(ele_2)
        digraph_list.append(add_value)
    return digraph_list

def er_in_degree(list1):
    nodes = []
    in_list = []
    output = []
    for ele in list1:
        nodes.append(ele[0])
        in_list += ele[1:]
    for node in nodes:
        times = in_list.count(node)
        result = [node,times]
        output.append(result)
    return output
        
def er_distribution(list1):
    distribution = {}
    times_list = [ele[1] for ele in list1]
    for ele in times_list:
        temp_count = times_list.count(ele)
        distribution[ele] = temp_count/float(len(list1))
    return distribution  
    
#citation_nodes = range(2000) 
#digraph_list = er_alg(citation_nodes,0.15)
#in_degree_list = er_in_degree(digraph_list)
#result = er_distribution(in_degree_list)
#
#x = sorted(result.keys())[1:]
#y = [result[k] for k in x]
#plt.yscale('log') # set the x and y scale 
#plt.xscale('log')
#plt.scatter(x,y)
#plt.title('In degree distribution in loglog')
#plt.xlabel('citataions')
#plt.ylabel('normailzed distribution')
## to save the figure 
#fig = plt.gcf() # get the current figure 
#fig.savefig('good.png', dpi = 200)
## save the fig with defined dpi 
#plt.show()
    
# Question 4
"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes # num of initial nodes 
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    def generate(self,fin_num_nodes):
        # generate completed graph
        ini_num_nodes = self._num_nodes
        digraph = make_complete_graph(ini_num_nodes)
        # run m times trials from m to n 
        for ele in range(self._num_nodes,fin_num_nodes):
            add_set = self.run_trial(ini_num_nodes)
            digraph[ele] = add_set
        return digraph 

#DPA = DPATrial(13)
#DPAdigraph = DPA.generate(27770)        
#print DPAdigraph
#result = in_degree_distribution(DPAdigraph) 
#print result 
#x = sorted(result.keys())[1:]
#y = [result[k] for k in x]
#plt.yscale('log') # set the x and y scale 
#plt.xscale('log')
#plt.scatter(x,y)
#plt.title('In degree distribution in loglog')
#plt.xlabel('citataions')
#plt.ylabel('normailzed distribution')
## to save the figure 
#fig = plt.gcf() # get the current figure 
#fig.savefig('good.png', dpi = 200)
## save the fig with defined dpi 
#plt.show()
#
#                