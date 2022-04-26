''' 
Main window file methods
'''

from PyQt5 import QtGui, QtWidgets, uic

import main_window_design

class MainApplication(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    ''' Class for the main window'''
    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # design init
        
        # Vars and variables
        

        # Events
        self.build_about_toolButton.clicked.connect(self.about_show)
        self.build_choosefile_button.clicked.connect(self.choose_file)
        self.build_createModel_button.clicked.connect(self.create_regression_model)
        self.build_editdata_button.clicked.connect(self.open_edit_window)
        self.build_savemodel_button.clicked.connect(self.save_model)
        

    def about_show(self):
        '''Showing manual how to prepare data for regression'''
        pass
    
    def choose_file(self):
        '''File choosing for regression model build'''
        pass 
    
    def create_regression_model(self):
        '''Initialize creating regression model'''
        pass
    
    def open_edit_window(self):
        '''Open the edit data window'''
        pass
    
    def save_model(self):
        '''Saving the regression model'''
        pass