import sys
from PyQt5 import QtWidgets
from UI_Armaduras import Ui_Armaduras
from UI_Functions import Ui_Functions

class Ui_MainWindow(QtWidgets.QMainWindow):
    '''
    Programó:
    M. en I. Josue Emmanuel Cruz Barragan
    '''
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Armaduras()
        self.ui.setupUi(self)

        # Valores de inicializacion
        Ui_Functions.Fn_Inicializar(self)

        # Manipular renglones en tablas
        Ui_Functions.Wgt_SpinBox(self)



    def AnadirRenglonSinCombo(self):
        val = self.ui.sp_numElem.value()
        self.ui.tbl_elem.setRowCount(val)
        self.ui.tbl_elem.update()

    def AnadirRenglonConCombo(self, var):
        if var == 'N':
            val = self.ui.sp_numNodo.value()
            attr = ["Fijo", "Libre", "DX", "DY"]
            self.ui.tbl_nod.setRowCount(val)

            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_nod.setCellWidget(i, 3, combobox)
        if var == 'F':
            val = self.ui.sp_fuerzas.value()
            attr = ["DX", "DY"]
            self.ui.tbl_fuerzas.setRowCount(val)

            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_fuerzas.setCellWidget(i, 2, combobox)
        if var == 'D':
            val = self.ui.sp_desp.value()
            attr = ["DX", "DY"]
            self.ui.tbl_desp.setRowCount(val)

            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_desp.setCellWidget(i, 2, combobox)









if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = Ui_MainWindow()
    my_app.show()
    sys.exit(app.exec_())

