# modelos/individuo.py

# Importaciones de terceros
import numpy as np


class Individuo:
    """Implementa un individuo de la población."""

    def __init__(self, tour, matriz, distancia=0):
        self.tour = tour
        self.matriz = matriz

        if distancia == 0:
            self.distancia = self.calcular_distancia(self.matriz)
        else:
            self.distancia = distancia


    def calcular_distancia(self, matriz):
        """Calcula la distancia total de un tour."""
        return np.sum(matriz[self.tour[:-1], self.tour[1:]]) + matriz[self.tour[-1], self.tour[0]]


    def mutar(self):
        """Realiza una mutación (2-opt) en el individuo."""
        pass