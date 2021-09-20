from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class MplCanvasLienzo(FigureCanvas):
    '''
    Programó:
    M. en I. Josue Emmanuel Cruz Barragan
    '''
    def __init__(self):
        self.fig = Figure(facecolor="#23395B")
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)

class MatplotlibWidgetLienzo(QtWidgets.QWidget):
    '''
    Programó:
    M. en I. Josue Emmanuel Cruz Barragan
    '''
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvasLienzo()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)










