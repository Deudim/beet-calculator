import numpy as np
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
import time

# Декоратор для измерения времени выполнения функций
def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Время выполнения функции '{func.__name__}': {(end_time - start_time) * 1e9} наносекунд")
        return result

    return wrapper


# Функция выполнения Венгерского алгоритма
#@calculate_time
def hungarian(matrix, target='min'):
    matrix = np.array(matrix)
    kf = 1
    if target == 'max':
        kf = -1
    matrix = kf * matrix
    row_ind, col_ind = linear_sum_assignment(
        matrix)  # Венгерский метод (https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.optimize.linear_sum_assignment.html)
    res = matrix[row_ind, col_ind].sum()
    return {'result': float(kf * res),
            'rows': row_ind.tolist(),
            'cols': col_ind.tolist()
            }

# Функция выполнения алгоритма Мака
#@calculate_time
def munkres(matrix, target='min'):
    kf = 1
    if target == 'max':
        kf = -1
    matrix = multiply_matrix_(matrix, kf)
    m = Munkres()  # Метод Мака https://software.clapper.org/munkres/
    indexes = m.compute(matrix)
    res = 0
    row_ind = []
    col_ind = []
    for row, column in indexes:
        value = matrix[row][column]
        res += value
        row_ind.append(row)
        col_ind.append(column)
    return {'result': float(kf * res),
            'rows': row_ind,
            'cols': col_ind
            }


# Функция выполнения жадного алгоритма
#@calculate_time
def greedy(matrix, target='min'):
    matrix = np.array(matrix)
    kf = 1
    if target == 'max':
        kf = -1
    matrix = kf * matrix
    row_ind, col_ind = _greedy_assignment(
        matrix)
    res = matrix[row_ind, col_ind].sum()
    return {'result': float(kf * res),
            'rows': row_ind,
            'cols': col_ind
            }

# Умножение матрицы на число
def multiply_matrix_(matrix, a):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= a
    return matrix


# Жадный алгоритм для задачи о назначениях
def _greedy_assignment(matrix):
    """
    жадная
    """
    num_rows, num_cols = matrix.shape
    if num_rows != num_cols:
        raise ValueError("num rows must me match num cols")
    assignments_row = []
    assignments_col = []

    # Создаем копию матрицы для работы
    temp_matrix = np.copy(matrix)

    for i in range(num_rows):
        min_col_index = i

        min_row_index = np.argmin(temp_matrix[:, min_col_index])

        assignments_row.append(min_row_index)
        assignments_col.append(min_col_index)

        # Для исключения выбранных строк и столбцов
        temp_matrix[min_row_index, :] = np.inf
        temp_matrix[:, min_col_index] = np.inf

    return assignments_row, assignments_col


# Создание матрицы Z с использованием Браунгшвейской формулы
def create_matrix_z():
    """
    Формируем матрицу сахаростисти с учетом Браунгшвейской формулы

    :return list[20][20]
    """
    a = np.arange(15, 21, 0.3)  # Вектор изначальной сахаростисти свеклы
    K = np.arange(5, 7.5, 0.13)  # Вектор неораники K
    Na = np.arange(0.3, 0.9, 0.031)  # Вектор неораники Na
    N = np.arange(1.5, 3, 0.076)  # Вектор неораники N
    np.random.shuffle(K)
    np.random.shuffle(Na)
    np.random.shuffle(N)

    B = 0.12 * (K + Na) + 0.24 * N + 0.48  # Формируем вектор неорганики по Браунгшвейской формуле

    b_matrix = []                             # Матрица коофициентов дегродации
    for i in range(20):                       #
        cache = np.arange(0.9, 0.99, 0.0048)
        np.random.shuffle(cache)
        b_matrix.append(cache)

    b_matrix = np.array(b_matrix)

    np.random.shuffle(a)

    Z = np.zeros((20, 20))

    for i in range(20):               # Формируем матрицу Z, z_i_j = a_i*b_i_j - B_i  (b_i_j = (i = 1..19 )) (B_i = a[i] * B[i]/100 (вычитаем влияние не ораники как процентB[i] от сахористости))
        Z[i][0] = a[i] - a[i] * B[i]/100        #a[i] умножить на влияние не органики(не органика считается процентом от сахаристости)
        product = a[i]
        for j in range(1, 20):
            product *= b_matrix[i][j - 1]
            product = product - product * B[i]/100
            Z[i][j] = product

    return Z.tolist()


# Преобразование строки в число
def string_to_number(string):
    # Split the string by '/'
    numbers = string.split('/')
    if string.find('/') == -1:
        return float(string)

    # Convert strings to floating-point numbers and perform division
    result = float(numbers[0]) / float(numbers[1])

    return result
