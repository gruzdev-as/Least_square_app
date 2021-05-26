''' Main file for app ''' 
import json
import sys 

from PyQt5 import QtWidgets, QtCore

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

        # Vars
        self.x_values = []
        self.y_values = []

        # Insert powerlist 
        for power in range(2,9):
            self.Choose_power.insertItem(
                0, '{}'.format(power), '{}'.format(power)
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
        self.Choose_power.textActivated.connect(self.choose_power)
        self.Display_all_checkbox.stateChanged.connect(self.display_all)
        self.Display_formula_checkbox.stateChanged.connect(self.display_formula)


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
            
            self.x_values = data['x_values']
            self.y_values = data['y_values']
            self.draw_graph()
            

        

    def open_excell(self, path):
        print(path)

        
    def save_file(self):
        ''' Save file as JSON ''' 
        None


    def choose_power(self, item):

        print('clicked', item)


    def display_all(self):
        
        print('hey', self.Display_all_checkbox.isChecked())


    def display_formula(self):

        print('hey', self.Display_formula_checkbox.isChecked())
        
        if self.x_values != []:
            self.draw_graph()


    def draw_graph(self):
        
        self.canvas.axes.clear()
        self.canvas.axes.grid()
        self.canvas.axes.plot(self.x_values, self.y_values, color = 'red')
        self.canvas.draw()
        if self.Display_formula_checkbox.isChecked():
            print("True")
        else:
            print("False")
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
