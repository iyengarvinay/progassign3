import fileinput
import bisect
import sys
import random

if (len(sys.argv) != 2):
    print ("usage: python3 <inputfile>")
    exit(1)

A = [int(line.rstrip('\n')) for line in open(sys.argv[1])]
original = list(A)

A.sort()

for i in range(len(A) - 1):
    a1 = A.pop()
    a2 = A.pop()
    diff = a1 - a2
    bisect.insort(A, diff)

print(A[0])

minResidue = max(original)
for j in range(25000):
	randSolution = [0]*100
	residue = 0
	for i in range(100):
		randSolution[i] = random.choice([-1,1])
		residue = abs(residue + (randSolution[i] * original[i]))
	if(residue < minResidue):
		minResidue = residue

print(minResidue)



	