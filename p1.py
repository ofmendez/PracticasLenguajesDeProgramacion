from sys import stdin

def isAlphabet(symbol):
    return  (symbol >= 'a' and symbol <= 'z') or(symbol >= 'A' and symbol <= 'Z')
def isDigit(symbol):
    return  symbol >= '0' and symbol <= '9'
def isAlphaNumeric(symbol):
    return isAlphabet(symbol) or isDigit(symbol)
    
operators = {}
reserved = {}
operators["{"] = "token_llave_izq"
operators["}"] = "token_llave_der"
operators["$"] = "token_dollar"
operators[";"] = "token_pyc"
operators["["] = "token_cor_izq"
operators["]"] = "token_cor_der"
operators["("] = "token_par_izq"
operators[")"] = "token_par_der"
operators[">"] = "token_mayor"
operators["<"] = "token_menor"
operators["!"] = "token_not"
operators["+"] = "token_mas"
operators["-"] = "token_menos"
operators["*"] = "token_mul"
operators["/"] = "token_div"
operators["%"] = "token_mod"

operators["eq"] = "token_igual_str"
operators["ne"] = "token_diff_str"

operators[">="] = "token_mayor_igual"
operators["<="] = "token_menor_igual"
operators["=="] = "token_igual_num"
operators["!="] = "token_diff_num"

operators["&&"] = "token_and"
operators["||"] = "token_or"
operators["**"] = "token_pot"

reserved["after"] = "after"
reserved["append"] = "append"
reserved["array"] = "array"
reserved["auto_execok"] = "auto_execok"
reserved["auto_import"] = "auto_import"
reserved["auto_load"] = "auto_load"
reserved["auto_load_index"] = "auto_load_index"
reserved["auto_qualify"] = "auto_qualify"
reserved["binary"] = "binary"
reserved["Bgerror"] = "Bgerror"
reserved["break"] = "break"
reserved["catch"] = "catch"
reserved["cd"] = "cd"
reserved["Clock"] = "Clock"
reserved["close"] = "close"
reserved["concat"] = "concat"
reserved["continue"] = "continue"
reserved["Dde"] = "Dde"
reserved["default"] = "default"
reserved["else"] = "else"
reserved["elseif"] = "elseif"
reserved["Encoding"] = "Encoding"
reserved["eof"] = "eof"
reserved["error"] = "error"
reserved["eval"] = "eval"
reserved["Exec"] = "Exec"
reserved["exit"] = "exit"
reserved["expr"] = "expr"
reserved["fblocked"] = "fblocked"
reserved["Fconfigure"] = "Fconfigure"
reserved["fcopy"] = "fcopy"
reserved["file"] = "file"
reserved["fileevent"] = "fileevent"
reserved["Flush"] = "Flush"
reserved["for"] = "for"
reserved["foreach"] = "foreach"
reserved["format"] = "format"
reserved["Gets"] = "Gets"
reserved["glob"] = "glob"
reserved["global"] = "global"
reserved["history"] = "history"
reserved["if"] = "if"
reserved["info"] = "info"
reserved["interp"] = "interp"
reserved["join"] = "join"
reserved["Lappend"] = "Lappend"
reserved["lindex"] = "lindex"
reserved["linsert"] = "linsert"
reserved["list"] = "list"
reserved["Llength"] = "Llength"
reserved["load"] = "load"
reserved["lrange"] = "lrange"
reserved["lreplace"] = "lreplace"
reserved["Lsearch"] = "Lsearch"
reserved["lsort"] = "lsort"
reserved["namespace"] = "namespace"
reserved["open"] = "open"
reserved["Package"] = "Package"
reserved["pid"] = "pid"
reserved["pkg_mkIndex"] = "pkg_mkIndex"
reserved["proc"] = "proc"
reserved["puts"] = "puts"
reserved["pwd"] = "pwd"
reserved["read"] = "read"
reserved["regexp"] = "regexp"
reserved["Regsub"] = "Regsub"
reserved["rename"] = "rename"
reserved["resource"] = "resource"
reserved["return"] = "return"
reserved["Scan"] = "Scan"
reserved["seek"] = "seek"
reserved["set"] = "set"
reserved["socket"] = "socket"
reserved["Source"] = "Source"
reserved["split"] = "split"
reserved["string"] = "string"
reserved["subst"] = "subst"
reserved["switch"] = "switch"
reserved["tclLog"] = "tclLog"
reserved["tell"] = "tell"
reserved["time"] = "time"
reserved["Trace"] = "Trace"
reserved["unknown"] = "unknown"
reserved["unset"] = "unset"
reserved["update"] = "update"
reserved["Uplevel"] = "Uplevel"
reserved["upvar"] = "upvar"
# reserved["variable"] = "variable" ???
reserved["vwait"] = "vwait"
reserved["while"] = "while"
reserved["exists"] ="exists"
reserved["then"] ="then"



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
        return { 1:3, 3:4, 5:6 }.get(actual, 0)
    if isDigit(symbol):
        return { 0:1, 1:1, 3:5, 5:5 }.get(actual, 0)
    return { 1:2, 3:4, 5:6 }.get(actual, 0)
    
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
#************************MAIN*******************
f = open('out.txt', 'w')
nLine = 0
mBuffer = []

