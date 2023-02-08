''' 
Main window file methods
'''
import pandas as pd
import time 
from random import choices
from PyQt5 import QtGui, QtWidgets, QtCore


from regression import NewRegressionModel
from canvas import MplCanvase
from messageBox import MessageBox

from edit_application import EditApplication

from matplotlib.backends.backend_qt5agg import(
    NavigationToolbar2QT as NavigationToolbar,
    )

import main_window_design

class MainApplication(QtWidgets.QMainWindow, main_window_design.Ui_MainWindow):
    ''' Class for the main window'''
    
    def __init__(self):
        
        super().__init__()
        self.setupUi(self) # design init
        
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
        self.edit_window = None

        # Validators
        self.master_square_edit.setValidator(QtGui.QIntValidator(0, 100))
        
       # Database
        self.database = pd.read_csv('..\\data\\database.csv', sep=';', decimal=',')
        
        list1 = self.database.name.value_counts().index.to_list()
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
            '',# Base Dir
            '*.csv'# File Formats
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
        self.build_canvas.axes.clear()
        self.build_canvas.axes.grid()
        self.build_canvas.axes.scatter(
            self.regression_df.section_area,
            self.regression_df.max_force,
            color='red', 
        )
        self.build_canvas.draw()
   
    def create_regression_model(self):
        '''Initialize creating regression model'''
        self.model = NewRegressionModel(self.regression_df)
        self.model.create_model()
        self.build_progresbar.setEnabled(True)
        self.build_progresbar.setValue(100)
        accuracy = self.model.vars['accuracy']
        equation = self.model.vars['equation']
        self.build_accuracy_label.setText(
            f'Точность данной предсказательной модели: {accuracy}'
            )
        self.build_equation_label.setText(
            f'Уравнение, описывающее зависимость максимально-допустимой нагрузки: {equation}'
            )
        
        self.build_modelName_edit.setEnabled(True)
        self.build_savemodel_button.setEnabled(True)
        
        #Draw a regression Line
        X = self.model.vars['coefficients']['coef']
        B = self.model.vars['coefficients']['intercept']
        y = []
        for area in self.regression_df.section_area.unique():
            predict = X * area + B
            y.append(predict)
        self.build_canvas.axes.plot(
            self.regression_df.section_area.unique(), 
            y) 
        ### OR
        x1, x2 = choices(self.regression_df.section_area.value_counts().index, k=2)
        y1, y2 = X*x1+B, X*x2+B
        
        self.build_canvas.axes.axline(
            (x1,y1),
            (x2,y2)
            )
        
        self.build_canvas.draw()
            
    def open_edit_window(self):
        '''Open the edit data window'''
        
        MessageBox(
            title = 'Подсказка про правильное редактирование данных',
            text = 'Какая-то переменная или файлик будет хранить этот текст'
            )
        
        self.edit_window = EditApplication(self.regression_df)
        self.edit_window.setWindowModality(QtCore.Qt.ApplicationModal)
        self.edit_window.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)   
        self.edit_window.show()

    def save_model(self):
        size = len(self.regression_df.max_force.to_numpy())
        new_df = pd.DataFrame({
           'name' : [self.build_modelName_edit.text()] * size,
           'max_force': self.regression_df.max_force.to_numpy(),
           'section_area': self.regression_df.section_area.to_numpy(),
           'accuracy': [self.model.vars['accuracy']] * size,
           'intercept' : [self.model.vars['coefficients']['intercept']] * size,
           'coef' : [self.model.vars['coefficients']['coef']] * size,
        })

        self.database = pd.concat([self.database, new_df], ignore_index=True)
        self.database.to_csv('..\\data\\database_new.csv', index=True)

        MessageBox(
            title = 'Сохранение',
            text = 'Успешно сохранено!'
            )

        self.build_modelName_edit.setEnabled(False)
        self.build_savemodel_button.setEnabled(False)
    
    def fetch_experiment_data(self, text):   
        
        self.master_canvas.axes.clear()
        self.master_canvas.axes.grid()
        self.master_square_edit.setEnabled(True)
        self.coef = self.database[self.database.name == text].coef.to_numpy()[0]
        self.intercept = self.database[self.database.name == text].intercept.to_numpy()[0]
        accuracy = self.database[self.database.name == text].accuracy.to_numpy()[0]
        self.master_equation_label.setText(f'Max Force = {self.coef} * Section Area + {self.intercept}')
        self.master_label_accuracy.setText(f'{accuracy}')

        self.master_canvas.axes.scatter(
            self.database[self.database.name == text].section_area.to_numpy(),
            self.database[self.database.name == text].max_force.to_numpy(),
            color='red', 
        )
        self.master_canvas.draw()
        print(self.coef, self.intercept)

    def calculate_stress(self, text):
        
        self.master_maxForce_label.setText(f'Расчитанная максимально-допустимая нагрузка при центральном растяжении для данного сечения соответственно равна: {self.coef*int(text) + self.intercept} Н')
        self.master_recForce_label.setText(f'Рекомендованное статическое нагружение данного сечения не более: {(self.coef*int(text) + self.intercept)*0.8} Н')