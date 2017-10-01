from sys import stdin

gramatica = {}

def pp():
    for key in gramatica.keys():
        print key, "=>", gramatica[key]

for line in stdin:
    line = line.strip().split()

    KEY = line[0]
    VALUES = line[ 2:len(line) ]

    if KEY not in gramatica.keys():
        gramatica[ KEY ] = []

    gramatica[ KEY ].append(VALUES)

pp()