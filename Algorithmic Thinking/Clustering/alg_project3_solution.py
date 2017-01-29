"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster


######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))

def mod_pair_distance(cluster_list, idx1, idx2):
    '''
    modified pair distance to for idx keeping 
    '''
    temp_idx_1 = min(idx1, idx2)
    temp_idx_2 = max(idx1, idx2)
    return (cluster_list[temp_idx_1][0].distance(cluster_list[temp_idx_2][0]),
            min(cluster_list[temp_idx_1][1] ,cluster_list[temp_idx_2][1]),
            max(cluster_list[temp_idx_1][1] ,cluster_list[temp_idx_2][1]))

def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    result = (float('inf'),-1,-1)
    list_len = len(cluster_list)
    for idx_1 in range(list_len):
        for idx_2 in range(idx_1+1,list_len):
            temp_distance = pair_distance(cluster_list,idx_1,idx_2)
            if temp_distance[0] < result[0]:
                result = temp_distance               
    return result 


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    cluster_len = len(cluster_list)
    if cluster_len <= 3:
        result = slow_closest_pair(cluster_list)
    else:   
        mid_idx = cluster_len/2  
        left_part = range(mid_idx)
        right_part = range(mid_idx,cluster_len)
        result_left = fast_closest_pair( [cluster_list[idx] for idx in left_part])
        result_right = fast_closest_pair( [cluster_list[idx] for idx in right_part])
        if result_left[0] > result_right[0]:
            result_one_side = (result_right[0], result_right[1]+mid_idx, result_right[2]+mid_idx) 
        else:
            result_one_side = result_left  
        if cluster_len // 2 == 0:    
            strip_center = 1/2.0 * (cluster_list[mid_idx-1].horiz_center() + cluster_list[mid_idx].horiz_center()) 
        else:
            strip_center = cluster_list[mid_idx].horiz_center()
#        print strip_center, mid_idx, result_one_side
        result_split = closest_pair_strip(cluster_list, strip_center, result_one_side[0]) 
#        print result_split
        if result_one_side[0] < result_split[0]:
            result = result_one_side
        else:
            result = result_split  
    return result


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    sy_list = []
    result = (float('inf'),-1,-1)
    for idx in range(len(cluster_list)):
        horiz_distance = abs(cluster_list[idx].horiz_center() - horiz_center) 
        if horiz_distance < half_width:            
            sy_list.append( (cluster_list[idx], idx) )    
    if sy_list == []:
        return result 
    else:
        sy_list.sort(key = lambda x: x[0].vert_center())  
        sy_len = len(sy_list)
        for idx_1 in range(sy_len - 1):
            idx_start_2 = idx_1 + 1 
            for idx_2 in range(idx_start_2, min(idx_1 + 3, sy_len - 1)+1):            
                temp_dist = mod_pair_distance(sy_list, idx_1, idx_2)
#                print idx_1,idx_2,temp_dist
                if temp_dist[0] < result[0]:
                    result = temp_dist 
        return result 
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    cluster_list.sort(key = lambda x: x.horiz_center())
    dist_list = [ ele.horiz_center() for ele in cluster_list ]
    while len(cluster_list) > num_clusters:
#        print dist_list
        (_, idx_1, idx_2) = fast_closest_pair(cluster_list)
        cluster_list[idx_1].merge_clusters(cluster_list[idx_2])
        new_dist = cluster_list[idx_1].horiz_center()
        cluster_insert = cluster_list[idx_1]
        cluster_list.pop(idx_2)
        cluster_list.pop(idx_1)
        #resort the cluster_list
        dist_list.pop(idx_2)
        dist_list.pop(idx_1)
        pos = 0
        dist_list.append(new_dist)
        while dist_list[pos] < new_dist:
                pos += 1 
        dist_list.pop(-1)                
        cluster_list.insert(pos,cluster_insert)
        dist_list.insert(pos,new_dist)
    return cluster_list


######################################################################
# Code for k-means clustering

def closest_cluster(point, list1):
    '''
    takes a point and a list of cluster 
    returns the cluster that is closest to the point 
    '''
    distance = float('inf')
    output_idx = None
    for idx in range(len(list1)):
            temp_cluster = alg_cluster.Cluster(set([]), list1[idx][0], list1[idx][1], 0, 0)
            temp_dist = temp_cluster.distance(point)     
            if temp_dist < distance:
                output_idx = idx
                distance = temp_dist 
    return output_idx    
    
 
#def code_rep(alg_list):
#    return [[ele.fips_codes() for ele in list1] for list1 in alg_list]

def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    total_cluster_num = len(cluster_list)
    cluster_list = [ele.copy() for ele in cluster_list]
    cluster_list.sort(key = lambda x: -x.total_population())
    center_list = [ (cluster_list[idx].horiz_center(), cluster_list[idx].vert_center())
                  for idx in range(num_clusters)]
    for _ in range(num_iterations):
        cluster_groups = [ [] for _ in range(num_clusters) ] 	
        for idx in range(total_cluster_num):
            group_idx = closest_cluster( cluster_list[idx], center_list )
            cluster_groups[group_idx] += [cluster_list[idx].copy()]        
        for fdx in range(num_clusters):
            one_group = cluster_groups[fdx]
            if one_group != []:
                for fdx_2 in range(1,len(one_group)):
                    one_group[0].merge_clusters( one_group[fdx_2] )     
                    center_list[fdx] =( one_group[0].horiz_center(),
                                       one_group[0].vert_center() )        
    output_clusters = [ele[0] for ele in cluster_groups]
    return output_clusters        
                        

## test cases 
#test_list = [alg_cluster.Cluster(set(['00']), 0.0, 0.0, 1, 0.1),
#             alg_cluster.Cluster(set(['10']), 1.0, 0.0, 2, 0.1),
#             alg_cluster.Cluster(set(['11']), 1.0, 1.0, 3, 0.1),
#             alg_cluster.Cluster(set(['01']), 0.0, 1.0, 4, 0.1),
#             alg_cluster.Cluster(set(['1010']), 10.0, 10.0, 5, 0.1),
#             alg_cluster.Cluster(set(['1011']), 10.0, 11.0, 6, 0.1),
#             alg_cluster.Cluster(set(['1111']), 11.0, 11.0, 7, 0.1),
#             alg_cluster.Cluster(set(['1110']), 11.0, 10.0, 8, 0.1)]
#
#print kmeans_clustering(test_list, 2, 2)                          
