'''
File for edit the data
'''

import sip 
from PyQt5 import QtWidgets, QtGui
from canvas import MplCanvase, SeabornPlot
from matplotlib.backends.backend_qt5agg import(
    NavigationToolbar2QT as NavigationToolbar,
    )
import edit_window_design
from matplotlib.cbook import boxplot_stats  

class EditApplication(QtWidgets.QMainWindow, edit_window_design.Ui_MainWindow):
    
    def __init__(self, df):
        
        super().__init__()
        self.setupUi(self) # design init
        
        ### Dataframe 
        self.df = df 
        self.original_df = self.df.copy().reset_index(drop=True)

        ### Validator
        #self.edit_table.setValidator(QtGui.QIntValidator(0, 1000))
        
        ### Canvases settings 
        # Boxplot
        self.boxplot_canvas = SeabornPlot(self.df)
        self.boxplot_canvas_lay = QtWidgets.QVBoxLayout(
            self.edit_boxplotgraph_widget
            )
        self.boxplot_canvas_lay.addWidget(self.boxplot_canvas)
        self.master_toolbar = NavigationToolbar(
            self.boxplot_canvas, 
            self.edit_boxplotgraph_widget
            )
        self.boxplot_canvas_lay.addWidget(self.master_toolbar)
        
        # Scatterplot
        self.scatter_canvas = MplCanvase()
        self.scatter_canvas_lay = QtWidgets.QVBoxLayout(
            self.edit_dotGraph_widget
            )
        self.scatter_toolbar = NavigationToolbar(
            self.scatter_canvas, 
            self.edit_dotGraph_widget
            )
        self.scatter_canvas_lay.addWidget(self.scatter_canvas) 
        self.scatter_canvas_lay.addWidget(self.scatter_toolbar) 
        self.scatter_canvas.axes.clear()
        self.scatter_canvas.axes.grid()
        self.scatter_canvas.axes.scatter(
            self.df.section_area,
            self.df.max_force,
            color='red', 
        )
        
        ### Table Widget Fill
        for i, row in self.df.iterrows():
            self.edit_table.setRowCount(self.edit_table.rowCount() + 1)
            for j in range(self.edit_table.columnCount()):
                self.edit_table.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(row[j]))
                    )
        
        for section_area, data in self.df.groupby('section_area'):
            data = data.drop('section_area', axis=1)
            stats = boxplot_stats(data)
            stats = stats.pop()['fliers']
            for values in stats:
                index = self.df.loc[self.df['max_force'] == values].index[0] 
                self.edit_table.item(index, 1).setBackground(QtGui.QColor('red'))

        ### Events
        self.edit_table.cellChanged.connect(self.change_cell)
        self.edit_cancelEdit_button.clicked.connect(self.reset_df)
        self.edit_save_button.clicked.connect(self.save)
        self.edit_close_button.clicked.connect(self.close)
        
    def save(self):
        
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
        self, 
        "Сохранение измененного набора данных", 
        'data', 
        "(*.csv)"
        )
        self.df.to_csv(filename+'.csv', index=False)
        
    def change_cell(self, row, column): 
        '''Is emitted whenever the data has changed'''

        self.df.iloc[row, column] = int(self.edit_table.item(row, column).text())
        self.redraw()

    def reset_df(self):
        self.df = self.original_df
        
        # It creates a lot of empty rows and works slowly 
        for i, row in self.df.iterrows():
            self.edit_table.setRowCount(self.edit_table.rowCount() + 1)
            for j in range(self.edit_table.columnCount()):
                self.edit_table.setItem(
                    i, j, QtWidgets.QTableWidgetItem(str(row[j]))
                    )
   
    def redraw(self):

        self.scatter_canvas.axes.clear()
        self.scatter_canvas.axes.grid()  
        self.scatter_canvas.axes.scatter(
            self.df.section_area,
            self.df.max_force,
            color='red', 
        )
        self.scatter_canvas.draw()

        self.boxplot_canvas_lay.removeWidget(self.boxplot_canvas)
        sip.delete(self.boxplot_canvas)
        self.boxplot_canvas_lay.removeWidget(self.master_toolbar)
        sip.delete(self.master_toolbar)
        self.boxplot_canvas = SeabornPlot(self.df)
        self.boxplot_canvas_lay.addWidget(self.boxplot_canvas)
        self.master_toolbar = NavigationToolbar(
            self.boxplot_canvas, 
            self.edit_boxplotgraph_widget
            )
        self.boxplot_canvas_lay.addWidget(self.master_toolbar)
        
        for section_area, data in self.df.groupby('section_area'):
            data = data.drop('section_area', axis=1)
            stats = boxplot_stats(data)
            stats = stats.pop()['fliers']
            for values in stats:
                index = self.df.loc[self.df['max_force'] == values].index[0] 
                self.edit_table.item(index, 1).setBackground(QtGui.QColor('red'))

        
        
    
