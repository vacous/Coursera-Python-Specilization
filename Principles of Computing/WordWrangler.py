"""
Student code for Word Wrangler game
"""

import urllib2
import math
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    output = []
    for ele in list1:
        if ele not in output:
            output.append(ele) 
    return output 

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    output = []
    for ele in list1:
        if ele in list2:
            output.append(ele)
    return output

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """   
    output = merge_sort(list1+list2) 
  
    return output

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    output = None
    if len(list1) == 1:
        return list1
    elif list1 == []:
        return list1
    else:
        smaller = []
        larger = []
        equal = []
        mean = sum(list1)/len(list1)
        
        for ele in list1:
            if ele < math.ceil(mean):
                smaller.append(ele)
            elif ele == math.ceil(mean):
                equal.append(ele)
            else:
                larger.append(ele)     
            output = merge_sort(smaller)+ equal + merge_sort(larger)
         
    return output 

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word)==0:
        return [word]
    first=word[0]
    rest_strings=gen_all_strings(word[1:])
    
    result=[]
    for string in rest_strings:
        for idx in range(len(string)+1):
            result.append(string[:idx]+first+string[idx:]) 
            
    return rest_strings+result
             
    
# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()
print  gen_all_strings('ab')  
