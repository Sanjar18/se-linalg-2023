import sys
import copy
from transform_express import normalize_expression
from gaus import gauss, infinite_solutions_check


def print_matrix(m):
    k = 1
    for row in m:
        print(f'x{k} = {row[0]}')
        k += 1


def multiplicationMatrix(a, b):
    str_A, cols_A = len(a), len(a[0])
    str_B, cols_B = len(b), len(b[0])

    if cols_A != str_B:
        print('Некорректный ввод1')
        sys.exit()
    result = [[0 for _ in range(cols_B)] for _ in range(str_A)]
    for s in range(str_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[s][j] += a[s][k] * b[k][j]
    return result


def multOnNumber(mat, num):
    result = [[mat[y][x] * num for x in range(len(mat[0]))] for y in range(len(mat))]
    return result


def SlMat(A, B):
    str_A, cols_A = len(A), len(A[0])
    str_B, cols_B = len(B), len(B[0])
    if str_A != str_B or cols_A != cols_B:
        print('Некорректный ввод')
        sys.exit()
    result_data = [[A[i][j] + B[i][j] for j in range(cols_A)] for i in range(str_A)]
    return result_data


def transformParse(matrix, exspressions):
    m = matrix
    a = []
    for i in exspressions:
        n = i.replace('x', '')
        if len(n) == 1:
            if not a:
                a= m[n]
            else:
                a = SlMat(a, m[n])
            continue

        k = 0
        while '[-1]' in n:
            n = n.replace('[-1]', '', 1)
            k += 1
        if k % 2 > 0:
            z = 1
            prom = multOnNumber(m[n[0]], -1)
        else:
            z = 2
            if n[0].isdigit() or n[1].isdigit():
                if n[0].isdigit() and n[1].isdigit():
                    prom = [int(n[0]) * int(n[1])]
                elif n[0].isdigit():
                    prom = multOnNumber(m[n[1]], int(n[0]))
                else:
                    prom = multOnNumber(m[n[0]], int(n[1]))
            else:
                prom = multiplicationMatrix(m[n[0]], m[n[1]])
        for j in n[z:]:
            if type(prom[0]) == int:
                if j.isdigit():
                    prom = [prom[0] * int(j)]
                else:
                    prom = multOnNumber(m[n[0]], prom[0])
            else:
                if j.isdigit():
                    prom = multOnNumber(prom, int(j))
                else:
                    prom = multiplicationMatrix(prom, m[j])
        if not a:
            a = prom
        else:
            a = SlMat(a, prom)
    return a


def makeslay(matrix, text):
    withx, without = normalize_expression(text)
    # print(withx, without)
    a = transformParse(matrix, withx)
    b = multOnNumber(transformParse(matrix, without), -1)
    c = copy.deepcopy(a)
    d = copy.deepcopy(b)
    if infinite_solutions_check(c, d):
        print('Бесконечное количество решений')
        exit()
    print_matrix(gauss(a, b))


def ReadFile(filename):
    try:
        with open(filename) as f:
            file = f.readlines()
    except Exception as e:
        print('Некорректное имя фаила')
        sys.exit()
    text = file[0].strip()
    matrixLetters = list()
    vectorLetters = list()
    for i in text:
        if i.isupper():
            if i not in matrixLetters:
                matrixLetters.append(i)
        elif i.islower():
            if i not in vectorLetters and i != "x":
                vectorLetters.append(i)
    matrix = dict()
    file.pop(0)
    for i in range(len(matrixLetters)):
        mat = []
        mat1 = []
        a = list(map(int, file[0].split()))
        file.pop(0)
        if len(a) == 1:
            n = a[0]
        else:
            n = a[1]
        for j in range(n):
            mat.append(list(map(int, file[0].split())))
            file.pop(0)
            for x in range(len(mat[0])):
                prom = []
                for y in range(len(mat)):
                    prom.append(mat[y][x])
                mat1.append(prom)
            matrix[matrixLetters[i]] = mat1
            mat1 = []
    for i in range(len(vectorLetters)):
        file.pop(0)
        matrix[vectorLetters[i]] = [[x] for x in list(map(int, file[0].split()))]
        file.pop(0)
    makeslay(matrix, text)


ReadFile('text2')
