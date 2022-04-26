import sys 
from PyQt5 import QtWidgets

from main_application import MainApplication



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApplication()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()                                                                      