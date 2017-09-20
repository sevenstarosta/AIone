'''
Timothy Davison and Seven Starosta
Yeeeeeeeeeeahhhhhhh boiiiiiii
9-17-2017
'''

# Attributes
facts = {}
rules = []
roots = {}
learned = {}

# Functions
def teach_variable(arg, identifier, name):
    if (arg == "-R"):
        roots[identifier] = [name,False]
    else:
        learned[identifier] = [name, False]

def teach_root(identifier, value):
    if value == "true":
        value = True
    else:
        value = False
    if identifier not in roots.keys():
        print ("Don't touch my roots")
    else:
        roots[identifier][1] = value

def teach_rule(rule,result):
    rules.append((rule,result))

def learn():
    facts.clear()
    for i in roots.keys():
        if roots[i][1]:
            facts[i]=roots[i][0]
    for i,j in rules:
        if forwardCheck(i):
            facts[j]=learned[j][0]
            learned[j][1]=True
        #verify if conditions of i met.

def forwardCheck(expr):
    if (expr.find('(') == 0):
        i=0 #will hold location of closing parentheses
        j=1 #count of unclosed sets of parentheses
        while(i < len(expr) - 1 and j > 0):
            i+= 1
            if expr[i] == '(':
                j+=1
            elif expr[i] == ')':
                j-=1
        if i == len(expr) -1:
            return forwardCheck(expr[1:i-1])
        elif expr[i+1] == '&': #there is some expression to the right
            return forwardCheck(expr[1:i-1]) and forwardCheck(expr[i+2:])
        else: # there is an or
            return forwardCheck(expr[1:i-1]) or forwardCheck(expr[i+2:])
    if (expr.find('(') > 0):
        if expr[expr.find('(')-1] == '!':
            return not forwardCheck(expr[expr.find('('):])
        elif expr[expr.find('(')-1] == '&':
            return forwardCheck(expr[:expr.find('(')-1]) and forwardCheck(expr[expr.find('('):])
        elif expr[expr.find('(')-1] == '|':
            return forwardCheck(expr[:expr.find('(')-1]) or forwardCheck(expr[expr.find('('):])

    if (expr.find("!") == -1 and expr.find("&") == -1 and expr.find("|") == -1): #Should just be a variable. see if in facts
        return expr in facts.keys()
    #need to separate based on parentheses, going out in. Should use stack?
    index = expr.find("!")
    if (index == 0):
        #have to actually evaluate the thing being negated before
        if (expr.find('&') > 0 and expr.find('&') < expr.find('|')):
            return (not forwardCheck(expr[1:expr.find('&')])) and forwardCheck(expr[expr.find('&')+1:])
        if (expr.find('|') > 0):
            return (not forwardCheck(expr[1:expr.find('|')])) or forwardCheck(expr[expr.find('|')+1:])
        return not forwardCheck(expr[1:])
    if (index > 0):
        if expr[index-1] == '&': # go to case above....
            if (expr[index:].find('&') > 0 and expr[index:].find('&') < expr[index:].find('|')):
                return forwardCheck(expr[:index-1]) and (not forwardCheck(expr[index+1:expr[index:].find('&')+index]) and forwardCheck(expr[expr[index:].find('&')+index+1:]))
            if (expr[index:].find('|') > 0):
                return forwardCheck(expr[:index-1]) and (not forwardCheck(expr[index+1:expr[index:].find('|')+index])) or forwardCheck(expr[expr[index:].find('|')+index+1:])
            return forwardCheck(expr[:index-1]) and not forwardCheck(expr[1:])
            #return forwardCheck(expr[:index-1]) and not forwardCheck(expr[index+1:])
        elif expr[index-1] == '|':
            if (expr[index:].find('&') > 0 and expr[index:].find('&') < expr[index:].find('|')):
                return forwardCheck(expr[:index-1]) or (not forwardCheck(expr[index+1:expr[index:].find('&')+index])) and forwardCheck(expr[expr[index:].find('&')+index+1:])
            if (expr[index:].find('|') > 0):
                return forwardCheck(expr[:index-1]) or (not forwardCheck(expr[index+1:expr[index:].find('|')+index])) or forwardCheck(expr[expr[index:].find('|')+index+1:])
            return forwardCheck(expr[:index-1]) or not forwardCheck(expr[1:])
    index = expr.find('&')
    if (index >0):
        return forwardCheck(expr[:index]) and forwardCheck(expr[index+1:])
    index = expr.find('|')
    if index > 0:
        return forwardCheck(expr[:index]) or forwardCheck(expr[index+1:])
    return false


def query(variable):
    pass

def why(variable):
    pass

def list():
    print ("Root Variables: ")
    for i in roots.keys():
        "MUST REMOVE THE BOOLEAN AT THE END. JUST FOR TESTING."
        print ("     " + i + " = \""+ roots[i][0]+ "\" " + str(roots[i][1]))
    print ("\n")
    print ("Learned Variables: ")
    for i in learned.keys():
        print ("     " + i + " = \"" + learned[i][0] + "\" " + str(learned[i][1]))
    print ("\n")
    print("Facts: ")
    for i in facts.keys():
        print ("     " + i)
    print ("\n")
    print("Rules: ")
    for i,j in rules:
        print ("     " + i + " -> " + j)

while (True):
    myInput = input("Enter: ")
    if myInput == "quit": break
    sInput = myInput.split()
    if sInput[0] == "Teach":
        if sInput[1] == "-R" or sInput[1] == "-L": #TEACHING ROOT VARIABLE
            #indices = [index for index, c in enumerate(myInput) if c == chr(34)]
            index = myInput.index(chr(34))
            index2 = myInput[index+1:].index(chr(34)) +index+1
            teach_variable(sInput[1], sInput[2], myInput[index+1:index2])
        elif "->" in sInput: #TEACHING EXPRESSION
            teach_rule(sInput[1], sInput[3])
        else: # teaching root variable
            teach_root(sInput[1], sInput[3])
    if sInput[0] == "List":
        list()
    if sInput[0] == "Learn":
        learn()
    if sInput[0] == "Query":
        query(sInput(1))
    if sInput[0] == "Why":
        why(sInput(1))
