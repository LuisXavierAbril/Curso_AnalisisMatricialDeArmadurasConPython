from PyQt5 import QtWidgets


class Ui_Functions(QtWidgets.QMainWindow):
    '''
    Programó:
    M. en I. Josue Emmanuel Cruz Barragan
    '''
    def Fn_Inicializar(self):

        # Crear Tabla de Elementos
        #        Elem, A, E, Nodo_I, Nodo_F
        dataElem = [['E1', 1, 1, 'N5', 'N1'],
                    ['E2', 1, 1, 'N2', 'N1'],
                    ['E3', 1, 1, 'N3', 'N2'],
                    ['E4', 1, 1, 'N2', 'N5'],
                    ['E5', 1, 1, 'N3', 'N5'],
                    ['E6', 1, 1, 'N4', 'N5'],
                    ['E7', 1, 1, 'N3', 'N4']]

        row = len(dataElem)
        self.ui.sp_numElem.setValue(row)
        col = len(dataElem[0])

        for i in range(row):
            self.ui.tbl_elem.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataElem[i][j]))
                self.ui.tbl_elem.setItem(i, j, celda)

        # Crear Tabla de Nodos: {Fijo, Libre, DX, DY}
        #        Nodos,    X,    Y,   Tipo
        dataNodos = [['N1', 14.0, 07.0, "Libre"],
                    ['N2', 07.0, 07.0, "Libre"],
                    ['N3', 00.0, 07.0, "Fijo"],
                    ['N4', 00.0, 00.0, "Fijo"],
                    ['N5', 07.0, 00.0, "Libre"]]

        row = len(dataNodos)
        self.ui.sp_numNodo.setValue(row)
        col = len(dataNodos[0])
        attr = ["Fijo", "Libre", "DX", "DY"]
        for i in range(row):
            self.ui.tbl_nod.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataNodos[i][j]))
                self.ui.tbl_nod.setItem(i, j, celda)

                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataNodos[i][3]))
                self.ui.tbl_nod.setCellWidget(i, 3, combobox)



        # Crear Tabla de Fuerzas
        #          Frza, Nodo, Direcc
        dataFrzas = [[-3, 'N2', "DY"],
                     [-2, 'N1', "DY"]]

        row = len(dataFrzas)
        self.ui.sp_fuerzas.setValue(row)
        col = len(dataFrzas[0])
        attr = ["DX", "DY"]
        for i in range(row):
            self.ui.tbl_fuerzas.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataFrzas[i][j]))
                self.ui.tbl_fuerzas.setItem(i, j, celda)

                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataFrzas[i][2]))
                self.ui.tbl_fuerzas.setCellWidget(i, 2, combobox)



        # Crear Tabla de Desplazamientos
        #          Desp, Nodo, Direcc
        dataDesp = [[0, 'N3', "DX"],
                    [0, 'N3', "DY"],
                    [0, 'N4', "DX"],
                    [0, 'N4', "DY"]]

        row = len(dataDesp)
        self.ui.sp_desp.setValue(row)
        col = len(dataDesp[0])
        attr = ["DX", "DY"]
        for i in range(row):
            self.ui.tbl_desp.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataDesp[i][j]))
                self.ui.tbl_desp.setItem(i, j, celda)

                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataDesp[i][2]))
                self.ui.tbl_desp.setCellWidget(i, 2, combobox)







    def Wgt_ComboBox(self):
        pass

    def Wgt_SpinBox(self):
        self.ui.sp_numElem.valueChanged.connect(self.AnadirRenglonSinCombo)
        self.ui.sp_numNodo.valueChanged.connect(lambda: self.AnadirRenglonConCombo('N'))
        self.ui.sp_fuerzas.valueChanged.connect(lambda: self.AnadirRenglonConCombo('F'))
        self.ui.sp_desp.valueChanged.connect(lambda: self.AnadirRenglonConCombo('D'))

    def Wgt_PushButton(self):
        pass
