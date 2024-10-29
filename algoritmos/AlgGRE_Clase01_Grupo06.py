# algoritmos/AlgGRE_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random

# Importaciones de terceros
import numpy as np


class GreedyAleatorio:
    """Implementa el algoritmo greedy aleatorio para la generación de soluciones"""

    def __init__(self, matriz, parametros, semilla):
        self.matriz = matriz
        self.parametros = parametros
        self.semilla = semilla

    def ejecutar(self):
        # Ejecuta el algoritmo con una semilla específica
        random.seed(self.semilla)
        num_ciudades = self.matriz.shape[0]

        tour = []
        visitadas = np.zeros(num_ciudades, dtype=bool)

        # Calcula la suma de cada ciudad al resto
        suma_distancias = np.sum(self.matriz, axis=1)

        # Ordena la ciudades
        ciudades_ordenadas = np.argsort(suma_distancias)

        # Selecciona la ciudad inicial de entre las k más prometedoras
        prometedoras = ciudades_ordenadas[:self.parametros['k']]
        ciudad_actual = random.choice(prometedoras)

        # Añade la ciudad a la solucion
        tour.append(ciudad_actual)
        visitadas[ciudad_actual] = True
        distancia_total = 0.0

        for _ in range(num_ciudades - 1):
            # Filtra las ciudades no visitadas
            no_visitadas = np.where(~visitadas)[0]

            # Obtiene las k más prometedoras
            prometedoras = ciudades_ordenadas[np.isin(ciudades_ordenadas, no_visitadas)][self.parametros['k']]

            # Elige una ciudad aleatoriamente
            ciudad_siguiente = random.choice(prometedoras)

            distancia_total += self.matriz[ciudad_actual, ciudad_siguiente]

            # Actualiza la solución
            tour.append(ciudad_siguiente)
            visitadas[ciudad_siguiente] = True
            ciudad_actual = ciudad_siguiente

        return tour, distancia_total