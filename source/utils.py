import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
import time
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt

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
    return {'result': float(kf * res),
            'rows': row_ind.tolist(),
            'cols': col_ind.tolist()
            }


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


def create_matrix_z():
    """
    Формируем матрицу сахаростисти с учетом колбасной формулы

    :return list[20][20]
    """
    a = np.arange(15, 21, 0.3)  # Вектор изначальной сахаростисти свеклы
    K = np.arange(5, 7.5, 0.13)  # Вектор неораники K
    Na = np.arange(0.3, 0.9, 0.031)  # Вектор неораники Na
    N = np.arange(1.5, 3, 0.076)  # Вектор неораники N
    np.random.shuffle(K)
    np.random.shuffle(Na)
    np.random.shuffle(N)

    B = 0.12 * (K + Na) + 0.24 * N + 0.48  # Формируем вектор неорганики по колбасной формуле

    b_matrix = []                             # Матрица коофициентов дегродации
    for i in range(20):                       #
        cache = np.arange(0.05, 1, 0.05)
        np.random.shuffle(cache)
        b_matrix.append(cache)

    b_matrix = np.array(b_matrix)

    np.random.shuffle(a)

    Z = np.zeros((20, 20))

    for i in range(20):               # Формируем матрицу Z, z_i_j = a_i*b_i_j - B_i  (b_i_j = (i = 1..20 ))
        Z[i][0] = a[i] - B[i]
        product = a[i]
        for j in range(1, 20):
            product *= b_matrix[i][j - 1]
            product -= B[i]
            Z[i][j] = product

    return Z.tolist()


def _matrix_assist(type, matrix, target):
    if type == 0:
        return hungarian(matrix, target)
    elif type == 1:
        return munkres(matrix, target)
    elif type == 2:
        return greedy(matrix, target)


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../widget.ui', self)
        self.spinBox_matrics_count.valueChanged.connect(self.on_spinBox_matrics_count_changed)
        self.get_res.clicked.connect(self.on_get_res)
        self.exit.clicked.connect(self.on_exit)
        self.pb_gen.clicked.connect(self.on_gen)
        self.gridLayout.setSpacing(0)
        for i in range(self.spinBox_matrics_count.value()):
            for j in range(self.spinBox_matrics_count.value()):
                test = QLineEdit(self)
                test.insert("0")
                self.gridLayout.addWidget(test, i, j, Qt.AlignHCenter)
            self.show()

    def on_exit(self):
        self.close()

    def on_gen(self):
        self.spinBox_matrics_count.setValue(20)
        ret = create_matrix_z()
        #print(ret[0][0])
        for i in range(self.spinBox_matrics_count.value()):
            for j in range(self.spinBox_matrics_count.value()):
                self.gridLayout.itemAtPosition(i, j).widget().setStyleSheet("background-color: none")
                self.gridLayout.itemAtPosition(i, j).widget().setText(str(float('{:.3f}'.format(ret[i][j]))))


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
                self.gridLayout.addWidget(test, i, j, Qt.AlignHCenter)

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
                self.gridLayout.itemAtPosition(i, j).widget().setStyleSheet("background-color: none")
                matrics[i][j] = textnew
        get_out = "max"
        out_text= "Максимум = "
        if self.rb_min.isChecked():
            get_out = "min"
            out_text = "Минимум = "
        type = 0
        if self.rb_greedy.isChecked():
            type = 2
        elif self.rb_munkres.isChecked():
            type = 1

        result = _matrix_assist(type, matrics, get_out)
        rows = result['rows']
        cols = result['cols']
        text_res = result['result']
        self.l_res.setText(out_text + str(text_res))
        for i in range(matrics_count):
            self.gridLayout.itemAtPosition(rows[i], cols[i]).widget().setStyleSheet("background-color: green")
