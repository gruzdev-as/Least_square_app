''' Main file for app ''' 
import json
import sys 
import pandas as pd
import numpy as np

from datetime import date, datetime
from PyQt5 import QtGui, QtWidgets, QtCore
from sympy import S, symbols, printing

import design_with_table

import matplotlib
matplotlib.use('QT5Agg') # backend for qt app

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
    )

class MplCanvase(FigureCanvas):
    ''' The class describe a figure for import them into the apps widget ''' 

    def __init__(self):
        ''' Executed when the class is instantiated '''

        fig = Figure()
        self.axes = fig.add_subplot()
        fig.subplots_adjust(
            left = 0.08,
            right = 0.98, # 1 - 0.98 = 0.2
            top = 0.95, # 1 - 0.95 = 0.5
            bottom = 0.1
            )

        super().__init__(fig)
        

class Application(QtWidgets.QMainWindow, design_with_table.Ui_MainWindow):

    def __init__(self):
        ''' Init a file for acess to vars and methods in design.py'''
        super().__init__()
        self.setupUi(self) # design init

        # Vars
        self.x_dot_values = []
        self.y_dot_values = []
        self.x_poly_values = []
        self.y_poly_values = []
        self.x_poly_values_list = []
        self.y_poly_values_list = []
        self.powers = []

        self.power = 2
        
        for row in range (0, 8):
            self.PowerTable.setItem(row, 0, 
                QtWidgets.QTableWidgetItem('{} степень полинома' .format(row+2))
                )

        
        # Canvas setting 
        self.canvas = MplCanvase()
        self.canvas_lay = QtWidgets.QVBoxLayout(self.widget)
        self.toolbar = NavigationToolbar(self.canvas, self.widget)
        self.canvas_lay.addWidget(self.canvas) # Add Canvas obj to Widget
        self.canvas_lay.addWidget(self.toolbar) # Add toolbar to Widget
        self.canvas.axes.clear()
        self.canvas.axes.grid()

    
        #Events
        self.Open_button.clicked.connect(self.open_file)
        self.Save_button.clicked.connect(self.save_file)
        self.PowerTable.cellClicked.connect(self.choose_power)
        self.Display_formula_checkbox.stateChanged.connect(self.display_formula)


    def choose_power(self):
        
        self.powers = []
        for item in self.PowerTable.selectedItems():
            self.powers.append(item.row())
        
        self.draw_graph(self.powers)
        

    def open_file(self):
        ''' Open file for analysis ''' 
        
        self.Text_box.clear()

        file_information_list = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Выберите файл с данными',
            # Base Dir
            '',
            '*.json *.xls *.xlsx'
        )

        # 0 index because of getOpenFileName method return 
        # path + file types '*.json *.xls *.xlsx' as list
        file_path = file_information_list[0]

        
        file_type = file_path.split(sep = '.')
        file_type = file_type[1]

        if file_type == 'json':
            self.open_json(file_path)

        else:
            self.open_excell(file_path)
        

    def open_json(self, path):
        
        with open(path, 'r') as data_file:
                
            json_dict = json.loads(data_file.read())
            data = json_dict['data']
            
            self.x_dot_values = data['x_values'] 
            self.y_dot_values = data['y_values']
            self.draw_graph()


    def open_excell(self, path):
        
        excell_file = pd.ExcelFile(path)
        print(excell_file.sheet_names)
        df1 = excell_file.parse('Bla')
        self.x_dot_values = df1['x_values']
        self.y_dot_values = df1['y_values']
        self.draw_graph()
        self.PowerTable.setEnabled(True)
        self.Display_formula_checkbox.setEnabled(True)
        self.Save_button.setEnabled(True)


    def save_file(self):
        ''' Save file as JSON ''' 
        
        x_dot_list = self.x_dot_values.tolist()
        y_dot_list = self.y_dot_values.tolist()
        powers = [power + 2 for power in self.powers]
        

        json_input = {
            "dot_data" : {
                "x_dot_values" : x_dot_list,
                "y_dot_values" : y_dot_list,
            },
            "poly_data": {
                "powers" : powers,
                "x_poly_values" : self.x_poly_values_list,
                "y_poly_values" : self.y_poly_values_list
            },
            "formula" : "",
            "date_added": ""
        }

        
        path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            'Введите имя файла',
            '', 
        )

        file_path = str(path[0]) + '.json'
        with open(file_path, 'w') as json_file:
            json.dump(json_input, json_file, indent = 4)
        


    def display_formula(self):

        # redraw
        self.draw_graph(self.powers)


    def draw_graph(self, items = None):
        
        self.canvas.axes.clear()
        self.canvas.axes.grid()
        self.canvas.axes.scatter(
            self.x_dot_values, 
            self.y_dot_values, 
            color = 'red'
            )
        
        if items:
            
            self.x_poly_values_list = []
            self.y_poly_values_list = []

            for item in items:
                self.power = item + 2
                
                # With least square method
                polynom = np.polyfit(
                    self.x_dot_values,
                    self.y_dot_values,
                    self.power
                )
                
                # Encapsulates a polynomial for the convenience 
                # of performing operations on it in the future
                poly_class = np.poly1d(polynom)
                
                # Dividing the space equally at intervals for construction
                self.x_poly_values = np.linspace(
                    self.x_dot_values.values[0],
                    self.x_dot_values.values[-1],
                    num = 5
                )
                self.y_poly_values = poly_class(self.x_poly_values)

                self.x_poly_values_list.append(self.x_poly_values.tolist())
                self.y_poly_values_list.append(self.y_poly_values.tolist())

                if self.Display_formula_checkbox.isChecked():
                    
                    x = symbols('x')
                    formula = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(polynom[::-1]))
                    label = printing.latex(formula)

                    self.canvas.axes.plot(
                    self.x_poly_values,
                    self.y_poly_values,
                    label = "${}$" .format(label)
                    )
                
                else: 
                    
                    label = '{} степень полинома' .format(self.power)
                    
                    self.canvas.axes.plot(
                    self.x_poly_values,
                    self.y_poly_values,
                    label = label
                    )
                    
        self.canvas.axes.legend()
        self.canvas.draw()
        print(self.x_poly_values_list, self.y_poly_values_list)



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
