# modelos/individuo.py

# Importaciones locales

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

        self.fitness = self.distancia    # Valor fitness del individuo


    def calcular_distancia(self, matriz):
        """Calcula la distancia total de un tour."""
        return np.sum(matriz[self.tour[:-1], self.tour[1:]]) + matriz[self.tour[-1], self.tour[0]]


    def mutar(self):
        """Realiza una mutación (2-opt) en el individuo."""
        n = len(self.tour)
        i, j = np.random.choice(range(1, n - 1), size=2, replace=False)  # Evita el primer y último índice

        # Aplica el operador de intercambio 2-opt
        arcos_desaparecen, arcos_nuevos = self.factorizacion(i, j)
        nueva_distancia_total = self.distancia - arcos_desaparecen + arcos_nuevos

        self.tour[i], self.tour[j] = self.tour[j], self.tour[i]     # Actualiza los índices del tour
        self.distancia = nueva_distancia_total
        self.fitness = nueva_distancia_total


    def factorizacion(self, i, j):
        """Calcula eficientemente la distancia de un tour tras un intercambio 2-opt."""
        n = len(self.tour)

        # Manejar el caso cuando las ciudades son consecutivas
        if abs(i - j) == 1 or (i == 0 and j == n - 1) or (i == n - 1 and j == 0):
            arcos_desaparecen = self.matriz[self.tour[i - 1], self.tour[i]] + self.matriz[self.tour[j], self.tour[(j + 1) % n]]
            arcos_nuevos = self.matriz[self.tour[i - 1], self.tour[j]] + self.matriz[self.tour[i], self.tour[(j + 1) % n]]
        else:
            arcos_desaparecen = (
                    self.matriz[self.tour[i - 1], self.tour[i]] + self.matriz[self.tour[i], self.tour[(i + 1) % n]] +
                    self.matriz[self.tour[j - 1], self.tour[j]] + self.matriz[self.tour[j], self.tour[(j + 1) % n]]
            )
            arcos_nuevos = (
                    self.matriz[self.tour[i - 1], self.tour[j]] + self.matriz[self.tour[j], self.tour[(i + 1) % n]] +
                    self.matriz[self.tour[j - 1], self.tour[i]] + self.matriz[self.tour[i], self.tour[(j + 1) % n]]
            )

        return arcos_desaparecen, arcos_nuevos


    def __repr__(self):
        return f'distancia={self.fitness:.2f}'