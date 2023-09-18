from resources.json import read_code_rules


def translate_instructions(instructions) -> [str]:
    rules_dict = read_code_rules()
    result = []

    for instruction in instructions:
        indentation = ''

        while instruction.startswith('  '):
            indentation += '  '
            instruction = instruction[2:]

        if instruction.startswith("while "):
            condition = instruction[len("while "):]
            if condition == '':
                condition = 'True'
            result.append(f"{indentation}while {condition}:")
            continue

        if instruction.startswith("if "):
            condition = instruction[len("if "):]
            result.append(f"{indentation}if {condition}:")
            continue

        if instruction.startswith("for "):
            value = instruction[len("for "):]
            result.append(f"{indentation}for _ in range({value}):")
            continue

        if instruction in rules_dict:
            result.append(indentation + rules_dict[instruction])
        else:
            return ['ERROR', f"Syntax error: '{instruction}' is not a valid instruction."]

    return result
