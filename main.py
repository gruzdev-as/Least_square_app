''' Main file for app ''' 
import json
import sys
import pandas as pd
import numpy as np

from datetime import datetime
from PyQt5 import QtGui, QtWidgets, uic
from sympy import S, symbols, printing

import design

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
        

class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        ''' Init a file for acess to vars and methods in design.py'''
        super().__init__()
        self.setupUi(self) # design init

        # Vars and default values
        self.x_dot_values = []
        self.y_dot_values = []
        self.x_poly_values = []
        self.y_poly_values = []
        self.x_poly_values_list = []
        self.y_poly_values_list = []
        self.powers = []
        self.formulas = []
        self.power = 0
        self.points_number = 50

        self.Number_of_points.insert(str(self.points_number))
        self.Number_of_points.setValidator(QtGui.QIntValidator(0, 1000))
        
        for row in range (0, 9):
            self.PowerTable.setItem(
                row, 
                0, 
                QtWidgets.QTableWidgetItem('{} степень полинома' .format(row + 1))
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
        self.Number_of_points.textChanged.connect(self.changed_number_of_points)
        self.menuAuthor.triggered.connect(self.author_page_open)
    

    def open_file(self):
        ''' Open file for analysis ''' 

        def open_json(path):
        
            with open(path, 'r') as data_file:
                    
                json_dict = json.loads(data_file.read())
                data = json_dict['data']
                
                self.x_dot_values = data['x_values'] 
                self.y_dot_values = data['y_values']
                self.draw_graph()

        def open_excell(path):
        
            excell_file = pd.ExcelFile(path)
            data_frame_1 = excell_file.parse('dots')
            self.x_dot_values = data_frame_1['x_dot_values']
            self.y_dot_values = data_frame_1['y_dot_values']
            self.draw_graph()
            self.PowerTable.setEnabled(True)
            self.Display_formula_checkbox.setEnabled(True)
            self.Save_button.setEnabled(True)

        file_information_list = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Выберите файл с данными',
            # Base Dir
            '',
            # File Formats
            '*.json *.xls *.xlsx'
        )

        # 0 index because of getOpenFileName method return 
        # path + file types '*.json *.xls *.xlsx' as list
        file_path = file_information_list[0]
        
        file_type = file_path.split(sep = '.')
        file_type = file_type[1]

        if file_type == 'json':
            open_json(file_path)

        else:
            open_excell(file_path)
        

    def save_file(self):
        ''' Save file as JSON & Excell''' 
        
        def save_json(path):
            
            json_input = {
                "date_added": str(datetime.now()),
                "dot_data" : {
                    "x_dot_values" : x_dot_list,
                    "y_dot_values" : y_dot_list,
                },
                "formula" : self.formulas,
                "poly_data": {
                    "powers" : self.powers,
                    "x_poly_values" : self.x_poly_values_list,
                    "y_poly_values" : self.y_poly_values_list
                },
                "formula" : self.formulas,
            }

            file_path = str(path[0]) + '.json'
            with open(file_path, 'w') as json_file:
                json.dump(json_input, json_file, indent = 4)

        def save_excell(path):
            
            sheetlist = {}
            excell_dot_df = pd.DataFrame({
                'x_dot_values' : self.x_dot_values.tolist(),
                'y_dot_values' : self.y_dot_values.tolist()
            })

            sheetlist['dots'] = excell_dot_df

            for iteration in range(0, len(self.powers)):
                excell_poly_df = pd.DataFrame({
                    'x_poly_values' : self.x_poly_values_list[iteration],
                    'y_poly_values' : self.y_poly_values_list[iteration]
                })

                sheetlist['poly {}' .format(self.powers[iteration])] = excell_poly_df

            file_path = str(path[0])
            writer = pd.ExcelWriter(file_path + '.xlsx',)
            
            for sheet in sheetlist.keys():
                sheetlist[sheet].to_excel(
                    writer, 
                    index=False,
                    sheet_name=sheet
                )
            writer.save()

        x_dot_list = self.x_dot_values.tolist()
        y_dot_list = self.y_dot_values.tolist()     

        path = QtWidgets.QFileDialog.getSaveFileName(
            self,
            'Введите имя файла',
            '', 
        )
        
        save_json(path)
        save_excell(path)


    def choose_power(self):
        
        self.powers.clear()
        for item in self.PowerTable.selectedItems():
            self.powers.append((item.row() + 1))
        
        self.Number_of_points.setEnabled(True)
        self.draw_graph(self.powers)


    def display_formula(self):

        # redraw
        self.draw_graph(self.powers)


    def changed_number_of_points(self, item):

        self.points_number = item
        
        if len(self.points_number) <= 0:
            self.points_number = 2
            self.Number_of_points.insert(str(self.points_number))
            self.Text_box.clear()
            self.Text_box.addItem('Точек недостаточно для построения графика')
        else:
            # redraw
            self.points_number = int(self.points_number)
            self.draw_graph(self.powers)


    def draw_graph(self, items = None):
        
        self.canvas.axes.clear()
        self.canvas.axes.grid()
        self.canvas.axes.scatter(
            self.x_dot_values, 
            self.y_dot_values, 
            color='red',
            s=2
            )
        
        if items:
            
            self.x_poly_values_list.clear()
            self.y_poly_values_list.clear()
            self.formulas.clear() 

            for item in items:
                
                self.power = item
                
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
                    num=self.points_number
                )
                self.y_poly_values = poly_class(self.x_poly_values)

                self.x_poly_values = np.round(self.x_poly_values, 2)
                self.y_poly_values = np.round(self.y_poly_values, 2)

                self.x_poly_values_list.append(self.x_poly_values.tolist()) # TODO Надо как-то округлить значения в листах, хотя, возможно и так хватит
                self.y_poly_values_list.append(self.y_poly_values.tolist())


                if self.Display_formula_checkbox.isChecked():
                    
                    x = symbols('x')
                    
                    formula = sum(S("{:6.2f}".format(v))*x**i for i, v in enumerate(polynom[::-1]))
                    
                    label = printing.latex(formula)
                    
                    self.formulas.append(str(formula))

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


    def author_page_open(self):
        self.author_window = uic.loadUi('author_window.ui')
        self.author_window.show()
        
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
