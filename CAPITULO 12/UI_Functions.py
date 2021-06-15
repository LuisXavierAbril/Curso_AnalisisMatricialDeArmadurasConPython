from PyQt5 import QtWidgets


class Ui_Functions(QtWidgets.QMainWindow):
    def Fn_Inicializar(self):
        ############################
        # Crear Tabla de Elementos #
        ############################
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

        ###############################################
        # Crear Tabla de Nodos: {Fijo, Libre, DX, DY} #
        ###############################################
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
                # Introducir ComboBox
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataNodos[i][3]))
                self.ui.tbl_nod.setCellWidget(i, 3, combobox)

        ##########################
        # Crear Tabla de Fuerzas #
        ##########################
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
                # Introducir ComboBox
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataFrzas[i][2]))
                self.ui.tbl_fuerzas.setCellWidget(i, 2, combobox)

        ##################################
        # Crear Tabla de Desplazamientos #
        ##################################
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
                # Introducir ComboBox
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                combobox.setCurrentText(str(dataDesp[i][2]))
                self.ui.tbl_desp.setCellWidget(i, 2, combobox)

        ###########################
        # Dibujo de Restricciones #
        ###########################
        self.ploteo = self.ui.wgt_restricciones.canvas
        self.ploteo.ax.clear()
        # Apoyo Libre
        self.ploteo.ax.plot(1, 2, 'oc', ms = 10)
        self.ploteo.ax.text(1, 0, "Libre", weight = 'bold',color = 'k')
        # Apoyo Fijo
        self.ploteo.ax.plot(2, 2, 'sr', ms=10)
        self.ploteo.ax.text(2, 0, "Fijo", weight='bold', color='k')
        # Apoyo DX
        self.ploteo.ax.plot(3, 2, '^r', ms=10)
        self.ploteo.ax.text(3, 0, "DX", weight='bold', color='k')
        # Apoyo DY
        self.ploteo.ax.plot(4, 2, '<r', ms=10)
        self.ploteo.ax.text(4, 0, "DY", weight='bold', color='k')
        # Ejes Max y Min
        self.ploteo.ax.axis([0, 5, -3, 5])
        # Maximizar espacio
        self.ploteo.fig.subplots_adjust(0,0,1,1)
        # Dibujar en lienzo
        self.ploteo.draw()















    def Wgt_ComboBox(self):
        self.ui.cb_paginas.currentTextChanged.connect(self.CambiarPagina)
        self.ui.cb_elemento.currentTextChanged.connect(self.Fn_MatricesRigidezGUI)

    def Wgt_SpinBox(self):
        self.ui.sp_numElem.valueChanged.connect(self.AnadirRenglonSinCombo)
        self.ui.sp_numNodo.valueChanged.connect(lambda: self.AnadirRenglonConCombo('N'))
        self.ui.sp_fuerzas.valueChanged.connect(lambda: self.AnadirRenglonConCombo('F'))
        self.ui.sp_desp.valueChanged.connect(lambda: self.AnadirRenglonConCombo('D'))

    def Wgt_PushButton(self):
        self.ui.btn_visualizar.clicked.connect(self.Fn_VisualzarArmadura)
