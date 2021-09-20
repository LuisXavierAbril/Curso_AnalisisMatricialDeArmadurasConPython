import sys
from PyQt5 import QtWidgets
from UI_Armaduras import Ui_Armaduras
from UI_Functions import Ui_Functions
import AnalisisEstructuralArmaduras as AEA

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

        # Manipular botones
        Ui_Functions.Wgt_PushButton(self)

        # Manipular ComboBox
        Ui_Functions.Wgt_ComboBox(self)



    def AnadirRenglonSinCombo(self):
        val = self.ui.sp_numElem.value()
        self.ui.tbl_elem.setRowCount(val)
        self.ui.tbl_elem.update()

    def AnadirRenglonConCombo(self, var):
        # Añadir renglon en la tabla de Nodos
        if var == 'N':
            val = self.ui.sp_numNodo.value()
            attr = ["Fijo", "Libre", "DX", "DY"]
            self.ui.tbl_nod.setRowCount(val)
            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_nod.setCellWidget(i, 3, combobox)
        # Añadir renglon en la tabla de Fuerzas
        if var == 'F':
            val = self.ui.sp_fuerzas.value()
            attr = ["DX", "DY"]
            self.ui.tbl_fuerzas.setRowCount(val)
            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_fuerzas.setCellWidget(i, 2, combobox)
        # Añadir renglon en la tabla de Desplazamientos
        if var == 'D':
            val = self.ui.sp_desp.value()
            attr = ["DX", "DY"]
            self.ui.tbl_desp.setRowCount(val)
            # Introducir un ComboBox
            for i in range(val):
                combobox = QtWidgets.QComboBox()
                combobox.addItems(attr)
                self.ui.tbl_desp.setCellWidget(i, 2, combobox)

    def Fn_ExtraerDatosTablas(self):
        # Tabla de Elementos
        tbl_elementos = []
        num_elem_tab = self.ui.sp_numElem.value()
        for i in range(num_elem_tab):
            el = str(self.ui.tbl_elem.item(i,0).text())
            a = float(self.ui.tbl_elem.item(i,1).text())
            me = float(self.ui.tbl_elem.item(i,2).text())
            ni = str(self.ui.tbl_elem.item(i,3).text())
            nf = str(self.ui.tbl_elem.item(i,4).text())
            tbl_elementos.append([el, a, me, ni, nf])
        # Tabla de Nodos
        tbl_nodos = []
        num_nodos_tab = self.ui.sp_numNodo.value()
        for i in range(num_nodos_tab):
            nod = str(self.ui.tbl_nod.item(i, 0).text())
            cx = float(self.ui.tbl_nod.item(i, 1).text())
            cy = float(self.ui.tbl_nod.item(i, 2).text())
            tipo = str(self.ui.tbl_nod.cellWidget(i, 3).currentText())
            tbl_nodos.append([nod, cx, cy, tipo])
        # Tabla de Fuerzas
        tbl_fuerzas = []
        num_fuerzas_tab = self.ui.sp_fuerzas.value()
        for i in range(num_fuerzas_tab):
            frza = float(self.ui.tbl_fuerzas.item(i, 0).text())
            f_nod = str(self.ui.tbl_fuerzas.item(i, 1).text())
            dir = str(self.ui.tbl_fuerzas.cellWidget(i, 2).currentText())
            tbl_fuerzas.append([frza, f_nod, dir])
        # Tabla de Desplazamientos
        tbl_desp = []
        num_desp_tab = self.ui.sp_desp.value()
        for i in range(num_desp_tab):
            des = float(self.ui.tbl_desp.item(i, 0).text())
            d_nod = str(self.ui.tbl_desp.item(i, 1).text())
            dir = str(self.ui.tbl_desp.cellWidget(i, 2).currentText())
            tbl_desp.append([des, d_nod, dir])
        # Valores que retona la funcion
        return tbl_elementos, tbl_nodos, tbl_fuerzas, len(tbl_elementos), tbl_desp

    def Fn_DiccionarioNodal(self, tab_N):
        DiccionarioNodos = {}
        c = 1               # Número de grados de libertad que se ajusta al nodo
        nN = len(tab_N)     # Número de nodos
        gl = 2*nN           # Número de grados de libertad totales
        numReacciones = 0   # Número de reacciones que se ajusta al nodo
        for i in range(nN):
            tipo = tab_N[i][3]
            NODO_key = tab_N[i][0]
            cx = tab_N[i][1]
            cy = tab_N[i][2]
            # Apoyo Libre
            if tipo == "Libre":
                numReacciones += 0
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, c, c + 1])
                c += 2
            # Apoyo Fijo
            elif tipo == "Fijo":
                numReacciones += 2
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, gl - 1, gl])
                gl -= 2
            # Apoyo con desplazamiento DX
            elif tipo == "DX":
                numReacciones += 1
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, c, gl])
                c += 1
                gl -= 1
            # Apoyo con desplazamiento DX
            elif tipo == "DY":
                numReacciones += 1
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, gl, c])
                c += 1
                gl -= 1
        # Valores que retona la funcion
        return DiccionarioNodos

    def Fn_VisualzarArmadura(self):
        # Obtenemos los valore de las tablas en la GUI
        [tE, tN, tF, nE, tD] = self.Fn_ExtraerDatosTablas()
        # Cramos el diccionario de nodos
        dic_N = self.Fn_DiccionarioNodal(tN)
        # Inicializamos el lienzo para dibujar la armadura
        self.ploteo = self.ui.wgt_armadura.canvas
        # Limpiamos el lienzo antes de dibujar
        self.ploteo.ax.clear()

        # Dibujo de las barras (Elementos)
        for i in range(nE):
            NI = tE[i][3]
            NF = tE[i][4]
            xi = dic_N[NI][0]
            yi = dic_N[NI][1]
            xf = dic_N[NF][0]
            yf = dic_N[NF][1]
            self.ploteo.ax.plot([xi, xf], [yi, yf], 'k-', linewidth=5)

        # Dibujo de los apoyos (Libre, Fijo, DX, DY)
        for i in range(len(tN)):
            cx = tN[i][1]
            cy = tN[i][2]
            fig = tN[i][3]
            if fig == "Libre":
                self.ploteo.ax.plot(cx, cy, 'oc', ms=15)
            elif fig == "Fijo":
                self.ploteo.ax.plot(cx, cy, 'sr', ms=15)
            elif fig == "DX":
                self.ploteo.ax.plot(cx, cy, '^r', ms=15)
            elif fig == "DY":
                self.ploteo.ax.plot(cx, cy, '<r', ms=15)

        # Límitamos los ejes X y Y
        xmax = 0
        ymax = 0
        for key in dic_N:
            xval = dic_N[key][0]
            yval = dic_N[key][1]
            if xmax < xval:
                xmax = xval
            if ymax < yval:
                ymax = yval

        # Dibujo de las fuerzas
        def Fuerzas(wgt, Direccion, cx, cy, val):
            if Direccion == "DX":
                wgt.annotate("", xy=(cx + xmax / 3, cy), xytext=(cx, cy),
                             arrowprops=dict(arrowstyle="simple", color="m"), size=30)
                wgt.text(cx + xmax / 3, cy, str(val), weight="bold", color="m", size=20)
            elif Direccion == "DY":
                wgt.annotate("", xy=(cx, cy + ymax / 3), xytext=(cx, cy),
                             arrowprops=dict(arrowstyle="simple", color="m"), size=30)
                wgt.text(cx, cy + ymax / 3, str(val), weight="bold", color="m", size=20)
        for i in range(len(tF)):
            Nod = tF[i][1]
            cx = dic_N[Nod][0]
            cy = dic_N[Nod][1]
            Direc = tF[i][2]
            valor = tF[i][0]
            Fuerzas(self.ploteo.ax, Direc, cx, cy, valor)

        # Limitamos los ejes aun valor Max y Min
        self.ploteo.ax.axis([-0.5 * xmax, 1.5 * xmax, -0.5 * ymax, 1.5 * ymax])
        # Maximizar espacio
        self.ploteo.fig.subplots_adjust(0, 0, 1, 1)
        # Dibujar en lienzo
        self.ploteo.draw()

    def CambiarPagina(self):
        val = self.ui.cb_paginas.currentText()
        if val == 'INTRODUCIR DATOS':
            self.ui.stackedWidget.setCurrentWidget(self.ui.pag_1)
        elif val == 'MATRIZ DE RIGIDEZ':
            self.ui.stackedWidget.setCurrentWidget(self.ui.pag_2)
            self.Fn_ElementoCombobox()
        elif val == 'RESULTADOS Y DIAGRAMAS':
            self.ui.stackedWidget.setCurrentWidget(self.ui.pag_3)


    ############################
    # PAGINA MATRIZ DE RIGIDEZ # ##############################################################################
    ############################

    def Fn_ElementoCombobox(self):
        # Obtenemos los valore de las tablas en la GUI
        [tE, tN, tF, nE, tD] = self.Fn_ExtraerDatosTablas()

        for i in range(nE):
            index = self.ui.cb_elemento.findText(str(tE[i][0]))
            self.ui.cb_elemento.removeItem(index)
            self.ui.cb_elemento.addItem(str(tE[i][0]))

    def Fn_MatricesRigidezGUI(self):
        # Obtenemos los valore de las tablas en la GUI
        [tE, tN, tF, nE, tD] = self.Fn_ExtraerDatosTablas()

        # Extraer las Propiedades de la Clase AEA
        ae = AEA.AnalisisMatricial(tE, tN, tF, tD)
        val = str(self.ui.cb_elemento.currentText())
        for i in range(nE):
            if val == ae.Armad[i].elem:
                MatRigLoc = ae.Armad[i].k_loc
                MatRigGlo = ae.Armad[i].k_glob
                MatTrans = ae.Armad[i].T
                val_lx = ae.Armad[i].lx
                val_ly = ae.Armad[i].ly
                [gl1, gl2, gl3, gl4] = ae.Armad[i].vc

        # Tabla MRLE
        self.ui.tbl_MRLE.clearContents()
        self.ui.tbl_MRLE.setRowCount(0)
        for i in range(2):
            self.ui.tbl_MRLE.insertRow(i)
            for j in range(2):
                tb = QtWidgets.QTableWidgetItem(str(round(MatRigLoc[i][j], 4)))
                self.ui.tbl_MRLE.setItem(i,j,tb)
        self.ui.tbl_MRLE.resizeColumnsToContents()

        # Tabla MTE
        self.ui.tbl_MTE.clearContents()
        self.ui.tbl_MTE.setRowCount(0)
        for i in range(2):
            self.ui.tbl_MTE.insertRow(i)
            for j in range(4):
                tb = QtWidgets.QTableWidgetItem(str(round(MatTrans[i][j], 4)))
                self.ui.tbl_MTE.setItem(i, j, tb)
        self.ui.tbl_MTE.resizeColumnsToContents()

        # Tabla MRGE
        self.ui.tbl_MRGE.clearContents()
        self.ui.tbl_MRGE.setRowCount(0)
        for i in range(4):
            self.ui.tbl_MRGE.insertRow(i)
            for j in range(4):
                tb = QtWidgets.QTableWidgetItem(str(round(MatRigGlo[i][j], 4)))
                self.ui.tbl_MRGE.setItem(i, j, tb)
        self.ui.tbl_MRGE.setVerticalHeaderLabels([str(gl1), str(gl2), str(gl3), str(gl4)])
        self.ui.tbl_MRGE.setHorizontalHeaderLabels([str(gl1), str(gl2), str(gl3), str(gl4)])
        self.ui.tbl_MRGE.resizeColumnsToContents()

        # Lambdas X y Y
        self.ui.lbl_LX.setText("Lambda X: " + str(round(val_lx,4)))
        self.ui.lbl_LY.setText("Lambda Y: " + str(round(val_ly, 4)))

        # Tabla MRGA
        MatRigGloArm = ae.Kg
        self.ui.tbl_MRGA.clearContents()
        self.ui.tbl_MRGA.setRowCount(0)
        self.ui.tbl_MRGA.setColumnCount(0)
        cont = 0
        for i in range(ae.nGl):
            self.ui.tbl_MRGA.insertRow(i)
            for j in range(ae.nGl):
                if cont < ae.nGl:
                    self.ui.tbl_MRGA.insertColumn(j)
                    cont += 1
                tb = QtWidgets.QTableWidgetItem(str(round(MatRigGloArm[i][j], 4)))
                self.ui.tbl_MRGA.setItem(i, j, tb)
        self.ui.tbl_MRGA.resizeColumnsToContents()
        self.Fn_Visulaizar2()

    def Fn_Visulaizar2(self):
        # Obtenemos los valore de las tablas en la GUI
        [tE, tN, tF, nE, tD] = self.Fn_ExtraerDatosTablas()
        # Cramos el diccionario de nodos
        dic_N = self.Fn_DiccionarioNodal(tN)
        # Inicializamos el lienzo para dibujar la armadura
        self.ploteo = self.ui.wgt_GL.canvas
        # Limpiamos el lienzo antes de dibujar
        self.ploteo.ax.clear()

        # Dibujo de las barras (Elementos)
        for i in range(nE):
            NI = tE[i][3]
            NF = tE[i][4]
            xi = dic_N[NI][0]
            yi = dic_N[NI][1]
            xf = dic_N[NF][0]
            yf = dic_N[NF][1]
            self.ploteo.ax.plot([xi, xf], [yi, yf], 'k-', linewidth=5)

        # Límitamos los ejes X y Y
        xmax = 0
        ymax = 0
        for key in dic_N:
            xval = dic_N[key][0]
            yval = dic_N[key][1]
            if xmax < xval:
                xmax = xval
            if ymax < yval:
                ymax = yval

        # Dibujo de las fuerzas
        def Fuerzas(wgt, Direccion, cx, cy, val):
            if Direccion == "DX":
                wgt.annotate("", xy=(cx + xmax / 3, cy), xytext=(cx, cy),
                             arrowprops=dict(arrowstyle="simple", color="blue"), size=15)
                wgt.text(cx + xmax / 3, cy, str(val), weight="bold", color="red", size=15)
            elif Direccion == "DY":
                wgt.annotate("", xy=(cx, cy + ymax / 3), xytext=(cx, cy),
                             arrowprops=dict(arrowstyle="simple", color="blue"), size=15)
                wgt.text(cx, cy + ymax / 3, str(val), weight="bold", color="red", size=15)

        for i in range(len(tN)):
            Nod = tN[i][0]
            cx = dic_N[Nod][0]
            cy = dic_N[Nod][1]
            dx = "DX"
            dy = "DY"
            glx = dic_N[Nod][2]
            gly = dic_N[Nod][3]
            Fuerzas(self.ploteo.ax, dx, cx, cy, glx)
            Fuerzas(self.ploteo.ax, dy, cx, cy, gly)

        # Limitamos los ejes aun valor Max y Min
        self.ploteo.ax.axis([-0.2 * xmax, 1.5 * xmax, -0.2 * ymax, 1.5 * ymax])
        # Maximizar espacio
        self.ploteo.fig.subplots_adjust(0, 0, 1, 1)
        # Dibujar en lienzo
        self.ploteo.draw()
























if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    my_app = Ui_MainWindow()
    my_app.show()
    sys.exit(app.exec_())

