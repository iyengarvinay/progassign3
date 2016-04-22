#!/usr/bin/python
# -*- coding: utf-8 -*-

# usage: python3 genNums.py maxValue setSize numSets
# where maxValue is the top bound for any integer element of the matrix

import random
import sys

def genNums(n, maxVal):
    lst = []
    for i in range(n):
        lst.append(random.randint(1, maxVal))
    return lst

def writeNums(numList, filename):
    f = open(filename, 'w')
    for num in numList:
        f.write(str(num) + "\n")

if (len(sys.argv) != 4):
    print ("usage: python genNums.py maxValue setSize numSets")
    exit(1)

maxVal = int(sys.argv[1])
setSize = int(sys.argv[2])
numSets = int(sys.argv[3])

for i in range(numSets):
    numList = genNums(setSize, maxVal)
    writeNums(numList, "nums{}.txt".format(i))