dfaNumeric   = DFA( range(7) , delta_num , 0 , {2,4,6} )
dfaAlphaNum  = DFA( range(3) , delta_id  , 0 , {2} )
dfaStrings   = DFA( range(4) , delta_str , 0 , {3} )
dfaOperators = DFA( range(6) , delta_opr , 0 , {5} )

for line in stdin: 
    nLine += 1
    iniToken =1
    dfaNumeric.Reset()
    dfaAlphaNum.Reset()
    y = 0 
    while y <= len(line):
        if y < len(line):
            symbol = line[y]
        elif line[-1] != '\n': 
            symbol = '\n'
        else :
            break
        y += 1
            
        symbolToBuffer = symbol != ' ' and symbol != '"'and symbol != '\n'and symbol != '\r'
        dfaStrings.EvalSymbol(symbol)
        # print >> f, "sym: ", symbol if symbol != '\n' else '\\n'," stat:", dfaStrings.actual , "w:", ''.join(mBuffer),"i:",iniToken
        if dfaStrings.InAccepting():  ## FIN STRING
            print >> f, "<token_string,{},{},{}>".format(''.join(mBuffer),nLine,iniToken)
            mBuffer = []
            iniToken = y+1
        elif (dfaStrings.actual != 1 and dfaStrings.actual != 2 ): ## FUERA DE STRING
            if not PassAlphabet(symbol):
                pass
            dfaNumeric.EvalSymbol(symbol)
            dfaAlphaNum.EvalSymbol(symbol)
            dfaOperators.EvalSymbol(symbol)
            word = ''.join(mBuffer)
            if  dfaAlphaNum.InAccepting():
                EvalWordToPrnt()
                if  symbolToBuffer and dfaNumeric.InInit() and dfaOperators.InInit() and symbol not in operators:
                    LaunchError(nLine, y)
                dfaAlphaNum.Reset()
                mBuffer = []
                iniToken = y
            elif  dfaNumeric.InAccepting(): 
                # if  symbolToBuffer and dfaNumeric.InInit() and dfaOperators.InInit() and symbol not in operators:
                #     LaunchError(nLine, y)
                nType = "double" if dfaNumeric.actual == 6 else "integer" 
                print >> f, "<token_{},{},{},{}>".format(nType,word,nLine,iniToken)
                mBuffer = []
                iniToken = y
            elif dfaOperators.InAccepting():
                # if  symbolToBuffer and dfaNumeric.InInit() and dfaOperators.InInit() and symbol not in operators:
                #     LaunchError(nLine, y)
                print >> f, "<{},{},{}>".format(operators[word+symbol],nLine,iniToken)
                mBuffer = []
                iniToken = y
                symbolToBuffer = False
            elif len(word)==1 and word[0] in operators :
                print >> f, "<{},{},{}>".format(operators[word[0]],nLine,y-1)
                mBuffer = []
                iniToken = y
            elif symbol == '#': ## SOLO APLICA FUERA DE UN STRING
                break
            elif symbolToBuffer:
                print >> f, 
        else:                 ## LEYENDO DENTRO DE STRING
            if not symbolToBuffer and symbol != '"' :
                mBuffer.append(symbol )
                        
        if symbolToBuffer  :
            mBuffer.append(symbol )
        elif dfaStrings.InInit() :
            iniToken +=1
        
if  not dfaStrings.InAccepting():
    pass # PRNT ERROR

f.close()
            




# print >> f, ("es: ", reserved ["while"])
# print >> f, ("es: ", operators["$"])
# for i in range(7):
#     for j in range(10):
#         print >> f, ("es: ",i, j, delta_num(i, str(j) ))
#     print >> f, ("punto: ",delta_num(i, '.'))
#     print >> f, ("otro: ",delta_num(i, '%'))

        



























