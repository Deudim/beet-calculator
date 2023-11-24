import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
import time


def calculate_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        print(f"Время выполнения функции '{func.__name__}': {(end_time - start_time) * 1e9} наносекунд")
        return result
    return wrapper


#@calculate_time
def hungarian(matrix, target='min'):
    matrix = np.array(matrix)
    kf = 1
    if target == 'max':
        kf = -1
    matrix = kf * matrix
    row_ind, col_ind = linear_sum_assignment(matrix) #Венгерский метод (https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.optimize.linear_sum_assignment.html)
    res = matrix[row_ind, col_ind].sum()
    return float(kf * res)


#@calculate_time
def munkres(matrix, target='min'):
    kf = 1
    if target == 'max':
        kf = -1
    matrix = multiply_matrix_(matrix, kf)
    m = Munkres()  #Метод Мака https://software.clapper.org/munkres/
    indexes = m.compute(matrix)
    res = 0
    for row, column in indexes:
        value = matrix[row][column]
        res += value
    return float(kf * res)


def multiply_matrix_(matrix, a):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= a
    return matrix
