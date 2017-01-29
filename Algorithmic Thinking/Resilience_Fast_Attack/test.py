# -*- coding: utf-8 -*-
''''
Created on Sun Aug 28 22:43:18 2016

'''
from collections import deque

a = deque([1,2,3])
a.remove(1)
print a

print [node for node in range(4) for dummy_idx in range(4)] 