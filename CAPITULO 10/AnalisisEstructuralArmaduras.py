import numpy as np
import math

class MiembroArmadura():
    '''
    Descripción:
    Esta clase sirve para obtener las propiedades de cualquier elemento de una armadura.

    Funciones:
    --> Longitud(self)
    --> Rig_Loc(self)
    --> def Lambda_X(self)
    --> def Lambda_Y(self)
    --> def Trans(self)
    --> def Rig_Glob(self)

    Programó:
    Ing. Josue Emmanuel Cruz Barragan
    '''
    def __init__(self, elemento, area, modElasticidad, coordenada_xi, coordenada_yi, coordenada_xf, coordenada_yf, vec_coord):

        ####################
        # Datos de entrada #
        ####################

        self.elem = elemento
        self.A = area
        self.E = modElasticidad
        self.xi = coordenada_xi
        self.yi = coordenada_yi
        self.xf = coordenada_xf
        self.yf = coordenada_yf
        self.vc = vec_coord

        ###############
        # Propiedades #
        ###############

        self.L = self.Longitud()
        self.k_loc = self.Rig_Loc()
        self.lx = self.Lambda_X()
        self.ly = self.Lambda_Y()
        self.T = self.Trans()
        self.k_glob = self.Rig_Glob()

        #######################################################
        # Funciones para obtener las propiedades del elemento #
        #######################################################

    def __str__(self):
        print("Area: ", self.A)
        print("Mod. Elasticidad: ", self.E)
        print("Coordenadas Iniciales: ({} , {})".format(self.xi, self.yi))
        print("Coordenadas Finales: ({} , {})".format(self.xf, self.yf))
        print("Vector de Cooredenadas: ", self.vc)
        print("Longitud: ", self.L)
        print("Rigidez Local:", self.k_loc)
        print("Lx = ", self.lx ,"  Ly = ", self.ly )
        print("Matriz de Transformacion: ", self.T)
        print("")
        print("Rigidez global del elemento:", self.k_glob)
        return ""

    def Longitud(self):
        """Calcula la longitud del elemento."""
        return math.sqrt((self.xf - self.xi )**2 + (self.yf - self.yi )**2)

    def Rig_Loc(self):
        """Calcula la matriz de rigidez local del elemento."""
        return (self. A *self. E /self.L) * np.array([[1 ,-1] ,[-1 ,1]])

    def Lambda_X(self):
        """Calcula la lambda X del elemento."""
        return (self.xf - self.xi ) /self.L

    def Lambda_Y(self):
        """Calcula la lambda Y del elemento."""
        return (self.yf - self.yi ) /self.L

    def Trans(self):
        """Calcula la matriz de tarnsformación del elemento."""
        return np.array([[self.lx, self.ly, 0, 0] ,[0, 0, self.lx, self.ly]])

    def Rig_Glob(self):
        """Calcula la matriz de rigidez global del elemento."""
        Tt = np.transpose(self.T)
        Tt_k_loc = np.matmul(Tt ,self.k_loc)
        return np.matmul(Tt_k_loc ,self.T)


