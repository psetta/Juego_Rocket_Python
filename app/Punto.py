# ==========================================
#
# Pygame Arkanoid
# Autor: manuel.mayo.lado@gmail.com
#
# ==========================================

import math

class Punto:
    """
    Clase comodín para indicar posición y facilitar calculos
    """
    def __init__(self,*pos):
        """
        ::args
        :pos[0][float]: Posición en el eje x
        :pos[1][float]: Posición en el eje y
        """
        self.x = pos[0]
        self.y = pos[1]

    # suma
    def __add__(self,other):
        if type(other) == Punto:
            return Punto(self.x+other.x,self.y+other.y)
        else:
            return Punto(self.x+other,self.y+other)

    # resta
    def __sub__(self,other):
        return Punto(self.x-other.x,self.y-other.y)

    # multiplicación
    def __mul__(self,other):
        if type(other) == Punto:
            return Punto(self.x*other.x,self.y*other.y)
        else:
            return Punto(self.x*other,self.y*other)

    # len
    def __len__(self):
        return 2

    # string
    def __str__(self):
        return "Punto({0},{1})".format(self.x,self.y)

    # item
    def __getitem__(self,item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError()

    #round
    def __round__(self):
        return Punto(round(self.x),round(self.y))

    # distancia entre 2 puntos
    def distance(self,other):
        return math.sqrt((other.x-self.x)**2 + (other.y-self.y)**2)
