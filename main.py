''' Main file for app ''' 
import json
import sys 
import pandas as pd
import numpy as np
from PyQt5 import QtWidgets, QtCore

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
        self.PowerTable.cellClicked.connect(self.testTable)
        self.Display_formula_checkbox.stateChanged.connect(self.display_formula)


    def testTable(self):
        #print('hey', type(item), str(item))
        items = []
        for item in self.PowerTable.selectedItems():
            items.append(item.row())
            print (items)
        

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

        
    def save_file(self):
        ''' Save file as JSON ''' 
        None


    def choose_power(self, item):

        self.power = int(item)
        print(int(item))
        if len(self.x_dot_values) != 0:
            self.draw_graph()


    def display_all(self):
        
        print('hey', self.Display_all_checkbox.isChecked())


    def display_formula(self):

        print('hey', self.Display_formula_checkbox.isChecked())
        
        if self.x_values != []:
            self.draw_graph()


    def draw_graph(self):
        
        self.canvas.axes.clear()
        self.canvas.axes.grid()
        self.canvas.axes.scatter(
            self.x_dot_values, 
            self.y_dot_values, 
            color = 'red'
            )
        
        
        if self.Display_formula_checkbox.isChecked():
            self.get_formula()
        
        z = np.polyfit(
            self.x_dot_values,
            self.y_dot_values,
            self.power
        )
        
        p = np.poly1d(z)
        
        self.x_poly_values = np.linspace(
            self.x_dot_values.values[0],
            self.x_dot_values.values[-1],
            num = 50
        )
        self.y_poly_values = p(self.x_poly_values)

        self.canvas.axes.plot(
            self.x_poly_values,
            self.y_poly_values,
        )

        self.canvas.draw()


    def get_formula(self):
        None
        
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
