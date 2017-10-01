from sys import stdin

def isAlphabet(symbol):
    return  (symbol >= 'a' and symbol <= 'z') or(symbol >= 'A' and symbol <= 'Z')
def isDigit(symbol):
    return  symbol >= '0' and symbol <= '9'
def isAlphaNumeric(symbol):
    return isAlphabet(symbol) or isDigit(symbol)
    
operators = { "{" :"token_llave_izq", 
"}" :"token_llave_der", 
"$" :"token_dollar", 
";" :"token_pyc", 
"[" :"token_cor_izq", 
"]" :"token_cor_der", 
"(" :"token_par_izq", 
")" :"token_par_der", 
">" :"token_mayor", 
"<" :"token_menor", 
"!" :"token_not", 
"+" :"token_mas", 
"-" :"token_menos", 
"*" :"token_mul", 
"/" :"token_div", 
"%" :"token_mod", 
"eq" :"token_igual_str", 
"ne" :"token_diff_str", 
">=" :"token_mayor_igual", 
"<=" :"token_menor_igual", 
"==" :"token_igual_num", 
"!=" :"token_diff_num", 
"&&" :"token_and", 
"||" :"token_or", 
"**" :"token_pot"}
reserved =  {
    "stdin":"stdin", "gets":"gets", "size":"size", "incr":"incr" , "append":"append"  , "array":"array"  , "auto_execok":"auto_execok"  , "auto_import":"auto_import"  , "auto_load":"auto_load"  , "auto_load_index":"auto_load_index"  , "auto_qualify":"auto_qualify"  , "binary":"binary"  , "Bgerror":"Bgerror"  , "break":"break"  , "catch":"catch"  , "cd":"cd"  , "Clock":"Clock"  , "close":"close"  , "concat":"concat"  , "continue":"continue"  , "Dde":"Dde"  , "default":"default"  , "else":"else"  , "elseif":"elseif"  , "Encoding":"Encoding"  , "eof":"eof"  , "error":"error"  , "eval":"eval"  , "Exec":"Exec"  , "exit":"exit"  , "expr":"expr"  , "fblocked":"fblocked"  , "Fconfigure":"Fconfigure"  , "fcopy":"fcopy"  , "file":"file"  , "fileevent":"fileevent"  , "Flush":"Flush"  , "for":"for"  , "foreach":"foreach"  , "format":"format"  , "Gets":"Gets"  , "glob":"glob"  , "global":"global"  , "history":"history"  , "if":"if"  , "info":"info"  , "interp":"interp"  , "join":"join"  , "Lappend":"Lappend"  , "lindex":"lindex"  , "linsert":"linsert"  , "list":"list"  , "Llength":"Llength"  , "load":"load"  , "lrange":"lrange"  , "lreplace":"lreplace"  , "Lsearch":"Lsearch"  , "lsort":"lsort"  , "namespace":"namespace"  , "open":"open"  , "Package":"Package"  , "pid":"pid"  , "pkg_mkIndex":"pkg_mkIndex"  , "proc":"proc"  , "puts":"puts"  , "pwd":"pwd"  , "read":"read"  , "regexp":"regexp"  , "Regsub":"Regsub"  , "rename":"rename"  , "resource":"resource"  , "return":"return"  , "Scan":"Scan"  , "seek":"seek"  , "set":"set"  , "socket":"socket"  , "Source":"Source"  , "split":"split"  , "string":"string"  , "subst":"subst"  , "switch":"switch"  , "tclLog":"tclLog"  , "tell":"tell"   , "Trace":"Trace"  , "unknown":"unknown"  , "unset":"unset"  , "update":"update"  , "Uplevel":"Uplevel"  , "upvar":"upvar"  , "vwait":"vwait"  , "while":"while"  , "exists":"exists"  , "then":"then" , "case":"case" }
# reserved["variable"] = "variable" ???
class DFA:
    def __init__(self,  delta, initial, finals):
        self.initial = initial
        self.delta = delta
        self.finals = set(finals)
        self.actual = initial
    def EvalSymbol(self, symbol):
        self.actual = self.delta(self.actual, symbol)
    def Reset(self):
        self.actual = self.initial
    def InAccepting(self):
        return self.actual in self.finals
    def InInit(self):
        return self.actual == self.initial
################################ DELTAS DE CADA DFA  #################        
def delta_str(actual, symbol):
    if (symbol == '"'):
        return { 0:1, 1:2, 2:3, 3:1 }.get(actual, 0)
    return { 1:1, 2:3 }.get(actual, 0)
def delta_opr(actual, symbol):
    if (symbol == '<' or symbol == '>' or symbol == '!'):
        return { 0:1, 5:1  }.get(actual, 0)
    if (symbol == '=' ):
        return { 0:1, 1:5, 5:1  }.get(actual, 0)
    if (symbol == '&' ):
        return { 0:2, 2:5, 5:2  }.get(actual, 0)
    if (symbol == '|' ):
        return { 0:3, 3:5, 5:3  }.get(actual, 0)
    if (symbol == '*' ):
        return { 0:4, 4:5, 5:4  }.get(actual, 0)
    return 0
def delta_num(actual, symbol):
    if (symbol == '.'):
        return { 1:3, 4:5 }.get(actual, 0)
    if isDigit(symbol):
        return { 0:1, 1:1, 2:1, 3:4, 4:4 }.get(actual, 0)
    return { 1:2, 4:5 }.get(actual, 0)
def delta_id(actual, symbol):
    if (isAlphabet(symbol) or symbol == '_'):
        return { 0:1, 1:1, 2:0 }.get(actual, 0)
    if isDigit(symbol):
        return { 0:0, 1:1, 2:0 }.get(actual, 0)
    return { 0:0, 1:2, 2:0 }.get(actual, 0)
