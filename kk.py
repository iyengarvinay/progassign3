import fileinput
import bisect
import sys
import random

if (len(sys.argv) != 2):
    print ("usage: python kk.py <inputfile>")
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

	

	