import fileinput
import sys

if (len(sys.argv) != 2):
    print ("usage: python <inputfile>")
    exit(1)

A = [line.rstrip('\n') for line in open(sys.argv[1])]

print(A)

A.sort()

print(A)