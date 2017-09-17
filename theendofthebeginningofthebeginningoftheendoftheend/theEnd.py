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

def teach_root(value, identifier):
    if value == "true":
        value = True
    else:
        value = False
    if identifier not in roots.keys():
        print ("Don't touch my roots")
    else:
        roots[identifier][1] = value

def teach_rule(rule):
    rules.apppend(rule)

def list():
    print ("Root Variables: ")
    for i in roots:
        print ("     " + i + "= " + roots[i][0])
    print ("\n")
    print ("Learned Variables: ")
    for i in learned:
        print ("     " + i + "= " + learned[i][0])
    print ("\n")
    print("Facts: ")
    for i in facts:
        print ("     " + i)
    print ("\n")
    for i in rules:
        print ("     " + i)

while (True):
    myInput = input("Enter stuff")
    if myInput == "quit": break
    sInput = myInput.split()
    if sInput[0] == "Teach":
        if sInput[1] == "-R":
            teach_root(sInput[4], sInput[2])
        elif sInput[1] == "-L":
            teach_variable(sInput[4], sInput[2])
        elif sInput[1] == "S":
            teach_rule(sInput[3])






