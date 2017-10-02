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
    if KEY == "S":
        list_SIGUIENTES.append("eof")
    for NTER in gramatica.keys():
        for derivacion in gramatica[NTER]:
           list_SIGUIENTES.extend( ret_SIGUIENTES(derivacion, KEY, NTER) )
    
    
    list_SIGUIENTES = set(list_SIGUIENTES)
    list_SIGUIENTES = list(list_SIGUIENTES)
    if "epsilon" in list_SIGUIENTES:
        list_SIGUIENTES.remove("epsilon")
    return list_SIGUIENTES
    

def ret_SIGUIENTES(derivacion, KEY, NTER):
    res_SIGUIENTES = []
    
    if KEY in derivacion:
        # print ">>>> NTR: ", NTER," - " , "K:", KEY, derivacion
        for i in range(len (derivacion)):
            if derivacion[i] == KEY :
                if i < (len(derivacion) - 1):
                    FLAG = False
                    incr = 1
                    
                    if isTerminal(derivacion[i + incr]):
                        res_SIGUIENTES.append(derivacion[i + incr])
                        break
                    
                    aux = PRIMEROS[ derivacion[i + incr] ][:]
                    
                    while "epsilon" in aux and (i + incr) < len(derivacion):
                        if  (i + incr) == len(derivacion)-1:
                            if KEY != NTER :
                                res_SIGUIENTES.extend( calc_SIGUIENTES (NTER) )
                                # res_SIGUIENTES.append( " aSIG({} )".format(NTER) )
                            FLAG = True
                            break
                            
                        aux.remove("epsilon")
                        res_SIGUIENTES.extend(aux)
                        incr += 1
                        
                        if isTerminal(derivacion[i + incr]) :
                            res_SIGUIENTES.append(derivacion[i + incr])
                            FLAG = True
                            break
                        
                        aux = PRIMEROS[ derivacion[i + incr] ][:]
                        
                        
                    res_SIGUIENTES.extend(aux)
                    if FLAG:
                        break   

                else : # KEY en ultima posicion
                    if KEY != NTER :
                        res_SIGUIENTES.extend( calc_SIGUIENTES (NTER) )
                        # res_SIGUIENTES.append( " bSIG({})".format(NTER) )
                
    
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
            
    return res_PRIMEROS
        


            
            
def prediccion(derivacion, KEY):
    
    list_prediccion = []
    if len(derivacion)  == 1 and derivacion[0] == "epsilon":
        list_prediccion.extend(SIGUIENTES[KEY])
    else:
        for word in derivacion:
            if isTerminal(word):
                list_prediccion.append(word) 
                break
            else:
                # print "DEBE SER NO TERMINAL: ",word, derivacion
                if "epsilon" in PRIMEROS[word]:
                    list_prediccion.extend(PRIMEROS[word]) 
                    list_prediccion.extend(SIGUIENTES[KEY]) 
                else:
                    list_prediccion.extend(PRIMEROS[word]) 
                    break
            
    
    list_prediccion = set(list_prediccion)
    list_prediccion = list(list_prediccion)

    if "epsilon" in list_prediccion:
        list_prediccion.remove("epsilon")
    
    return list_prediccion
        

def calc_PREDICCION(KEY):
    lista_prediccion = []
    for derivacion in gramatica[KEY]:
        lista_prediccion.append( prediccion(derivacion, KEY) )
        
    return lista_prediccion

PRIMEROS = {}
SIGUIENTES = {}
PREDICCION = {}

for KEY in gramatica.keys():
    PRIMEROS[KEY] = calc_PRIMEROS(KEY)
for KEY in gramatica.keys():
    SIGUIENTES[KEY] = calc_SIGUIENTES(KEY)
    
for KEY in gramatica.keys():
    PREDICCION[KEY] = calc_PREDICCION(KEY)


print "token = Translate( lexico.pop(0) ) "
print "S()"
print "if ( token != \"eof\" ):"



# print "  -PRIMEROS - " 
# pp(PRIMEROS)
# print "  -SIGUIENTES - " 
# pp(SIGUIENTES)
# print "  -PREDICCION - " 
# pp(PREDICCION)


# PRIM A =  perro ant cow daniel 
# PRIM B =  ant epsilon