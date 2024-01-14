from numpy import diag, array, linalg, zeros

def solve_linear_system(expression):
    variables = []
    sizes = []
    matrices = {}
    vectors = {}

    for char in expression:
        if char.isupper():
            m, n = map(int, input(f"Введите размеры матрицы {char}: ").split())
            matrix = []
            for _ in range(m):
                row = list(map(float, input().split()))
                matrix.append(row)
            matrices[char] = array(matrix)
        elif char.islower() and char != 'x' and char not in vectors:
            n = int(input(f"Введите размер вектора {char}: "))
            vector = list(map(float, input().split()))
            vectors[char] = array(vector)

    for char in expression:
        if char == 'x':
            variables.append(char)
        elif char.islower() and char != 'x':
            sizes.append(len(vectors[char]) if char in vectors else 1)

    augmented_matrix = build_augmented_matrix(expression, matrices, vectors)

    if check_inconsistency(augmented_matrix, len(variables), sizes):
        print("Система не имеет решений.")
    elif check_infinite_solutions(augmented_matrix, len(variables), sizes):
        print("Система имеет бесконечное количество решений.")
    else:
        solutions = linalg.solve(augmented_matrix[:, :-1], augmented_matrix[:, -1])
        result = ', '.join([f'{variables[i]} = {solutions[i]}' for i in range(len(variables))])
        print(result)


def build_augmented_matrix(expression, matrices, vectors):
    used_matrices = set()
    used_vectors = set()

    rows = max([len(matrices[char]) if char.isupper() and char not in used_matrices else len(vectors[char]) if char.islower() and char not in used_vectors else 1 for char in expression if char.isalpha()], default=1)
    cols = sum([len(matrices[char][0]) if char.isupper() and char not in used_matrices else len(vectors[char]) if char.islower() and char not in used_vectors else 1 for char in expression if char.isalpha()])

    augmented_matrix = zeros((rows, cols + 1))
    col_index = 0

    for char in expression:
        if char.isupper() and char not in used_matrices:
            matrix = matrices[char]
            rows, cols = matrix.shape
            augmented_matrix[:rows, col_index:col_index + cols] = matrix
            used_matrices.add(char)
        elif char.islower() and char != 'x' and char not in used_vectors:
            vector = vectors[char] if char in vectors else array([1])
            size = len(vector)
            augmented_matrix[:size, col_index:col_index + size] = diag(vector)
            used_vectors.add(char)

        col_index += len(vector)

    return augmented_matrix


def check_inconsistency(augmented_matrix, num_variables, sizes):
    return linalg.matrix_rank(augmented_matrix[:, :-1]) < linalg.matrix_rank(
        augmented_matrix[:, :-1][:, :num_variables])


def check_infinite_solutions(augmented_matrix, num_variables, sizes):
    return linalg.matrix_rank(augmented_matrix[:, :-1]) < num_variables

# Пример использования
expression = "BAc + DAx + Cc"
solve_linear_system(expression)
