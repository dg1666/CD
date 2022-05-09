gram = {"E":["2E2","3E3","4"]}
starting_terminal = "E"
inp = "2324232$"

stack = "$"
print(f'{"Stack": <5}'+"|"+f'{"Input": <5}'+"|"+f'Action')
print(f'{"-":-<20}')

while True:
    action = True
    i = 0
    while i<len(gram[starting_terminal]):
        if gram[starting_terminal][i] in stack:
            stack = stack.replace(gram[starting_terminal][i],starting_terminal)
            print(f'{stack: <5}'+"|"+f'{inp: <5}'+"|"+f'Reduce S->{gram[starting_terminal][i]}')
            i=-1
            action = False
        i+=1
    if len(inp)>1:
        stack+=inp[0]
        inp=inp[1:]
        print(f'{stack: <5}'+"|"+f'{inp: <5}'+"|"+f'Shift')
        action = False

    if inp == "$" and stack == ("$"+starting_terminal):
        print(f'{stack: <5}'+"|"+f'{inp: <5}'+"|"+f'Accepted')
        break

    if action:
        print(f'{stack: <5}'+"|"+f'{inp: <5}'+"|"+f'Rejected')
        break






