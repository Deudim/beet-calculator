from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from mat_backend import hungarian, munkres, greedy, create_matrix_z


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
