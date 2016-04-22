import fileinput
import bisect
import sys
import csv
import random

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
