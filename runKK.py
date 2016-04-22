import fileinput
import bisect
import sys
import csv

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

results = [["Random Set", "KK Result"]]

for i in range(int(sys.argv[1])):
    filename = "nums" + str(i) + ".txt"
    A = [int(line.rstrip('\n')) for line in open(filename)]
    results.append([i, kkRun(A)])

print (results)

# choosing one or two changes for neighborhood
# one with probability 100 / 5050 (100 = 100 choose 1)
# two with probability 4950 / 5050 (4950 = 100 choose 2)
total = 5050
r = random.uniform(0, total)
if (r >= 4950):
    # make one switch
else:
    # make two switches


csvfile = open('kkResults.csv','w')
wr = csv.writer(csvfile, quotechar=None)
wr.writerows(results)
csvfile.close()
