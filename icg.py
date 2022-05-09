#ICG- TAC,Quadruple,Triple,Indirect Triple
Symbols = set(['+', '-', '*', '/', '(', ')'])
Case = {'+': 1, '-': 1, '*': 2, '/': 2}

def infix_to_postfix(cond):
    stk=[]
    opt=''
    for x in cond:
        if x not in Symbols:
            opt +=x
        elif x == '(':
            stk.append('(')
        elif x == ')':
            while stk and stk[-1] != '(':
                opt += stk.pop()
            stk.pop()
        else:
            while stk and stk[-1] != '(' and PRI[x] <= PRI[stk[-1]]:
                opt += stk.pop()
            stk.append(x)
   
    while stk:
        opt += stk.pop()
    print(f'POSTFIX: {opt}')
    return opt

def infix_to_prefix(cond):
    op_stk=[]
    exp_stk=[]
    for x in cond:
        if not x in Symbols:
            exp_stk.append(x)
        elif x == '(':
            op_stk.append(x)
        elif x == ')':
            while op_stk[-1] != '(':
                op=op_stk.pop()
                p=exp_stk.pop()
                q=exp_stk.pop()
                exp_stk.append(op+q+p)
            op_stk.pop()  
        else:
            while op_stk and op_stk[-1] != '(' and PRI[x] <= PRI[op_stk[-1]]:
                op=op_stk.pop()
                p=exp_stk.pop()
                q=exp_stk.pop()
                exp_stk.append(op+q+p)
            op_stk.append(x)


    while op_stk:
        op=op_stk.pop()
        p=exp_stk.pop()
        q=exp_stk.pop()
        exp_stk.append(op+q+p)
    print(f'PREFIX: {exp_stk[-1]}')
    return exp_stk[-1]

def TAC(pos):
    print("Three Address Code:")
    exp_stk=[]
    temp=1

    for i in pos:
        if i not in Symbols:
            exp_stk.append(i)
        else:
            print(f't{temp} := {exp_stk[-2]} {i} {exp_stk[-1]}')
            exp_stk=exp_stk[:-2]
            exp_stk.append(f't{temp}')
            temp += 1


exp=input("Enter Expression: ")
pre=infix_to_prefix(exp)
pos=infix_to_postfix(exp)
TAC(pos)

def Quadruple(pos):
    stk=[]
    op=[]
    x=1
    for i in pos:
        if i not in Symbols:
            stk.append(i)
        elif i == '-':
            op1 = stk.pop()
            stk.append("t(%s)" % x)
            print("{0:^4s} | {1:^4s} | {2:^4s}|{3:4s}".format(
                i, op1, "(-)", " t(%s)" % x))
            x=x+1
            if stk!=[]:
                op2=stk.pop()
                op1=stk.pop()
                print("{0:^4s} | {1:^4s} | {2:^4s}|{3:4s}".format(
                    "+", op1, op2, " t(%s)" % x))
                stk.append("t(%s)" % x)
                x=x+1
        elif i == '=':
            op2=stk.pop()
            op1=stk.pop()
            print("{0:^4s} | {1:^4s} | {2:^4s}|{3:4s}".format(i, op2, "(-)", op1))
        else:
            op1=stk.pop()
            op2=stk.pop()
            print("{0:^4s} | {1:^4s} | {2:^4s}|{3:4s}".format(
                i, op2, op1, " t(%s)" % x))
            stk.append("t(%s)" % x)
            x=x+1

def Triple(pos):
    stk=[]
    op=[]
    x=0
    for i in pos:
        if i not in Symbols:
            stk.append(i)
        elif i == '-':
            op1=stk.pop()
            stk.append("(%s)" % x)
            print("{0:^4s} | {1:^4s} | {2:^4s}".format(i, op1, "(-)"))
            x=x+1
            if stk != []:
                op2=stk.pop()
                op1=stk.pop()
                print("{0:^4s} | {1:^4s} | {2:^4s}".format("+", op1, op2))
                stk.append("(%s)" % x)
                x=x+1
        elif i == '=':
            op2=stk.pop()
            op1=stk.pop()
            print("{0:^4s} | {1:^4s} | {2:^4s}".format(i, op1, op2))
        else:
            op1=stk.pop()
            if stk != []:
                op2=stk.pop()
                print("{0:^4s} | {1:^4s} | {2:^4s}".format(i, op2, op1))
                stk.append("(%s)" % x)
                x=x+1

def IndirectTriple(pos):
    stk=[]
    op=[]
    x=0
    ch=0
    for i in pos:
        if i not in Symbols:
            stk.append(i)
        elif i == '-':
            op1=stk.pop()
            stk.append("(%s)" % x)
            print("{0:^4s} | {1:^4s} | {2:^4s} | {3:^5d}".format(i, op1, "(-)", ch))
            x=x+1
            if stack != []:
                op2=stk.pop()
                op1=stk.pop()
                print("{0:^4s} | {1:^4s} | {2:^4s} | {3:^5d}".format(
                    "+", op1, op2, ch))
                stk.append("(%s)" % x)
                x=x+1
                ch=ch+1
        elif i == '=':
            op2=stk.pop()
            op1=stk.pop()
            print("{0:^4s} | {1:^4s} | {2:^4s} | {3:^5d}".format(i, op1, op2, ch))
            ch=ch+1
        else:
            op1=stk.pop()
            if stk != []:
                op2=stk.pop()
                print("{0:^4s} | {1:^4s} | {2:^4s} | {3:^5d}".format(
                    i, op2, op1, ch))
                stk.append("(%s)" % x)
                x=x+1
                ch=ch+1

print("Quadruple: ")
print("Op   | Src1 | Src2| Res")
Quadruple(pos)
print("Triple: ")
print("Op   | Src1 | Src2")
Triple(pos)
print("Indirect Triple: ")
print("Op   | Src1 | Src2 |Statement")
IndirectTriple(pos)

# Enter Expression: A=B+C/D*E
# Prefix: +B*/CDE
# Postfix: A=BCD/E*+
# Three Address Code:
# t1 := C / D
# t2 := t1 * E
# t3 := B + t2
# Quadruple: 
# Op   | Src1 | Src2| Res
#  /   |  C   |  D  | t(1)
#  *   | t(1) |  E  | t(2)
#  +   |  B   | t(2)| t(3)
# Triple: 
# Op   | Src1 | Src2
#  /   |  C   |  D  
#  *   | (0)  |  E  
#  +   |  B   | (1) 
# Indirect Triple: 
# Op   | Src1 | Src2 |Statement
#  /   |  C   |  D   |   0  
#  *   | (0)  |  E   |   1  
#  +   |  B   | (1)  |   2  