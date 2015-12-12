# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 02:25:21 2015

@author: Jigar Mehta
"""
list1=[]
path="C:\\txt_sentoken\\neg\\cv003_12683.txt"
print path
input=open(path, "r")      
for line in input:
    list1.append((line,"negative"))
print list1



import os
lst=os.listdir("C:\\txt_sentoken\\neg")
print lst
list1=[]
for i in range(0,len(lst)):
    path="C:\\txt_sentoken\\neg\\"+lst[i]
    print path
    input=open(path, "r")      
    for line in input:
        list1.append((line,"negative"))
print list1  

import os
lst=os.listdir("C:\\txt_sentoken\\pos")
print lst
list1=[]
for i in range(0,len(lst)):
    path="C:\\txt_sentoken\\pos\\"+lst[i]
    print path
    input=open(path, "r")      
    for line in input:
        list1.append((line,"positive"))
print list1       
    







