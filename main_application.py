''' 
Main window file methods
'''

import pandas as pd
import time 

from PyQt5 import QtGui, QtWidgets, uic


from regression import NewRegressionModel
from canvas import MplCanvase
from messageBox import MessageBox

from matplotlib.backends.backend_qt5agg import(
    NavigationToolbar2QT as NavigationToolbar,
    )

import main_window_design

class MainApplication(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    ''' Class for the main window'''
    
    def __init__(self, warning_window):
        
        super().__init__()
        self.setupUi(self) # design init
        
        self.warning_window = warning_window 
        # Canvas and toolbar setup
        # Master page
        self.master_canvas = MplCanvase()
        self.master_canvas_lay = QtWidgets.QVBoxLayout(
            self.master_graph_widget
            )
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
        self.build_canvas_lay = QtWidgets.QVBoxLayout(
            self.build_graph_widget
            )
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
        self.regression_df = None

        
        # Validators
        self.master_square_edit.setValidator(QtGui.QIntValidator(0, 100))
        
        # TODO items from the database
        list1 = [
            'First Item',
            'Second Item',
            'Third Item',
        ]
        self.master_comboBox.clear()
        self.master_comboBox.addItems(list1)
        
        # Events
        self.build_about_toolButton.clicked.connect(self.about_show)
        self.build_choosefile_button.clicked.connect(self.choose_file)
        self.build_createModel_button.clicked.connect(self.create_regression_model)
        self.build_editdata_button.clicked.connect(self.open_edit_window)
        self.build_savemodel_button.clicked.connect(self.save_model)
        self.master_comboBox.currentTextChanged.connect(self.fetch_experiment_data)
        self.master_square_edit.textChanged.connect(self.calculate_stress)
        
        
    def about_show(self):
        '''Showing manual how to prepare data for regression'''

        MessageBox(
            title = 'Как готовить данные для регрессии',
            text = 'Какая-то переменная или файлик будет хранить этот текст'
            )

    def choose_file(self):
        '''File choosing for regression model build'''
        
        file_list = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Выберите файл с данными',
            # Base Dir
            '',
            # File Formats
            '*.csv'
        )
        
        # 0 index because getOpenFileName method return 
        # path + file type as a list

        if len(file_list[1]) <= 0:
            return None # File hasn't been choosen 
        
        file_path = file_list[0]
        self.regression_df = pd.read_csv(file_path, sep = ',')
        self.build_createModel_button.setEnabled(True)
        self.build_editdata_button.setEnabled(True)

        # Draw scatters on canvas
        self.build_canvas.axes.scatter(
            self.regression_df.section_area,
            self.regression_df.max_force,
            color='red', 
        )
        self.build_canvas.draw()
   
    def create_regression_model(self):
        '''Initialize creating regression model'''
        model = NewRegressionModel(self.regression_df)
        model.create_model()
        self.build_progresbar.setEnabled(True)
        self.build_progresbar.setValue(100)
        accuracy = model.vars['accuracy']
        equation = model.vars['equation']
        self.build_accuracy_label.setText(
            f'Точность данной предсказательной модели: {accuracy}'
            )
        self.build_equation_label.setText(
            f'Уравнение, описывающее зависимость максимально-допустимой нагрузки: {equation}'
            )
        
        self.build_modelName_edit.setEnabled(True)
        self.build_savemodel_button.setEnabled(True)
        
        
        ### TODO FIX (It works, but looks weird here)
        #Draw a regression Line
        X = model.vars['coefficients']['coef']
        B = model.vars['coefficients']['intercept']
        y = []
        for area in self.regression_df.section_area.unique():
            predict = X * area + B
            y.append(predict)
        self.build_canvas.axes.plot(
            self.regression_df.section_area.unique(), 
            y) 
        ### OR
        x1= 40
        x2= 50
        y1= X*x1+B
        y2= X*x2+B
        
        self.build_canvas.axes.axline(
            (x1,y1),
            (x2,y2)
            )
        
        self.build_canvas.draw()
            
    def open_edit_window(self):
        '''Open the edit data window'''
        self.warning_window.show()
    
    def save_model(self):
        '''Saving the regression model'''
        pass
    
    def fetch_experiment_data(self, text):   
        
        self.master_square_edit.setEnabled(True)
        
        # TODO fetch choosen data from the dataset

    def calculate_stress(self, text):
        print(text)