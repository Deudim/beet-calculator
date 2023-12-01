from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from mat_backend import hungarian, munkres, greedy, create_matrix_z, string_to_number
from report import make_report
import os

def _matrix_assist(type, matrix, target):
    if type == 0:
        return hungarian(matrix, target)
    elif type == 1:
        return munkres(matrix, target)
    elif type == 2:
        return greedy(matrix, target)


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Передаём ссылку на родительский элемент и чтобы виджет
        # отображался как самостоятельное окно указываем тип окна
        super().__init__(parent, QtCore.Qt.Window)
        uic.loadUi('uis/otchet.ui', self)
        self.setWindowTitle("Отчёт")
        self.pix.setPixmap(QtGui.QPixmap("out\\my_plot.png"))
        self.exit.clicked.connect(self.on_exit)
        self.open_csv.clicked.connect(self.on_csv)
        self.open_folder.clicked.connect(self.on_folder)


    def on_folder(self):
        os.startfile("out\\")
    def on_csv(self):
        os.startfile("out\\report.csv")

    def on_exit(self):
        self.close()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('uis/widget.ui', self)
        self.secondWin = None
        self.spinBox_matrics_count.valueChanged.connect(self.on_spinBox_matrics_count_changed)
        self.get_res.clicked.connect(self.on_get_res)
        self.exit.clicked.connect(self.on_exit)
        self.pb_gen.clicked.connect(self.on_gen)
        self.gridLayout.setSpacing(0)
        self.get_otch.clicked.connect(self.on_otch)
        self.listv.setVisible(False)
        ret = create_matrix_z()
        for i in range(self.spinBox_matrics_count.value()+1):
            for j in range(self.spinBox_matrics_count.value()+1):
                test = QLineEdit(self)
                test.setReadOnly(True)
                if i == 0 and j != 0:
                    test.insert("day " + str(j))
                elif j == 0 and i != 0:
                    test.insert("p " + str(i))
                elif i == 0 and j == 0:
                    test.insert("p\d")
                else:
                    test.setReadOnly(False)
                    test.insert(str(float('{:.3f}'.format(ret[i-1][j-1]))))
                self.gridLayout.addWidget(test, i, j, Qt.AlignHCenter)
            self.show()

    def closeEvent(self, event):
        if self.secondWin.isVisible():
            reply = QtWidgets.QMessageBox.question(self, 'Информация',
                                                   "Вы хотите закрыть вместе с окном отчёта?",
                                                   QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.secondWin.close()  # ! widget
                event.accept()
            else:
                event.accept()

    def on_otch(self):
        self.secondWin = None
        if make_report():
            self.secondWin = SecondWindow()
            self.secondWin.show()

    def on_exit(self):
        self.close()

    def on_gen(self):
        self.spinBox_matrics_count.setValue(20)
        ret = create_matrix_z()
        #print(ret[0][0])
        for i in range(self.spinBox_matrics_count.value()):
            for j in range(self.spinBox_matrics_count.value()):
                self.gridLayout.itemAtPosition(i+1, j+1).widget().setStyleSheet("background-color: none")
                self.gridLayout.itemAtPosition(i+1, j+1).widget().setText(str(float('{:.3f}'.format(ret[i][j]))))


    def on_spinBox_matrics_count_changed(self):
        matrics_count = self.spinBox_matrics_count.value()
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            self.gridLayout.removeWidget(widgetToRemove)
            widgetToRemove.setParent(None)

        for i in range(self.spinBox_matrics_count.value()+1):
            for j in range(self.spinBox_matrics_count.value()+1):
                test = QLineEdit(self)
                test.setReadOnly(True)
                if i == 0 and j != 0:
                    test.insert("day " + str(j))
                elif j == 0 and i != 0:
                    test.insert("p " + str(i))
                elif i == 0 and j == 0:
                    test.insert("p\d")
                else:
                    test.setReadOnly(False)
                    test.insert("0")
                self.gridLayout.addWidget(test, i, j, Qt.AlignHCenter)

    def on_get_res(self):
        matrics_count = self.spinBox_matrics_count.value()
        matrics = []
        for i in range(matrics_count):
            matrics.append([])
            for j in range(matrics_count):
                matrics[i].append([])
                text = self.gridLayout.itemAtPosition(i+1, j+1).widget().text()
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
                self.gridLayout.itemAtPosition(i+1, j+1).widget().setStyleSheet("background-color: none")
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
        # for i, j in zip(result['rows'], result['cols']):  #test
        #     print(i, j)
        rows = result['rows']
        cols = result['cols']
        text_res = result['result']
        ##for i in range(matrics_count):
        #print(rows[0])
        out_text += str(float('{:.3f}'.format(text_res))) ## вывод текста
        out = {col: row for col, row in zip(cols, rows)}
        summa = 0
        self.listv.setVisible(True)
        string_list = []
        for i in range(matrics_count):
            self.gridLayout.itemAtPosition(rows[i]+1, cols[i]+1).widget().setStyleSheet("background-color: green")
            #for j in range(matrics_count):
                # if j == rows[j] and i == cols[i]:
                #     print("День "+ str(i+1) + " - " + self.gridLayout.itemAtPosition(j+1, i+1).widget().text())
            this_day = self.gridLayout.itemAtPosition(out[i]+1, i+1).widget().text()
            summa += float(string_to_number(this_day))/100
            #print("День " + str(i+1) + " - " + this_day)
            #print(f"За {i+1} день добыли {float(this_day)/100}кг, кг сахара в общем - {summa}")  #1партия - 1 кг сахара
            #out_text += "За " + str(i+1) + " день добыли "
            #out_text += str(float('{:.3f}'.format(float(this_day)/100))) + "кг, кг сахара в общем - " + str(float('{:.3f}'.format(summa)))
            #item = QtGui.QStandardItemModel(f"За {i+1} день добыли {float(this_day)/100}кг, кг сахара в общем - {summa}")
            string_list.append(f"За {i+1} день добыли { float('{:.3f}'.format(float(string_to_number(this_day))/100)) }кг, сахара в общем - {float('{:.3f}'.format(float(summa)))}кг")

        model_1 = QtCore.QStringListModel(self)
        model_1.setStringList(string_list)
        self.listv.setModel(model_1)
        #self.listv.addItem(item)
        self.l_res.setText(out_text)
