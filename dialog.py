from PyQt5 import QtWidgets
import dialog_window_design


class Dialog(QtWidgets.QDialog, dialog_window_design.Ui_Dialog):
    
    def __init__(self, edit_window, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self.edit_window = edit_window
        self.warning_buttonBox.accepted.connect(self.printed1)
        self.warning_buttonBox.rejected.connect(self.printed2)
        
    def printed1(self):
        
        self.edit_window.show()
        
    def printed2(self):
        
        pass