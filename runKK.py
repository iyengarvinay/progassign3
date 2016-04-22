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

def kkRun(numList, n):
    A = list(numList)
    A.sort()

    for i in range(n - 1):
        a1 = A.pop()
        a2 = A.pop()
        diff = a1 - a2
        bisect.insort(A, diff)

    return (A[0])

def repeatedRandomSolution(numList, n):
    minResidue = max(numList)
    for j in range(MAX_ITER):
        randSolution = [0]*n
        residue = 0
        for i in range(n):
            randSolution[i] = random.choice([-1,1])
            residue = abs(residue + (randSolution[i] * numList[i]))
        if(residue < minResidue):
            minResidue = residue

    return minResidue

def repeatedRandomPartition(numList, n):
    minResidue = max(numList)
    for j in range(MAX_ITER):
        randPartition = [0]*n
        numListModified = [0]*n
        for i in range(n):
            randPartition[i] = random.randint(0,n-1)
            numListModified[randPartition[i]] = numList[i] + numListModified[randPartition[i]]
        residue = kkRun(numListModified)
        if(residue < minResidue):
            minResidue = residue

    return minResidue

# choose random solution in neighborhood
# change one sign with probability 100 / 5050 (100 = 100 choose 1)
# change two with probability 4950 / 5050 (4950 = 100 choose 2)
def hillClimb(numList, n):
    randSolution = [0]*n
    residue = 0
    for i in range(n):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue

    # find random neighbor of S
    for j in range(MAX_ITER):
        # copy solution list in order to change
        neighbor = list(randSolution)

        # make one switch
        switch = random.randint(0,n-1)
        neighbor[switch] *= -1

        # second switch with prob 1/2
        if (random.getrandbits(1) == 1):
            switch2 = random.randint(0,n-1)
            while (switch == switch2):
                switch2 = random.randint(0,n-1)
            neighbor[switch2] *= -1
        
        #print("neighbor {}", j)
        #printSol(numList, neighbor, n)

        residue = 0
        for i in range(n):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if(residue < minResidue):
            minResidue = residue
            randSolution = list(neighbor)

    return minResidue

def hillClimbPartition(numList, n):
    randSolution = [0]*n
    residue = 0
    for i in range(n):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue

    # find random neighbor of S
    for j in range(MAX_ITER):
        # copy solution list in order to change
        neighbor = list(randSolution)

        # make one switch
        switch = random.randint(0,n-1)
        neighbor[switch] *= -1

        # second switch with prob 1/2
        if (random.getrandbits(1) == 1):
            switch2 = random.randint(0,n-1)
            while (switch == switch2):
                switch2 = random.randint(0,n-1)
            neighbor[switch2] *= -1
        
        #print("neighbor {}", j)
        #printSol(numList, neighbor, n)

        residue = 0
        for i in range(n):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if(residue < minResidue):
            minResidue = residue
            randSolution = list(neighbor)

    return minResidue

def simAnneal(numList, n):

    # create random solution S
    randSolution = [0]*n
    residue = 0
    for i in range(n):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue
    homeSolution = list(randSolution)
    homeRes = minResidue

    #probs = [[]]

    #switches = 0
    #succswitches = 0

    # find random neighbor of S
    for j in range(MAX_ITER):
        # copy solution list in order to change
        neighbor = list(randSolution)
        # make one switch
        switch = random.randint(0,n-1)
        neighbor[switch] *= -1

        # second switch with prob 1/2
        if (random.getrandbits(1) == 1):
            switch2 = random.randint(0,n-1)
            while (switch == switch2):
                switch2 = random.randint(0,n-1)
            neighbor[switch2] *= -1

        residue = 0
        for i in range(n):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if (residue <= minResidue):
            minResidue = residue
            randSolution = list(neighbor)
            #switches += 1

        else:
            tens = pow(10,10)
            bottom = pow(0.8,(math.floor(j/300)))
            resDiff = -(residue - minResidue)
            exponent = resDiff/(tens*bottom)
            #print(exponent)
            prob = math.exp(exponent)
            probs.append([prob])
            if (random.uniform(0,1) <= prob):
                randSolution = list(neighbor)
                minResidue = residue
                #switches += 1

        if (residue < homeRes):
            homeSolution = list(neighbor)
            homeRes = residue
            #succswitches += 1


    #csvSim = open('simFunc.csv','w')
    #wr = csv.writer(csvSim, quotechar=None)
    #wr.writerows(probs)
    #csvSim.close()
    #print(switches)
    #print(succswitches)
    return minResidue

def printSol(numList, signList, n):
    A = []
    B = []
    for i in range(n):
        if(signList[i] == 1):
            A.append(numList[i])
        else:
            B.append(numList[i])
    print(A)
    print(B)

# test numList: KK is 2
test = [10, 8, 7, 6, 5]
lenTest = len(test)

# compute results
#results = [["Random Set", "KK Result", "Repeated Random - Solution", "Repeated Random - Partition", "Hill Climbing - Solution", "Hill Climbing - Partition", "Simulated Annealing - Solution", "Simulated Annealing - Partition"]]
results = [["Random Set", "KK", "RR", "Hill Climb", "Simulated Annealing"]]
for i in range(int(sys.argv[1])):
    filename = "nums" + str(i) + ".txt"
    A = [int(line.rstrip('\n')) for line in open(filename)]
    lenA = len(A)
    #results.append([i, kkRun(A), repeatedRandomSolution(A), repeatedRandomPartition(A), hillClimb(A), simAnneal(A)])
    #results.append([i, kkRun(test, lenTest), repeatedRandomSolution(test, lenTest), hillClimb(test, lenTest), simAnneal(test, lenTest)])
    results.append([i, kkRun(A, lenA), repeatedRandomSolution(A, lenA), hillClimb(A, lenA), simAnneal(A, lenA)])
for line in results:
    print (line)


csvFile = open('kkResults.csv','w')
wr = csv.writer(csvFile, quotechar=None)
wr.writerows(results)
csvFile.close()
