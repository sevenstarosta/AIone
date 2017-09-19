'''
Timothy Davison and Seven Starosta
Yeeeeeeeeeeahhhhhhh boiiiiiii
9-17-2017
'''

# Attributes
facts = []
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
    facts = []
    for i in roots.keys():
        if roots[i][1]:
            facts.append(i)
    #now do forward chaining on expressions...
    #need to parse expression
    for i,j in rules:
        if forwardCheck(i):
            fact.append(j)
        #verify if conditions of i met.

def forwardCheck(expr):(
    if (expr.find("!") == -1 and expr.find("&") == -1 and expr.find("|") == -1)): #Should just be a variable. see if in facts"
        return expr in facts.keys()
    #need to separate based on parentheses, going out in. Should use stack?
    index = expr.find("!")
    return false


def query(variable):
    pass

def why(variable):
    pass

def list():
    print ("Root Variables: ")
    for i in roots.keys():
        print ("     " + roots[i][0] + " = " + str(roots[i][1]))
    print ("\n")
    print ("Learned Variables: ")
    for i in learned.keys():
        print ("     " + learned[i][0] + " = " + str(learned[i][1]))
    print ("\n")
    print("Facts: ")
    for i in facts:
        print ("     " + i)
    print ("\n")
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
    if sInput[0] == "Why"
        why(sInput(1))
