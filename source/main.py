import utils
from PyQt5 import QtWidgets
from utils import Ui
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    main()