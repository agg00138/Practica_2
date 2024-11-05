# modelos/individuo.py

# Importaciones locales
from auxiliares.funciones_generales import factorizacion

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

        self.fitness = distancia    # Valor fitness del individuo


    def calcular_distancia(self, matriz):
        """Calcula la distancia total de un tour."""
        return np.sum(matriz[self.tour[:-1], self.tour[1:]]) + matriz[self.tour[-1], self.tour[0]]


    def mutar(self):
        """Realiza una mutación (2-opt) en el individuo."""
        n = len(self.tour)
        i, j = np.random.choice(range(1, n - 1), size=2, replace=False)  # Evita el primer y último índice

        # Aplica el operador de intercambio 2-opt
        mutacion_tour = self.tour.copy()
        mutacion_tour[i], mutacion_tour[j] = self.tour[j], self.tour[i]

        # Calcula (eficientemente) la distancia total del nuevo tour
        arcos_desaparecen, arcos_nuevos = factorizacion(self.tour, self.matriz, i, j)
        nueva_distancia_total = self.distancia - arcos_desaparecen + arcos_nuevos

        self.tour = mutacion_tour
        self.distancia = self.fitness = nueva_distancia_total


    def __repr__(self):
        return f'distancia={self.distancia})'