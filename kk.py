import fileinput

if (len(sys.argv) != 2):
    print ("usage: python <inputfile>")
    exit(1)

for line in fileinput.input(sys.argv[1]):
    #process(line)