# modelos/poblacion.py

# Importaciones locales
from modelos.individuo import Individuo
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio

# Importaciones de terceros
import numpy as np


class Poblacion:
    """Implementa una población de individuos."""

    def __init__(self, generacion, matriz, params):
        self.t = generacion
        self.matriz = matriz
        self.params = params
        self.individuos = []


    def inicializar(self, logger=None):
        num_individuos_aleatoria = int(self.params['tamanio'] * self.params['per_individuos'])
        num_individuos_greedy = (self.params['tamanio'] - num_individuos_aleatoria)

        logger.registrar_evento(f'Nº.Individuos: Aleatorio = {num_individuos_aleatoria} | Greedy.Aleatorio = {num_individuos_greedy}')

        # Generación aleatoria
        for _ in range(num_individuos_aleatoria):
            tour = np.random.permutation(len(self.matriz))
            individuo = Individuo(tour, self.matriz)
            self.individuos.append(individuo)

        # Generación greedy aleatorio
        for _ in range(num_individuos_greedy):
            greedy = GreedyAleatorio(self.matriz, self.params)
            tour, distancia = greedy.ejecutar()
            individuo = Individuo(tour, self.matriz, distancia)
            self.individuos.append(individuo)