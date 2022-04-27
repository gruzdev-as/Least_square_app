''' 
Main window file methods
'''

from PyQt5 import QtGui, QtWidgets, uic


from canvas import MplCanvase

from matplotlib.backends.backend_qt5agg import(
    NavigationToolbar2QT as NavigationToolbar,
    )

import main_window_design

class MainApplication(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    ''' Class for the main window'''
    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # design init
        
        # TODO refactoring
        
        # Canvas and toolbar setup
        
        # Master page
        self.master_canvas = MplCanvase()
        self.master_canvas_lay = QtWidgets.QVBoxLayout(self.master_graph_widget)
        self.master_toolbar = NavigationToolbar(
            self.master_canvas, 
            self.master_graph_widget
        )
            # Add a Canvas obj to a Widget
        self.master_canvas_lay.addWidget(self.master_canvas) 
            # Add a toolbar to a Widget
        self.master_canvas_lay.addWidget(self.master_toolbar) 
        self.master_canvas.axes.clear()
        self.master_canvas.axes.grid()
        
        # Build page
        self.build_canvas = MplCanvase()
        self.build_canvas_lay = QtWidgets.QVBoxLayout(self.build_graph_widget)
        self.build_toolbar = NavigationToolbar(
            self.build_canvas, 
            self.build_graph_widget
        )
            # Add a Canvas obj to a Widget
        self.build_canvas_lay.addWidget(self.build_canvas) 
            # Add a toolbar to a Widget
        self.build_canvas_lay.addWidget(self.build_toolbar) 
        self.build_canvas.axes.clear()
        self.build_canvas.axes.grid()
        
        
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