class AnalisisMatricial():
    '''
    Descripción:
    Esta clase sirve para resolver cualquier armadura en 2D, tanto isostatica como hiperestatica. Tambien nos permite acceder
    a las propiedades de cuaquiera de sus elementos y a las reacciones, desplazamientos, fuerzas internas, etc.

    Funciones:
    --> VectorCoordenadasGlobales(self)
    --> Matriz_PI(self)
    --> Armadura(self)
    --> MatrizRigidezGlobal(self)
    --> MatrziRigidezGlobalParciales(self)
    --> VecFrzasGlobalesConocidas(self):
    --> VecDespGlobalesConocidas(self)
    --> ReaccionesDesplazamientos(self)
    --> TensionCompresion(self)

    Programó:
    Ing. Josue Emmanuel Cruz Barragan
    '''

    def __init__(self, tbl_Elem, tbl_Nods, tbl_Frza, tbl_Desp):

        ####################
        # Datos de entrada #
        ####################

        self.tE = tbl_Elem  # Tabla de elementos.
        self.tN = tbl_Nods  # Tabla de nodos.
        self.tF = tbl_Frza  # Tabla de fuerzas.
        self.tD = tbl_Desp  # Tabla de desplazamientos.

        ###############
        # Propiedades #
        ###############

        self.nE = len(self.tE)  # Número de elementos en la estructura.
        self.nN = len(self.tN)  # Número de nodos en la estructura.
        self.nGl = self.nN * 2  # Número de grados de libertad en la estructura.
        # [Número de reacciones, Número de fuerzas conocidas, Diccionario de nodos]
        [self.nR, self.nFc, self.N] = self.VectorCoordenadasGlobales()
        self.PI = np.array(self.Matriz_PI())  # Matriz PI.
        self.Armad = self.Armadura()  # Lista de las propiedades de los elementos.
        self.Kg = self.MatrizRigidezGlobal()  # Matriz de rigidez global del elemento.
        [self.k11, self.k12, self.k21,
         self.k22] = self.MatrziRigidezGlobalParciales()  # Sub-matrices de rigidez global.
        self.Fc = self.VecFrzasGlobalesConocidas()  # Vector de fuerzas globales conocidas.
        self.Dc = self.VecDespGlobalesConocidas()  # Vector de desplazamientos globales conocidos.
        # [Desplazamientos Desconocidos, Fuerzas Desconocidas, Fuerzas Globales, Desplazamientos Globales]
        [self.Dd, self.Fd, self.Fg, self.Dg] = self.ReaccionesDesplazamientos()
        self.TC = self.TensionCompresion()  # Fuerzas internas en los elementos de la estructura.

        #########################
        # Funciones de la clase #
        #########################

    def __str__(self):
        print("Numero de Elementos: ", self.nE)
        print("Numero de Nodos: ", self.nN)
        print("Numero de Grados de Libertad: ", self.nGl)
        print("Numero de Reacciones: ", self.nR)
        print("Numero de Fuerzas Conocidas: ", self.nFc)
        print("Diccionario de Nodos: ", self.N)
        print("\n Matriz PI: \n", self.PI)
        print("\n Elemento 3: \n", self.Armad[2])
        print("\n Matriz de Rigidez Global de la Armadura: \n", self.Kg)
        print("")
        print("\n Matriz de Rigidez k11: \n", self.k11)
        print("\n Matriz de Rigidez k12: \n", self.k12)
        print("\n Matriz de Rigidez k21: \n", self.k21)
        print("\n Matriz de Rigidez k22: \n", self.k22)
        print("")
        print("\n Vector de Fuerzas Conocidas: \n", self.Fc)
        print("")
        print("\n Vector de Desplazamientos Conocidos: \n", self.Dc)
        print("")
        print("Vector de Desplazamientos Desconocidos: \n", self.Dd)
        print("")
        print("Vector de Fuerzas Desconocidas: \n", self.Fd)
        print("")
        print("Vector de Fuerzas Globales: \n", self.Fg)
        print("")
        print("Vector de Desplazamientos Globales: \n", self.Dg)
        print("")
        print("Vector de Fuerzas Internas: \n", self.TC)
        return ""

    def VectorCoordenadasGlobales(self):
        """Calcula el número de reacciones, número de fuerzas conocidas y un diccionario de nodos."""
        numReacciones = 0
        DiccionarioNodos = {}
        c = 1
        gl = self.nGl

        for i in range(self.nN):
            tipo = self.tN[i][3]

            NODO_key = self.tN[i][0]
            cx = self.tN[i][1]
            cy = self.tN[i][2]

            if tipo == "Libre":
                numReacciones += 0
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, c, c + 1])
                c += 2

            elif tipo == "Fijo":
                numReacciones += 2
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, gl - 1, gl])
                gl -= 2

            elif tipo == "DX":
                numReacciones += 1
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, c, gl])
                c += 1
                gl -= 1

            elif tipo == "DY":
                numReacciones += 1
                DiccionarioNodos.setdefault(NODO_key, [cx, cy, gl, c])
                c += 1
                gl -= 1

        numFuerzasConocidas = self.nGl - numReacciones
        return numReacciones, numFuerzasConocidas, DiccionarioNodos

    def Matriz_PI(self):
        """Calcula la matriz de permutación PI."""
        PI = []
        for i in range(self.nE):
            ni = self.tE[i][3]
            nf = self.tE[i][4]
            PI.append([self.N[ni][2], self.N[ni][3], self.N[nf][2], self.N[nf][3]])
        return PI

    def Armadura(self):
        """Calcula la lista de propiedades de cada elemento de la armadura."""
        Elem = []
        for i in range(self.nE):
            el = self.tE[i][0]
            a = self.tE[i][1]
            me = self.tE[i][2]
            NI = self.tE[i][3]
            NF = self.tE[i][4]
            xi = self.N[NI][0]
            yi = self.N[NI][1]
            xf = self.N[NF][0]
            yf = self.N[NF][1]
            clix = self.N[NI][2]
            cliy = self.N[NI][3]
            clfx = self.N[NF][2]
            clfy = self.N[NF][3]
            Elem.append(MiembroArmadura(el, a, me, xi, yi, xf, yf, [clix, cliy, clfx, clfy]))
        return Elem

    def MatrizRigidezGlobal(self):
        """Calcula la matriz de rigidez global de la armadura."""
        K = np.zeros((self.nGl, self.nGl))
        for e in range(self.nE):
            ke_global = self.Armad[e].k_glob
            for i in range(4):
                for j in range(4):
                    a = self.PI[e, i] - 1
                    b = self.PI[e, j] - 1
                    K[a, b] = ke_global[i, j] + K[a, b]
        return K

    def MatrziRigidezGlobalParciales(self):
        """Calcula las sub-matrices de rigidez global de la armadura."""
        k11 = self.Kg[0:self.nFc, 0:self.nFc]
        k12 = self.Kg[0:self.nFc, self.nFc:self.nGl]
        k21 = self.Kg[self.nFc:self.nGl, 0:self.nFc]
        k22 = self.Kg[self.nFc:self.nGl, self.nFc:self.nGl]
        return k11, k12, k21, k22

    def VecFrzasGlobalesConocidas(self):
        """Calcula el vector de fuerzas globales conocidas de la armadura."""
        Fc = np.zeros((self.nFc, 1))
        for i in range(len(self.tF)):
            direccion = self.tF[i][2]
            nodo = self.tF[i][1]
            if direccion == 'DX':
                j = self.N[nodo][2] - 1
            elif direccion == 'DY':
                j = self.N[nodo][3] - 1
            Fc[j] = self.tF[i][0]
        return Fc

    def VecDespGlobalesConocidas(self):
        """Calcula el vector de desplazamientos globales conocidos de la armadura."""
        Dc = np.zeros((self.nGl - self.nFc, 1))
        for i in range(len(self.tD)):
            direccion = self.tD[i][2]
            nodo = self.tD[i][1]
            if direccion == 'DX':
                j = self.N[nodo][2] - 1 - self.nFc
            elif direccion == 'DY':
                j = self.N[nodo][3] - 1 - self.nFc
            Dc[j] = self.tD[i][0]
        return Dc

    def ReaccionesDesplazamientos(self):
        """Calcula los vectores de desplazamientos y fuerzas desconocidas, asi como las fuerzas y desplazamientos globales."""
        k11_inv = np.linalg.inv(self.k11)
        Dd = np.matmul(k11_inv, (self.Fc - np.matmul(self.k12, self.Dc)))
        Fd = np.matmul(self.k21, Dd) + np.matmul(self.k22, self.Dc)
        Fg = np.concatenate((self.Fc, Fd), axis=0)
        Dg = np.concatenate((Dd, self.Dc), axis=0)
        return Dd, Fd, Fg, Dg

    def TensionCompresion(self):
        """Calcula el vector de fuerzas internas de cada elemento de la armadura."""
        TC = []
        for e in range(self.nE):
            Te = self.Armad[e].T
            ke_loc = self.Armad[e].k_loc
            dix = self.Dg[self.Armad[e].vc[0] - 1]
            diy = self.Dg[self.Armad[e].vc[1] - 1]
            dfx = self.Dg[self.Armad[e].vc[2] - 1]
            dfy = self.Dg[self.Armad[e].vc[3] - 1]
            D = np.array([dix, diy, dfx, dfy])
            ke_loc_Te = np.matmul(ke_loc, Te)
            ke_loc_Te_D = np.matmul(ke_loc_Te, D)
            TC.append(round(float(ke_loc_Te_D[1]), 2))
        return TC