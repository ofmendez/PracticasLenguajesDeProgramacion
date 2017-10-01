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
       
       
    list_PRIMEROS = set(list_PRIMEROS)
    list_PRIMEROS = list(list_PRIMEROS)
    return list_PRIMEROS


def calc_SIGUIENTES(KEY):
    list_SIGUIENTES = []
    if KEY == "S"
        list_SIGUIENTES.append("eof")
    for NTER in gramatica.keys():
    list_SIGUIENTES = set(list_SIGUIENTES)
           list_SIGUIENTES.extend( ret_SIGUIENTES(derivacion, KEY) )
        
    
    
    list_SIGUIENTES = set(list_SIGUIENTES)
    list_SIGUIENTES = list(list_SIGUIENTES)
    return list_SIGUIENTES
    

def ret_SIGUIENTES(derivacion, KEY):
    res_SIGUIENTES = []
    for
    if KEY in derivacion:
        
    
    res_SIGUIENTES = set(res_SIGUIENTES)
    res_SIGUIENTES = list(res_SIGUIENTES)

    return res_SIGUIENTES
    

def ret_PRIMEROS(derivacion):
    
    res_PRIMEROS = []

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
            
    res_PRIMEROS = set(res_PRIMEROS)
    res_PRIMEROS = list(res_PRIMEROS)

    return res_PRIMEROS
        

PRIMEROS = {}
SIGUIENTES = {}
for KEY in gramatica.keys():
    PRIMEROS[KEY] = calc_PRIMEROS(KEY)
    SIGUIENTES[KEY] = calc_SIGUIENTES(KEY)
    
pp(PRIMEROS)



# PRIM A =  perro ant cow daniel 
# PRIM B =  ant epsilon