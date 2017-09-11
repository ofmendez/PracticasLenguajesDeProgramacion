from sys import stdin

def isAlphabet(symbol):
    return  (symbol >= 'a' and symbol <= 'z') or(symbol >= 'A' and symbol <= 'Z')
def isDigit(symbol):
    return  symbol >= '0' and symbol <= '9'
def isAlphaNumeric(symbol):
    return isAlphabet(symbol) or isDigit(symbol)
    
operators = { "{" :"token_llave_izq", "}" :"token_llave_der", "$" :"token_dollar", ";" :"token_pyc", "[" :"token_cor_izq", "]" :"token_cor_der", "(" :"token_par_izq", ")" :"token_par_der", ">" :"token_mayor", "<" :"token_menor", "!" :"token_not", "+" :"token_mas", "-" :"token_menos", "*" :"token_mul", "/" :"token_div", "%" :"token_mod", "eq" :"token_igual_str", "ne" :"token_diff_str", ">=" :"token_mayor_igual", "<=" :"token_menor_igual", "==" :"token_igual_num", "!=" :"token_diff_num", "&&" :"token_and", "||" :"token_or", "**" :"token_pot"}
reserved =  {"after":"after"  , "append":"append"  , "array":"array"  , "auto_execok":"auto_execok"  , "auto_import":"auto_import"  , "auto_load":"auto_load"  , "auto_load_index":"auto_load_index"  , "auto_qualify":"auto_qualify"  , "binary":"binary"  , "Bgerror":"Bgerror"  , "break":"break"  , "catch":"catch"  , "cd":"cd"  , "Clock":"Clock"  , "close":"close"  , "concat":"concat"  , "continue":"continue"  , "Dde":"Dde"  , "default":"default"  , "else":"else"  , "elseif":"elseif"  , "Encoding":"Encoding"  , "eof":"eof"  , "error":"error"  , "eval":"eval"  , "Exec":"Exec"  , "exit":"exit"  , "expr":"expr"  , "fblocked":"fblocked"  , "Fconfigure":"Fconfigure"  , "fcopy":"fcopy"  , "file":"file"  , "fileevent":"fileevent"  , "Flush":"Flush"  , "for":"for"  , "foreach":"foreach"  , "format":"format"  , "Gets":"Gets"  , "glob":"glob"  , "global":"global"  , "history":"history"  , "if":"if"  , "info":"info"  , "interp":"interp"  , "join":"join"  , "Lappend":"Lappend"  , "lindex":"lindex"  , "linsert":"linsert"  , "list":"list"  , "Llength":"Llength"  , "load":"load"  , "lrange":"lrange"  , "lreplace":"lreplace"  , "Lsearch":"Lsearch"  , "lsort":"lsort"  , "namespace":"namespace"  , "open":"open"  , "Package":"Package"  , "pid":"pid"  , "pkg_mkIndex":"pkg_mkIndex"  , "proc":"proc"  , "puts":"puts"  , "pwd":"pwd"  , "read":"read"  , "regexp":"regexp"  , "Regsub":"Regsub"  , "rename":"rename"  , "resource":"resource"  , "return":"return"  , "Scan":"Scan"  , "seek":"seek"  , "set":"set"  , "socket":"socket"  , "Source":"Source"  , "split":"split"  , "string":"string"  , "subst":"subst"  , "switch":"switch"  , "tclLog":"tclLog"  , "tell":"tell"  , "time":"time"  , "Trace":"Trace"  , "unknown":"unknown"  , "unset":"unset"  , "update":"update"  , "Uplevel":"Uplevel"  , "upvar":"upvar"  , "vwait":"vwait"  , "while":"while"  , "exists":"exists"  , "then":"then"  }
# reserved["variable"] = "variable" ???

class DFA:
    def __init__(self, states, delta, initial, finals):
        self.states = set(states)
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
        return { 0:1, 1:1, 3:4, 4:4 }.get(actual, 0)
    return { 1:2, 4:5 }.get(actual, 0)
    
def delta_id(actual, symbol):
    if (isAlphabet(symbol) or symbol == '_'):
        return { 0:1, 1:1, 2:0 }.get(actual, 0)
    if isDigit(symbol):
        return { 0:0, 1:1, 2:0 }.get(actual, 0)
    return { 0:0, 1:2, 2:0 }.get(actual, 0)

