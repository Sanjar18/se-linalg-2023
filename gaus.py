def gauss(am, bm):
    n = len(am)
    indices = list(range(n))
    for fd in range(n):
        try:
            fdScaler = 1.0 / am[fd][fd]
        except ZeroDivisionError:
            print('Нет решений')
            exit()
        for j in range(n):
            am[fd][j] *= fdScaler
        bm[fd][0] *= fdScaler
        for i in indices[0:fd] + indices[fd + 1:]:
            crScaler = am[i][fd]
            for j in range(n):
                am[i][j] = am[i][j] - crScaler * am[fd][j]
            bm[i][0] = bm[i][0] - crScaler * bm[fd][0]
    return bm

def rank_of_matrix(matrix):
    rank = min(len(matrix), len(matrix[0]))
    row_index = 0
    for i in range(len(matrix[0])):
        found_nonzero = False
        for j in range(row_index, len(matrix)):
            if matrix[j][i] != 0:
                found_nonzero = True
                matrix[row_index], matrix[j] = matrix[j], matrix[row_index]
                break
        if found_nonzero:
            for j in range(row_index + 1, len(matrix)):
                factor = matrix[j][i] / matrix[row_index][i]
                for k in range(i, len(matrix[0])):
                    matrix[j][k] -= matrix[row_index][k] * factor
            row_index += 1
    return rank


def infinite_solutions_check(A, b):
    matrix_AB = [list(row_A) + [elem_b][0] for row_A, elem_b in zip(A, b)]

    rank_A = rank_of_matrix(A)
    rank_AB = rank_of_matrix(matrix_AB)
    num_variables = len(A[0])

    if (rank_A == rank_AB) and (rank_AB < num_variables):
        return True
    else:
        return False


A = [[23, 57], [14, 34]]
B = [[-22], [-32]]


# print(gauss(A, B))
