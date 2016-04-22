import fileinput
import bisect
import sys
import csv
import random
import copy
import math
from decimal import *

MAX_ITER = 25000

if (len(sys.argv) != 2):
    print ("usage: python3 runKK.py numSets")
    exit(1)

def kkRun(numList):
    A = list(numList)
    A.sort()

    for i in range(len(A) - 1):
        a1 = A.pop()
        a2 = A.pop()
        diff = a1 - a2
        bisect.insort(A, diff)

    return (A[0])

def repeatedRandomSolution(numList):
    numCount = len(numList)
    minResidue = max(numList)
    for j in range(MAX_ITER):
        randSolution = [0]*numCount
        residue = 0
        for i in range(numCount):
            randSolution[i] = random.choice([-1,1])
            residue = abs(residue + (randSolution[i] * numList[i]))
        if(residue < minResidue):
            minResidue = residue

    return minResidue

def repeatedRandomPartition(numList):
    numCount = len(numList)
    minResidue = max(numList)
    for j in range(MAX_ITER):
        randPartition = [0]*numCount
        numListModified = [0]*numCount
        for i in range(numCount):
            randPartition[i] = random.randint(0,numCount-1)
            numListModified[randPartition[i]] = numList[i] + numListModified[randPartition[i]]
        residue = kkRun(numListModified)
        if(residue < minResidue):
            minResidue = residue

    return minResidue

# choose random solution in neighborhood
# change one sign with probability 100 / 5050 (100 = 100 choose 1)
# change two with probability 4950 / 5050 (4950 = 100 choose 2)
def hillClimb(numList):

    numCount = len(numList)

    # create random solution S
    randSolution = [0]*numCount
    residue = 0
    for i in range(numCount):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue

    # find random neighbor of S
    for j in range(MAX_ITER):
        # copy solution list in order to change
        neighbor = list(randSolution)

        # make one switch
        switch = random.randint(0,numCount-1)
        neighbor[switch] *= -1

        # second switch with prob 1/2
        if (random.getrandbits(1) == 1):
            switch2 = random.randint(0,numCount-1)
            while (switch == switch2):
                switch2 = random.randint(0,numCount-1)
            neighbor[switch2] *= -1
        
        residue = 0
        for i in range(numCount):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if(residue < minResidue):
            minResidue = residue
            randSolution = list(neighbor)

        return minResidue

def simAnneal(numList):

    numCount = len(numList)

    # create random solution S
    randSolution = [0]*numCount
    residue = 0
    for i in range(numCount):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue
    homeSolution = list(randSolution)
    homeRes = minResidue

    # find random neighbor of S
    for j in range(MAX_ITER):
        # copy solution list in order to change
        neighbor = list(randSolution)

        # make one switch
        switch = random.randint(0,numCount-1)
        neighbor[switch] *= -1

        # second switch with prob 1/2
        if (random.getrandbits(1) == 1):
            switch2 = random.randint(0,numCount-1)
            while (switch == switch2):
                switch2 = random.randint(0,numCount-1)
            neighbor[switch2] *= -1

        residue = 0
        for i in range(numCount):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if(residue < minResidue):
            minResidue = residue
            randSolution = list(neighbor)

        else:
            tens = pow(10,10)
            bottom = pow(0.8,(math.floor(j/300)))
            resDiff = -(residue - minResidue)
            exponent = resDiff/(tens*bottom)
            #print(exponent)
            prob = math.exp(exponent)
            #if (j < 300):
                #print (prob)
            if (random.uniform(0,1) > prob):
                randSolution = list(neighbor)
                minResidue = residue

        if(residue < homeRes):
            homeSolution = list(neighbor)
            homeRes = residue

    return minResidue

# test numList: KK is 2
test = [10, 8, 7, 6, 5]

# compute results
#results = [["Random Set", "KK Result", "Repeated Random - Solution", "Repeated Random - Partition", "Hill Climbing - Solution", "Hill Climbing - Partition", "Simulated Annealing - Solution", "Simulated Annealing - Partition"]]
results = [["Random Set", "KK", "RR", "Hill Climb", "Simulated Annealing"]]
for i in range(int(sys.argv[1])):
    filename = "nums" + str(i) + ".txt"
    A = [int(line.rstrip('\n')) for line in open(filename)]
    #results.append([i, kkRun(A), repeatedRandomSolution(A), repeatedRandomPartition(A), hillClimb(A), simAnneal(A)])
    results.append([i, kkRun(test), repeatedRandomSolution(test), hillClimb(test), simAnneal(test)])
for line in results:
    print (line)


csvfile = open('kkResults.csv','w')
wr = csv.writer(csvfile, quotechar=None)
wr.writerows(results)
csvfile.close()