def EvalWordToPrnt():
    firstItem = word if word in reserved else "id,{}".format(word)
    firstItem = firstItem if word not in operators else operators[word]
    print >> f, "<{},{},{}>".format(firstItem,nLine,iniToken)
def PassAlphabet(symbol):
    return False
def LaunchError(a,b):
    print >> f, ">>> Error lexico (linea: {}, posicion: {})".format(a, b )
    exit()
def MustSaveStrInit(strInit, symbol):
    return strInit and symbol == '"'
#************************MAIN*******************
f = open('out.txt', 'w')
nLine = 0
mBuffer = []
strPos =[1,1]

dfaNumeric   = DFA( range(6) , delta_num , 0 , {2,5} )
dfaAlphaNum  = DFA( range(3) , delta_id  , 0 , {2} )
dfaStrings   = DFA( range(4) , delta_str , 0 , {3} )
dfaOperators = DFA( range(6) , delta_opr , 0 , {5} )

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
            
        symbolToBuffer = symbol != ' ' and symbol != '"'and symbol != '\n'and symbol != '\r'
        strPos = [nLine,y] if MustSaveStrInit( dfaStrings.InInit(), symbol) else strPos
        dfaStrings.EvalSymbol(symbol)
        
        if dfaStrings.InAccepting():  ## FIN STRING
            print >> f, "<token_string,{},{},{}>".format(''.join(mBuffer),strPos[0],strPos[1])
            mBuffer = []
            iniToken = y+1
        elif (dfaStrings.actual != 1 and dfaStrings.actual != 2 ): ## FUERA DE STRING
            if not PassAlphabet(symbol):
                pass
            word = ''.join(mBuffer)
            lastOperatorState = dfaOperators.actual
            lastNumericState = dfaNumeric.actual
            dfaNumeric.EvalSymbol(symbol)
            dfaAlphaNum.EvalSymbol(symbol)
            dfaOperators.EvalSymbol(symbol)
            # print >> f, "sym: ", symbol if symbol != '\n' else '\\n'," stat:", dfaNumeric.actual , "w:", ''.join(mBuffer),"i:",iniToken
            if  dfaAlphaNum.InAccepting():
                EvalWordToPrnt()
                if  symbolToBuffer and not dfaNumeric.InAccepting() and dfaOperators.InInit() and symbol not in operators:
                    LaunchError(nLine, y)
                dfaAlphaNum.Reset()
                mBuffer = []
                iniToken = y
            elif  dfaNumeric.InAccepting(): 
                nType = "double" if dfaNumeric.actual == 5 else "integer" 
                print >> f, "<token_{},{},{},{}>".format(nType,word,nLine,iniToken)
                mBuffer = []
                iniToken = y
            elif dfaOperators.InAccepting():
                print >> f, "<{},{},{}>".format(operators[word+symbol],nLine,iniToken)
                mBuffer = []
                iniToken = y
                symbolToBuffer = False
            elif len(word)==1 :
                if word[0] in operators :
                    print >> f, "<{},{},{}>".format(operators[word[0]],nLine,y-1)
                    mBuffer = []
                    iniToken = y
                elif lastOperatorState != dfaOperators.actual :
                    LaunchError(nLine, y-1)
                    
            elif symbol == '#': ## SOLO APLICA FUERA DE UN STRING
                break
            elif len(word) >0  and symbolToBuffer :
                if (not dfaAlphaNum.InInit() and not isAlphaNumeric(word[0]) and word[0] != '_') or ( not dfaNumeric.InInit() and not isDigit(word[0]) and dfaAlphaNum.InInit() ):
                    LaunchError(nLine, y-2)
                elif lastNumericState != dfaNumeric.actual and  dfaNumeric.InInit() and not isDigit(symbol) and dfaAlphaNum.InInit():
                    print >> f, "<token_integer,{},{},{}>".format(word[:-1],nLine,iniToken)
                    LaunchError(nLine, y-1)
        elif not symbolToBuffer and symbol != '"' and (symbol != '\n'and symbol != '\r') : ## LEYENDO DENTRO DE STRING
            mBuffer.append(symbol )
                        
        if symbolToBuffer  :
            mBuffer.append(symbol )
        elif dfaStrings.InInit() :
            iniToken +=1
# if  not dfaStrings.InAccepting(): pass # PRNT ERROR
f.close()

