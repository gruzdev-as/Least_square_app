from PyQt5 import QtWidgets

class MessageBox():
    
    def __init__(self, text='', title=''):
        
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        returnValue = msgBox.exec()