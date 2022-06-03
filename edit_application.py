'''
File for edit the data
'''

from PyQt5 import QtGui, QtWidgets, uic

import edit_window_design

class EditApplication(QtWidgets.QMainWindow, edit_window_design.Ui_MainWindow):
    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # design init