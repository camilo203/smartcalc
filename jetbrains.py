from string import ascii_letters as abc
from collections import deque

dic = {}
operands = ["*", "(", ")", "+", "-", "^", "/"]
precedence = {"-": 1, "+": 1, "*": 2, "/": 2, "^": 3, "(": 4}


def tipo(x):
    if len(x) > 0:
        if "=" in x:
            return "Asign"
        elif x.strip()[0] == "/":
            return "Command"
        elif "+" in x or "-" in x or "*" in x or "/" in x or "^" in x:
            return "Operation"
        elif len(x.split()) == 1:
            return "Variable"


def sum(a, b):
    return float(a) + float(b)


def difference(a, b):
    return float(a) - float(b)


def multiply(a, b):
    return float(a) * float(b)


def divide(a, b):
    return float(a) / float(b)


def power(a, b):
    return float(a) ** float(b)


def asign(x):
    global dic
    if len(x) == 2:
        for i in x[0]:
            if i not in abc:
                print("Invalid identifier")
                break
        else:
            try:
                value = int(x[1])
                dic[x[0]] = value
            except:
                for i in x[1]:
                    if i not in abc:
                        print("Invalid assignment")
                        break
                else:
                    if x[1] in dic:
                        dic[x[0]] = dic[x[1]]
                    else:
                        print("Unknown variable")
    else:
        print("Invalid assignment")


def command(x):
    if x in ["/exit", "/help"]:
        if x == "/exit":
            print("Bye!")
            exit()
        else:
            print("Este programa permite sumar y restar, ademas almacena variables")

    else:
        print("Unknown command")


def evaluate(x):
    try:
        return int(x)
    except:
        if x in dic:
            return fetch(x)
        else:
            return "Unknown variable"


def parenthesis(x):
    queue = deque()
    for i in x:
        if i == "(":
            queue.append(i)
        elif i == ")" and len(queue) > 0:
            if queue[-1] == "(":
                queue.pop()
        elif i == ")":
            queue.append(i)
    if len(queue) != 0:
        return False
    return True


def isinteger(x):
    try:
        int(x)
        return True
    except:
        return False


def totalsep(x):
    ls = []
    new = x.replace(" ", "")
    act = ""
    for j, i in enumerate(new):
        if i in operands:
            ls.append(act.strip())
            act = ""
            ls.append(i)
        else:
            act += i
        if j == len(new)-1:
            ls.append(act)
    return list(filter(lambda x: x != "", ls))


def infixtopfix(ls):
    output = deque()
    stack = deque()
    for i in ls:
        if i.isalpha() or isinteger(i):
            output.append(i)
        else:
            if i == "(":
                stack.appendleft(i)
            elif i == ")":
                while True:
                    val = stack[0]
                    if stack[0] != "(":
                        output.append(stack.popleft())
                    else:
                        stack.popleft()
                        break
            else:
                if len(stack) > 0:
                    value = precedence[i]
                    if value <= precedence[stack[0]]:
                        while True:
                            if len(stack) == 0:
                                stack.appendleft(i)
                                break
                            val = stack[0]
                            if val == "(":
                                stack.appendleft(i)
                                break
                            elif value <= precedence[val]:
                                output.append(stack.popleft())
                            else:
                                stack.appendleft(i)
                                break

                    else:
                        stack.appendleft(i)
                else:
                    stack.appendleft(i)
    if len(stack) > 0:
        output.extend(stack)

    return deque(map(lambda x: str(dic[x]) if x in dic else x, output))


def value(x: deque):
    result = []

    while True:
        if len(x) > 0:
            if x[0].isalpha():
                return False
            elif isinteger(x[0]):
                result.append(x.popleft())
            else:
                b, a = result.pop(), result.pop()
                if x[0] == "+":
                    result.append(sum(a, b))
                elif x[0] == "-":
                    result.append(difference(a, b))
                elif x[0] == "*":
                    result.append(multiply(a, b))
                elif x[0] == "^":
                    result.append(power(a, b))
                else:
                    result.append(divide(a, b))
                x.popleft()
        else:
            break
    if len(result) > 1:
        return "Invalid Expression"
    else:
        if result[0] == int(result[0]):
            return int(result[0])
        else:
            return result[0]


def fetch(x):
    return dic[x]


while True:
    valor = input()
    val = tipo(valor)
    if val == "Asign":
        x = list(map(lambda e: e.strip(), valor.split("=")))
        asign(x)
    elif val == "Command":
        command(valor)
    elif val == "Variable":
        for i in valor.strip():
            if i not in abc:
                print("Invalid identifier")
                break
        else:
            if valor.strip() in dic:
                print(dic[valor.strip()])
            else:
                print("Unknown variable")
    elif val == "Operation":
        if parenthesis(valor):
            try:
                x = value(infixtopfix(totalsep(valor)))
                if str(x) == "False":
                    print("Invalid Variable")
                else:
                    print(x)
            except:
                print("Invalid expression")
        else:
            print("Invalid expression")
