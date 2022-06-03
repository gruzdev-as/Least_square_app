import sys 
from PyQt5 import QtWidgets

from main_application import MainApplication
from edit_application import EditApplication
from dialog import Dialog


def main():
    app = QtWidgets.QApplication(sys.argv)
    edit = EditApplication()
    warning = Dialog(edit)
    window = MainApplication(warning)
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()                                                                      