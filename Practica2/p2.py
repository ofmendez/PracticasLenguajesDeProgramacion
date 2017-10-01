from sys import stdin
 
 # TEST FUNCTIONS
def pp(dic):
    for key in dic.keys():
        print key, "=>", dic[key]
        
def TestIsTermial():
    print isTerminal("ID") 
    print isTerminal(";") 
    print isTerminal("+")
    print isTerminal("{")
    print isTerminal("(")
    print isTerminal("3")
    print isTerminal("gets")
    print isTerminal("integer")
    print ("must be false: ")
    print isTerminal("PARAM")
    print isTerminal("PARAM")
    print isTerminal("GETS")        
    print isTerminal("A_PREM")        


# Creacion de diccionario para cada No terminal 
gramatica = {}
for line in stdin:
    line = line.strip().split()

    KEY = line[0]
    VALUES = line[ 2:len(line) ]

    if KEY not in gramatica.keys():
        gramatica[ KEY ] = []

    gramatica[ KEY ].append(VALUES)

 
# Calcular primeros de cada NO TERMINAL

def isTerminal(data):
    if data == "ID":
        return True
    
    
    if data[0].isupper():
        return False
    
    return True

    
def calc_PRIMEROS(KEY):
    
    list_PRIMEROS = []
    
    for derivacion in gramatica[KEY]:
       list_PRIMEROS.extend( ret_PRIMEROS(derivacion) )
       
    return list_PRIMEROS


def ret_PRIMEROS(derivacion):
    
    res_PRIMEROS = []
    
    
    # if len(derivacion) == 1 and derivacion[0] == "epsilon":
    #     # res_PRIMEROS.append("epsilon")
    #     pass
    
    
    if isTerminal(derivacion[0]):
        res_PRIMEROS.append(derivacion[0])
        
    if not isTerminal(derivacion[0]):
        aux = calc_PRIMEROS(derivacion[0])
        
        if len(derivacion) == 1 and aux[0] == "epsilon":
            res_PRIMEROS.append( "epsilon" )
            
        for item in derivacion:
            if isTerminal(item) :
                res_PRIMEROS.append( item )
                break
            
            aux = calc_PRIMEROS(item)
            res_PRIMEROS.extend( aux )
            
            if item == derivacion[len(derivacion) - 1]:
                break
            
            if "epsilon" in aux:
                res_PRIMEROS.remove("epsilon")
            else:
                break
            
            
    # print res_PRIMEROS
    res_P
    return res_PRIMEROS
        

PRIMEROS = {}
for KEY in gramatica.keys():
    
    PRIMEROS[KEY] = calc_PRIMEROS(KEY)
    
pp(PRIMEROS)


# PRIM A =  perro ant cow daniel 
# PRIM B =  ant epsilon