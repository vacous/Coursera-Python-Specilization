# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 22:44:11 2016

@author: Administrator
"""

"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster

# conditional imports
if DESKTOP:
    import alg_project3_solution     # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
TABLE_URL_LIST = [DATA_111_URL, DATA_290_URL, DATA_896_URL, DATA_3108_URL]

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results

# distortion helper function 
def distortion(list1,data_table):
    '''
    list1 contains one list of clusters 
    data table is can provide the individual x and y for a county
    '''
    output_distortion = 0
    for cluster in list1:
        temp_error = cluster.cluster_error(data_table)
        output_distortion += temp_error
#        print temp_error
    return output_distortion 


def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_111_URL)
    
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
        
#    cluster_list = sequential_clustering(singleton_list, 15)	
#    print "Displaying", len(cluster_list), "sequential clusters"

    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
#    print "Displaying", len(cluster_list), "hierarchical clusters"

#    cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)	
#    print "Displaying", len(cluster_list), "k-means clusters"
            
    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        pass
#        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
#        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        pass
#        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers
    return distortion(cluster_list,data_table)
    
TABLE_URL_LIST = [DATA_111_URL, DATA_290_URL, DATA_896_URL]#, DATA_3108_URL]
def cluster_compare(cluster_range, num_iter, data_url_list):
    '''
    compare the performace between kmean and hcluster
    distortion as the metric 
    '''
    kmean_result = {}
    heir_result = {}
    for url in data_url_list:
        kmean_result[url] = {}
        heir_result[url] = {}
    print kmean_result     
    for table_url in data_url_list:
        for cluster_num in range(cluster_range[0],cluster_range[1]+1):
            data_table = load_data_table(table_url)
            singleton_list = []
            for line in data_table:
                singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
            # calculate the distortion
            list_kmean = alg_project3_solution.kmeans_clustering(singleton_list, cluster_num, num_iter)
            list_heir = alg_project3_solution.hierarchical_clustering(singleton_list, cluster_num)
            kmean_result[table_url][cluster_num] = distortion(list_kmean, data_table)
            heir_result[table_url][cluster_num] = distortion(list_heir, data_table)
    return [kmean_result, heir_result] 

print cluster_compare([6,20], 5, TABLE_URL_LIST)



    





  
        






        




