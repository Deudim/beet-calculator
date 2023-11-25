# import numpy as np
# from munkres import Munkres, print_matrix
#
# m = Munkres()
import numpy as np
from utils import multiply_matrix_
import numpy as np


def assignment_greedy(cost_matrix):
    '''
    Хорошая жадная ункция но не та что нам нужна, она ищет минимумы, и занимет их
    '''
    num_workers = cost_matrix.shape[0]
    num_tasks = cost_matrix.shape[1]

    # Создаем копию матрицы стоимостей
    cost_matrix_copy = np.copy(cost_matrix)

    assigned_workers = []
    assigned_tasks = []

    for _ in range(num_workers):
        min_cost_indices = np.unravel_index(np.argmin(cost_matrix_copy), cost_matrix_copy.shape)
        min_cost_row, min_cost_col = min_cost_indices

        assigned_workers.append(min_cost_row)
        assigned_tasks.append(min_cost_col)

        cost_matrix_copy[min_cost_row, :] = np.inf  # Меняем стоимость для этого работника на бесконечность
        cost_matrix_copy[:, min_cost_col] = np.inf  # Меняем стоимость для этой задачи на бесконечность

    return assigned_workers, assigned_tasks


# indexes = m.compute(matrix)
#
# print_matrix(matrix, msg='Lowest cost through this matrix:')
# total = 0
# for row, column in indexes:
#     value = matrix[row][column]
#     total += value
#     print(f'({row}, {column}) -> {value}')
# print(f'total cost: {total}')


matrix = np.array([
    [7, 6, 5.1, 4],
    [6, 5.1, 4, 2],
    [5, 4, 2, 1],
    [4, 2, 1, 0.5]
])

cost_matrix = np.array([
    [9, 2, 7, 8],
    [6, 4, 3, 7],
    [5, 8, 1, 8],
    [7, 6, 9, 4]
])

# assignments = assign_jobs(matrix)
# print("Назначения работников на работы:", assignments)
# total = 0
# for i in range(len(matrix)):
#     total += matrix[i][assignments[i]]
# print(total)

row_ind, col_ind = assignment_greedy(matrix)
for r, c in zip(row_ind, col_ind):
    print(f"Работник {r} назначен на задачу {c} (стоимость: {matrix[r, c]})")
print(matrix[row_ind, col_ind].sum())
