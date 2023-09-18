import re


def strategy_if(instructions: [str], global_i, ant, walls):

    pass_if = eval(instructions[global_i][3:-1], globals(), locals())
    j = 0

    instructions = instructions[:global_i] + instructions[global_i + 1:]
    while instructions[j+global_i].startswith(" "):
        if pass_if:
            instructions[j + global_i] = instructions[j + global_i][2:]
        else:
            instructions = instructions[:j + global_i] + instructions[j + global_i + 1:]
            global_i -= 1
        j += 1
    return instructions


def strategy_while(instructions: [str], global_i, ant, walls):
    pass_if = eval(instructions[global_i][6:-1], globals(), locals())
    sub_arr = []
    start = global_i
    end = global_i
    if not pass_if:
        instructions = instructions[:global_i] + instructions[global_i + 1:]
        while instructions[global_i].startswith(" "):
            del instructions[start:end + 1]
        return instructions

    while instructions[global_i+1].startswith(" "):
        global_i += 1
        if pass_if:
            sub_arr.append(instructions[global_i][2:])
        else:
            del instructions[start:end + 1]
        if global_i+1 >= len(instructions):
            break
    if pass_if:
        instructions = instructions[:start] + sub_arr + instructions[start:]

    return instructions


def strategy_for(instructions: [str], global_i, ant, walls):
    #TODO utilizar iterador
    n = re.search(r'for \w+ in range\((\d+)\):', instructions[global_i])
    n_int = int(n.group(1))

    sub_arr = []
    start = global_i
    end = global_i

    while instructions[global_i+1].startswith(" "):
        global_i += 1
        sub_arr.append(instructions[global_i][2:])


    if n_int == 1:
        instructions = instructions[:start] + instructions[start+1:]

        while instructions[start].startswith(" "):
            del instructions[start:end + 1]

        instructions = instructions[:start] + sub_arr + instructions[start:]
        return instructions

    instructions[start] = 'for _ in range(' + str(n_int - 1) + '):'
    instructions = instructions[:start] + sub_arr + instructions[start:]
    return instructions