################################ UTILS  #################   

def EvalWordToPrnt(word):
    firstItem = word            if word in reserved  else  "id,{}".format(word)
    firstItem = operators[word] if word in operators else  firstItem
    print  "<{},{},{}>".format(firstItem,nLine,iniToken)
def LaunchError(a,b):
    print  ">>> Error lexico (linea: {}, posicion: {})".format(a, b )
    exit()
def PutAndClear( outStr ):
    print  outStr
    return []
def MustSaveStrInit(strInit, symbol, strAccept):
    return (strInit and symbol == '"') or (strAccept and symbol == '"')
    
################################# -- MAIN  -- ###################
# f = open('out.txt', 'w')
nLine = 0
mBuffer = []
lastChar = ' '
strPos =[1,1]

dfaNumeric   = DFA( delta_num , 0 , {2,5} )
dfaAlphaNum  = DFA( delta_id  , 0 , {2} )
dfaStrings   = DFA( delta_str , 0 , {3} )
dfaOperators = DFA( delta_opr , 0 , {5} )

for line in stdin: 
    nLine += 1
    iniToken =1 
    dfaNumeric.Reset()
    dfaAlphaNum.Reset()
    y = 0 
    lenLine = len(line) if  line[-1] == '\n' else len(line)+1
    while y < lenLine:
        symbol = '\n' if y == len(line) else line[y]
        y += 1
            
        symbolToBuffer = symbol != ' ' and symbol != '"'and symbol != '\n' and symbol != '\r'
        strPos = [nLine,y] if MustSaveStrInit( dfaStrings.InInit(), symbol, dfaStrings.InAccepting()) else strPos
        dfaStrings.EvalSymbol(symbol)
        
        # print  "    sym: ", symbol if symbol != '\n' else '\\n'," stat:", dfaStrings.actual , "w:", ''.join(mBuffer),"i:",iniToken
        if ( dfaStrings.InInit() ): ## FUERA DE STRING (SIN INICIAR STRING)
            word = ''.join(mBuffer)
            lastOperatorState = dfaOperators.actual
            lastNumericState = dfaNumeric.actual
            dfaNumeric.EvalSymbol(symbol)
            dfaAlphaNum.EvalSymbol(symbol)
            dfaOperators.EvalSymbol(symbol)
            if symbol == '#': ## SOLO APLICA FUERA DE UN STRING
                break
            elif  dfaAlphaNum.InAccepting():
                EvalWordToPrnt(word)
                if  symbolToBuffer and not dfaNumeric.InAccepting() and dfaOperators.InInit() and symbol not in operators:
                    LaunchError(nLine, y)
                dfaAlphaNum.Reset()
                mBuffer = []
                iniToken = y
            elif  dfaNumeric.InAccepting(): 
                nType = "double" if dfaNumeric.actual == 5 else "integer" 
                mBuffer =  PutAndClear( "<token_{},{},{},{}>".format(nType,word,nLine,iniToken) )
                iniToken = y
            elif dfaOperators.InAccepting():
                mBuffer =  PutAndClear( "<{},{},{}>".format(operators[word+symbol],nLine,iniToken) )
                iniToken = y
                symbolToBuffer = False
            elif len(word)==1 :
                if word[0] in operators :
                    mBuffer =  PutAndClear( "<{},{},{}>".format(operators[word[0]],nLine,y-1) )
                    iniToken = y
                elif lastOperatorState != dfaOperators.actual :
                    LaunchError(nLine, y-1)
            elif len(word) >0  and symbolToBuffer :
                if (not dfaAlphaNum.InInit() and not isAlphaNumeric(word[0]) and word[0] != '_') or ( not dfaNumeric.InInit() and not isDigit(word[0]) and dfaAlphaNum.InInit() ):
                    LaunchError(nLine, y-2)
                elif lastNumericState != dfaNumeric.actual and  dfaNumeric.InInit() and not isDigit(symbol) and dfaAlphaNum.InInit():
                    mBuffer =  PutAndClear( "<token_integer,{},{},{}>".format(word[:-1],nLine,iniToken) )
                    LaunchError(nLine, y-1)
            iniToken += 0 if  symbolToBuffer else 1 # Simbolo omitido del bufer nunca sera posicion inicial del token, por lo tanto se mueve
            
        elif dfaStrings.InAccepting():  ## FIN STRING
            mBuffer = PutAndClear("<token_string,{},{},{}>".format(''.join(mBuffer),strPos[0],strPos[1]) )
            iniToken = y+1
        elif not symbolToBuffer and symbol != '"' and (symbol != '\n'and symbol != '\r') : ## LEYENDO DENTRO DE STRING
            mBuffer.append(symbol )
            
        if symbolToBuffer  : 
            if len(mBuffer) >0 and mBuffer[0] in operators and lastChar == '"' :
                mBuffer =  PutAndClear( "<{},{},{}>".format(operators[mBuffer[0]],nLine,y-2  ) )
            if dfaStrings.InInit() and symbol not in operators and not isDigit(symbol) and not isAlphaNumeric(symbol) and symbol != '_'and symbol != '|'and symbol != '&' and symbol != '=' and symbol != '.' and symbol != '#':
                LaunchError(nLine, y)
            mBuffer.append(symbol )
        lastChar = symbol
            
    if not (dfaStrings.InAccepting() or dfaStrings.InInit() ) : 
        LaunchError(strPos[0],strPos[1]) # Nunca se cierra un string
    
# f.close()

