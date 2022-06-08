import matplotlib
matplotlib.use('QT5Agg') # backend for qt app
import seaborn as sns 

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import(
    FigureCanvasQTAgg as FigureCanvas,
    )

class MplCanvase(FigureCanvas):
    ''' The class describe an empty canvas for QTWiget''' 

    def __init__(self):
        
        ''' Executed when the class is instantiated '''

        fig = Figure()
        self.axes = fig.add_subplot()
        fig.subplots_adjust(
            left = 0.08,
            right = 0.98, # 1 - 0.98 = 0.2
            top = 0.95, # 1 - 0.95 = 0.05
            bottom = 0.1
            )

        super().__init__(fig)
        
class SeabornPlot(FigureCanvas):
    
    def __init__(self, data):
        
        self.g = sns.FacetGrid(
            data, 
            col='section_area',
            sharey='col',
            sharex='col',
        )
        self.fig = self.g.fig
        self.g.map(sns.boxplot, 'section_area', 'max_force', order=None)
        super().__init__(self.g.fig)
        
         
        
    
    