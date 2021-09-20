#############
# Librerias #
#############

import math
import numpy as np

#########
# Clase #
#########

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
    M. en I. Josue Emmanuel Cruz Barragan.
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
        print("Lx = ", self.lx,"  Ly = ", self.ly )
        print("Matriz de Transformacion: ", self.T)
        print("")
        print("Rigidez global del elemento:", self.k_glob)
        return ""
    
    def Longitud(self):
        """Calcula la longitud del elemento."""
        return math.sqrt((self.xf-self.xi)**2 + (self.yf-self.yi)**2)
    
    def Rig_Loc(self):
        """Calcula la matriz de rigidez local del elemento."""
        return (self.A*self.E/self.L) * np.array([[1,-1],[-1,1]])
    
    def Lambda_X(self):
        """Calcula la lambda X del elemento."""
        return (self.xf-self.xi)/self.L
    
    def Lambda_Y(self):
        """Calcula la lambda Y del elemento."""
        return (self.yf-self.yi)/self.L
    
    def Trans(self):
        """Calcula la matriz de tarnsformación del elemento."""
        return np.array([[self.lx, self.ly, 0, 0],[0, 0, self.lx, self.ly]])
    
    def Rig_Glob(self):
        """Calcula la matriz de rigidez global del elemento."""
        Tt = np.transpose(self.T)
        Tt_k_loc = np.matmul(Tt,self.k_loc)
        return np.matmul(Tt_k_loc,self.T)
