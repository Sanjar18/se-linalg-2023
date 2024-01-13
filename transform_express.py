def normalize_expression(expression):
    expression = expression.replace(' ', '')
    expression = expression.replace('-', '+[-1]')
    if '=' in expression:
        expression = expression.replace('=', '+[-1](') + ')'
    withX = []
    withoutX = []
    string = ''
    flag = False
    for i in range(0, len(expression)):
        if expression[i].isalpha() or expression[i].isdigit() or expression[i] in '-[]':
            string += expression[i]
        else:
            if expression[i] in '()':
                flag = not flag
                string += expression[i]
                if i == len(expression) - 1:
                    if '(' in string:
                        opened = open_brackets(string)
                        [withX.append(x) if 'x' in x else withoutX.append(x) for x in opened]
                    elif 'x' in string:
                        withX.append(string)
                    else:
                        withoutX.append(string)
            elif flag:
                string += expression[i]
            if not flag and expression[i] == '+':
                if '(' in string:
                    opened = open_brackets(string)
                    [withX.append(x) if 'x' in x else withoutX.append(x) for x in opened]
                else:
                    if 'x' in string:
                        withX.append(string)
                    else:
                        withoutX.append(string)
                string = ''
    if '(' not in expression:
        if 'x' in string:
            withX.append(string)
        else:
            withoutX.append(string)
    return [withX, withoutX]


def open_brackets(expression):
    exsp = ''
    exsp2 = ''
    other = ''
    flag = True
    k = 0
    for i in expression:
        if i in '()':
            flag = not flag
            if flag:
                k = 1
        elif not flag:
            other += i
        elif flag:
            if k == 0:
                exsp += i
            else:
                exsp2 += i
    return [exsp + x +exsp2 for x in other.split('+')]

# print(normalize_expression("BAc+DACx+Cc"))