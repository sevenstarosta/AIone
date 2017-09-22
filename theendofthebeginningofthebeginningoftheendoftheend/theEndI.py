'''
Timothy Davison and Seven Starosta
tfd2xq sbs3bx
AI Homework 1
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
    k=0
    while k < len(rules):
        i,j = rules[k]
        if forwardCheck(i) and j not in facts.keys():
            facts[j]=learned[j][0]
            learned[j][1]=True
            k=-1
        k+=1

def exprToNames(expr):
    expr2 = ""
    i = 0
    while i < len(expr):
        if expr[i] not in ['(',')','&','|','!']:
            j=i
            while j < len(expr) and expr[j] not in ['(',')','&','|','!']:
                j+=1
            if expr[i:j] in roots.keys():
                expr2 = expr2 + roots[expr[i:j]][0]
            elif expr[i:j] in learned.keys():
                expr2 = expr2 + learned[expr[i:j]][0]
            i=j-1
        elif expr[i] in ['(',')']:
            expr2 = expr2 + expr[i]
        elif expr[i] == '&':
            expr2 = expr2 + " AND "
        elif expr[i] == '!':
            expr2 = expr2 + " NOT "
        elif expr[i] == '|':
            expr2 = expr2 + " OR "
        i+=1
    return expr2

def forwardCheck(expr):
    operands = []
    operators = []
    while len(expr) > 0:
        i = 0
        while (i < len(expr) and expr[i] not in ['(',')','&','|','!']):
            i+=1
        if i > 0: #Then there is an operand to be added to the stack.
            oper = expr[:i]
            operands.append(oper in facts.keys())
            if len(expr) > i:
                expr = expr[i:]
            else:
                expr = ""
        else: #Then the remainder is an operator or ()
            if expr[0] == '(':
                operators.append('(')
            elif expr[0] == '!':
                while (len(operators) > 0 and operators[-1] not in ['(',')','&','|']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        oparands.append(not b)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                operators.append('!')
            elif expr[0] == '&':
                while (len(operators) > 0 and operators[-1] not in ['(',')','|']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                operators.append('&')
            elif expr[0] == '|':
                while (len(operators) > 0 and operators[-1] not in ['(',')']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                operators.append('|')
            elif expr[0] == ')':
                while (len(operators) > 0 and operators[-1] not in ['(']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                operators.pop()
            if len(expr) > 1:
                expr = expr[1:]
            else:
                expr = ""
    while(len(operators) > 0):
        a = operators.pop()
        if a == '!':
            b = operands.pop()
            operands.append(not b)
        elif a == '&':
            b = operands.pop()
            c = operands.pop()
            operands.append(b and c)
        elif a == '|':
            b = operands.pop()
            c = operands.pop()
            operands.append(b or c)
    return operands[0]

def backward(expr):
    operands = []
    identifiers = [] #to be used for explanation
    operators = []
    answer = []
    while len(expr) > 0:
        i = 0
        while (i < len(expr) and expr[i] not in ['(',')','&','|','!']):
            i+=1
        if i > 0: #Then there is an operand to be added to the stack.
            oper = expr[:i]

            if oper in roots.keys() and roots[oper][1]:
                operands.append(True)
                identifiers.append(roots[oper][0])
                answer.append("I KNOW THAT IT IS TRUE THAT " + roots[oper][0])
            elif oper in roots.keys():
                operands.append(False)
                identifiers.append("NOT " + roots[oper][0])
                answer.append("I KNOW THAT IT IS NOT TRUE THAT " + roots[oper][0])
            else:
                val = False
                temp = []
                lastRule =""
                for rule,result in rules:
                    if result == oper:
                        lastRule = rule
                        val = val or backward(rule)[0]
                        temp = backward(rule)[1]
                        if val:
                            answer.append("BECAUSE " + exprToNames(rule) + " I KNOW THAT " + learned[oper][0])
                            answer= temp + answer
                            break
                operands.append(val)
                identifiers.append(learned[oper][0])
                if val == False:
                    if temp == []:
                        answer.append("I KNOW THAT IT IS NOT TRUE THAT "+ learned[oper][0])
                        answer= temp + answer
                    else:
                        answer.append("BECAUSE I CANNOT SAY THAT " + exprToNames(lastRule) + " I CANNOT PROVE " + learned[oper][0])
                        answer= temp + answer
            if len(expr) > i:
                expr = expr[i:]
            else:
                expr = ""
        else: #Then the remainder is an operator or ()
            if expr[0] == '(':
                operators.append('(')
            elif expr[0] == '!':
                while (len(operators) > 0 and operators[-1] not in ['(',')','&','|']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                        temp=identifiers.pop()
                        identifiers.append("NOT " + temp)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " AND " + iB)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " OR " + iB)
                operators.append('!')
            elif expr[0] == '&':
                while (len(operators) > 0 and operators[-1] not in ['(',')','|']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                        temp=identifiers.pop()
                        identifiers.append("NOT " + temp)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " AND " + iB)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " OR " + iB)
                operators.append('&')
            elif expr[0] == '|':
                while (len(operators) > 0 and operators[-1] not in ['(',')']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                        temp=identifiers.pop()
                        identifiers.append("NOT " + temp)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " AND " + iB)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " OR " + iB)
                operators.append('|')
            elif expr[0] == ')':
                while (len(operators) > 0 and operators[-1] not in ['(']):
                    a = operators.pop()
                    if a == '!':
                        b = operands.pop()
                        operands.append(not b)
                        temp=identifiers.pop()
                        identifiers.append("NOT " + temp)
                    elif a == '&':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b and c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " AND " + iB)
                    elif a == '|':
                        b = operands.pop()
                        c = operands.pop()
                        operands.append(b or c)
                        iA = identifiers.pop()
                        iB = identifiers.pop()
                        identifiers.append(iA + " OR " + iB)
                operators.pop()
                iA = identifiers.pop()
                identifiers.append("("+ iA + ")")
            if len(expr) > 1:
                expr = expr[1:]
            else:
                expr = ""
    while(len(operators) > 0):
        a = operators.pop()
        if a == '!':
            b = operands.pop()
            operands.append(not b)
            temp=identifiers.pop()
            identifiers.append("NOT " + temp)
        elif a == '&':
            b = operands.pop()
            c = operands.pop()
            operands.append(b and c)
            iA = identifiers.pop()
            iB = identifiers.pop()
            identifiers.append(iA + " AND " + iB)
        elif a == '|':
            b = operands.pop()
            c = operands.pop()
            operands.append(b or c)
            iA = identifiers.pop()
            iB = identifiers.pop()
            identifiers.append(iA + " OR " + iB)
    if operands[0]:
        answer.append("THUS I KNOW " + identifiers[0])
    else:
        answer.append("THUS I CANNOT SAY THAT " + identifiers[0])
    return operands[0], answer

def query(variable):
    value, explanation = backward(variable)
    print(str(value[0]).lower())

def why(variable):
    value, explanation = backward(variable)
    print (str(value).lower())
    for line in explanation:
        print(line)

def list():
    print ("Root Variables: ")
    for i in roots.keys():
        if roots[i][1]:
            print ("     " + i + " = \""+ roots[i][0]+ "\"")
    print("\n")
    print ("Learned Variables: ")
    for i in learned.keys():
        if learned[i][1]:
            print ("     " + i + " = \"" + learned[i][0] + "\"")
    print("\n")
    print("Facts: ")
    for i in facts.keys():
        print("     " + i)
    print("\n")
    print("Rules: ")
    for i,j in rules:
        print("     " + i + " -> " + j)
    print("\n")

while (True):
    myInput = input(">")
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
        query(sInput[1])
    if sInput[0] == "Why":
        why(sInput[1])
