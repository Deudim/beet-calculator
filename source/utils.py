import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
import time
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QPushButton


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
    row_ind, col_ind = linear_sum_assignment(
        matrix)  # Венгерский метод (https://docs.scipy.org/doc/scipy-1.1.0/reference/generated/scipy.optimize.linear_sum_assignment.html)
    res = matrix[row_ind, col_ind].sum()
    return float(kf * res)


#@calculate_time
def munkres(matrix, target='min'):
    kf = 1
    if target == 'max':
        kf = -1
    matrix = multiply_matrix_(matrix, kf)
    m = Munkres()  # Метод Мака https://software.clapper.org/munkres/
    indexes = m.compute(matrix)
    res = 0
    for row, column in indexes:
        value = matrix[row][column]
        res += value
    return float(kf * res)


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
    return float(kf * res)


def multiply_matrix_(matrix, a):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= a
    return matrix


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


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../widget.ui', self)
        self.spinBox_matrics_count.valueChanged.connect(self.on_spinBox_matrics_count_changed)
        self.get_res.clicked.connect(self.on_get_res)
        for i in range(2):
            for j in range(2):
                test = QLineEdit(self)
                test.insert("0")
                self.gridLayout.addWidget(test, i, j)
            self.show()


    def on_spinBox_matrics_count_changed(self):
        matrics_count = self.spinBox_matrics_count.value()
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        for i in range(matrics_count):
            for j in range(matrics_count):
                test = QLineEdit(self)
                test.insert("0")
                self.gridLayout.addWidget(test, i, j)

    def on_get_res(self):
        matrics_count = self.spinBox_matrics_count.value()
        matrics = []
        for i in range(matrics_count):
            matrics.append([])
            for j in range(matrics_count):
                matrics[i].append([])
                text = self.gridLayout.itemAtPosition(i, j).widget().text()
                texstarr = text.split("/")
                textnew = 0.0
                if len(texstarr) == 2:
                    try:
                        textnew = float(texstarr[0]) / float(texstarr[1])
                    except:
                        textnew = 0.0
                else:
                    try:
                        textnew = float(texstarr[0])
                    except:
                        textnew = 0.0

                matrics[i][j] = textnew
        #print(matrics)
        out = ""
        get_out = "max"
        if self.rb_min.isChecked():
            get_out = "min"
        self.l_res.setText(get_out + ": " + str(hungarian(matrics, get_out)))

