# modelos/individuo.py

# Importaciones de terceros
import numpy as np


class Individuo:
    """Implementa un individuo de la población."""

    def __init__(self, tour, matriz):
        self.tour = tour
        self.matriz = matriz
        self.distancia = self.calcular_distancia(self.matriz)


    def calcular_distancia(self, matriz):
        """Calcula la distancia total de un tour."""
        return np.sum(matriz[self.tour[:-1], self.tour[1:]]) + matriz[self.tour[-1], self.tour[0]]


    def mutar(self):
        """Realiza una mutación (2-opt) en el individuo."""
        pass