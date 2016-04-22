import fileinput
import bisect
import sys
import csv
import random
import copy

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
    minResidue = max(numList)
    for j in range(25000):
        randSolution = [0]*100
        residue = 0
        for i in range(100):
            randSolution[i] = random.choice([-1,1])
            residue = abs(residue + (randSolution[i] * numList[i]))
        if(residue < minResidue):
            minResidue = residue

    return minResidue

def repeatedRandomPartition(numList):
    minResidue = max(numList)
    for j in range(25000):
        randPartition = [0]*100
        numListModified = [0]*100
        for i in range(100):
            randPartition[i] = random.randint(0,99)
            numListModified[randPartition[i]] = numList[i] + numListModified[randPartition[i]]
        residue = kkRun(numListModified)
        if(residue < minResidue):
            minResidue = residue

    return minResidue

# choose random solution in neighborhood
# change one sign with probability 100 / 5050 (100 = 100 choose 1)
# change two with probability 4950 / 5050 (4950 = 100 choose 2)
def hillClimb(numList):

    # create random solution S
    randSolution = [0]*100
    residue = 0
    for i in range(100):
        randSolution[i] = random.choice([-1,1])
        residue = abs(residue + (randSolution[i] * numList[i]))
    minResidue = residue

    # find random neighbor of S
    total = 5050
    threshold = 4950
    for j in range(25000):
        # copy solution list in order to change
        neighbor = list(randSolution)
        r = random.uniform(0, total)

        # make one switch
        switch = random.uniform(0,99)
        neighbor[switch] = 1 if (neighbor[switch] == -1) else -1

        if (r < threshold):
            # make second switch
            switch2 = random.uniform(0,99)
            while (switch == switch2):
                switch2 = random.uniform(0,99)
            neighbor[switch2] = 1 if (neighbor[switch2] == -1) else -1
        
        residue = 0
        for i in range(100):
            residue = abs(residue + (neighbor[i] * numList[i]))

        if(residue < minResidue):
            minResidue = residue
            randSolution = neighbor

        return minResidue

# compute results
results = [["Random Set", "KK Result", "Repeated Random - Solution", "Repeated Random - Partition", "Hill Climbing - Solution", "Hill Climbing - Partition", "Simulated Annealing - Solution", "Simulated Annealing - Partition"]]

for i in range(int(sys.argv[1])):
    filename = "nums" + str(i) + ".txt"
    A = [int(line.rstrip('\n')) for line in open(filename)]
    results.append([i, kkRun(A), repeatedRandomSolution(A), repeatedRandomPartition(A)])

print (results)


csvfile = open('kkResults.csv','w')
wr = csv.writer(csvfile, quotechar=None)
wr.writerows(results)
csvfile.close()
