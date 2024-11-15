# algoritmos/AlgEST_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.poblacion import Poblacion
from modelos.individuo import Individuo

# Importaciones de tercero
import numpy as np


class Estacionario:
    """Implementa un algoritmo evolutivo estacionario (EST)."""

    def __init__(self, matriz, params):
        self.matriz = matriz
        self.params = params
        self.generacion = 0
        self.evaluaciones = 0
        self.inicio_tiempo = time.time()  # Iniciar el tiempo de ejecución

        # Inicializar la población
        self.poblacion = Poblacion(self.generacion, self.matriz, self.params)


    def ejecutar(self, logger=None):
        """Ejecuta el algoritmo evolutivo estacionario."""
        self.poblacion.inicializar(logger=logger)  # Inicializa la población
        self.evaluar()  # Evalúa la población actual
        while not self.condicion_parada():
            # Paso 2: Selección de padres
            padre1, padre2 = self.seleccionar()

            # Paso 3: Recombinar los padres y generar dos hijos
            hijo1, hijo2 = self.recombinar(padre1, padre2)

            # Paso 4: (Opcional) Mutación de los hijos
            self.mutar(hijo1)
            self.mutar(hijo2)

            # Paso 5: Evaluación de los hijos
            self.evaluar_individuos([hijo1, hijo2])

            # Paso 6: Reemplazo de los peores individuos en la población
            self.reemplazar(hijo1, hijo2)


    def evaluar(self, poblacion_descendiente=None):
        """Evalua toda la población."""
        if poblacion_descendiente is None:
            for individuo in self.poblacion.individuos:
                # Asumimos que la distancia ya está calculada
                self.evaluaciones += 1
        else:
            for individuo in poblacion_descendiente.individuos:
                self.evaluaciones += 1


    def seleccionar(self):
        """Selecciona dos individuos mediante torneo binario con kBest=2."""
        torneo1 = random.sample(self.poblacion.individuos, self.params['kBest'])
        torneo2 = random.sample(self.poblacion.individuos, self.params['kBest'])

        # Selecciona el mejor individuo de cada torneo
        padre1 = min(torneo1, key=lambda individuo: individuo.fitness)
        padre2 = min(torneo2, key=lambda individuo: individuo.fitness)

        return padre1, padre2


    def recombinar(self, padre1, padre2):
        """Recombina dos padres para generar dos hijos (probabilidad 100%)."""
        if self.params['cruce'] == 'OX2':
            hijo1 = self.cruce_ox2(padre1, padre2)
            hijo2 = self.cruce_ox2(padre2, padre1)
        else:
            hijo1 = self.cruce_moc(padre1, padre2)
            hijo2 = self.cruce_moc(padre2, padre1)

        return hijo1, hijo2


    @staticmethod
    def cruce_ox2(padre1, padre2):
        """Aplica el cruce OX2 entre dos padres para generar un hijo."""
        n = len(padre1.tour)  # Número de ciudades en el tour

        # Elegir al azar varias posiciones del padre2
        num_posiciones = random.randint(1, max(1, n // 3))  # Selecciona aproximadamente el 33% del tour
        posiciones_p2 = np.random.choice(range(n), size=num_posiciones, replace=False)
        posiciones_p2.sort()

        # Seleccionamos los elementos en esas posiciones
        elementos_p2 = padre2.tour[posiciones_p2]

        # Localizamos las posiciones que ocupan esos elementos en padre1
        posiciones_p1 = np.where(np.isin(padre1.tour, elementos_p2))

        # Crea un nuevo individuo hijo
        hijo_tour = padre1.tour.copy()
        hijo_tour[posiciones_p1] = -1  # equivale a '*'

        # Completa con los elementos no repetidos de padre2
        # elementos_no_repe_p2 = padre2.tour[~np.isin(padre2.tour, padre1.tour)]
        hijo_tour[posiciones_p1] = elementos_p2

        hijo = Individuo(hijo_tour, padre1.matriz)  # El fitness se calcula automáticamente

        return hijo


    @staticmethod
    def cruce_moc(padre1, padre2):
        """Aplica el cruce MOC entre dos padres para generar un hijo."""
        n = len(padre1.tour)  # Número de ciudades en el tour

        # Elegir un punto de cruce al azar
        punto_cruce = random.randint(1, n - 2)  # Se elige el punto evitando los extremos

        # Identifica la mitad derecha de padre2
        mitad_der_padre2 = padre2.tour[punto_cruce:]

        # Verificar si cada elemento de padre1 está en mitad_der_padre2
        esta_en_padre2 = np.isin(padre1.tour, mitad_der_padre2)
        indices_padre1 = np.where(esta_en_padre2)[0]  # índices de los elementos de padre1 que están en padre2

        hijo_tour = padre1.tour.copy()
        hijo_tour[indices_padre1] = -1  # equivale a '*'

        # Completa las posiciones '*' con los elementos de la mitad derecha de padre2
        hijo_tour[indices_padre1] = mitad_der_padre2

        hijo = Individuo(hijo_tour, padre1.matriz)  # El fitness se calcula automáticamente

        return hijo


    def mutar(self, individuo):
        """Aplica mutación a un individuo con probabilidad per_mutacion."""
        if random.random() < self.params['per_mutacion']:
            individuo.mutar()


    def evaluar_individuos(self, individuos):
        """Evalúa una lista de individuos para calcular su fitness."""
        for individuo in individuos:
            self.evaluaciones += 1


    def reemplazar(self, hijo1, hijo2):
        """Reemplaza los dos peores individuos en la población con los hijos."""
        # Seleccionar los dos peores individuos mediante torneo de perdedores
        torneo = random.sample(self.poblacion.individuos, self.params['kWorst'])
        peor_individuo1 = max(torneo, key=lambda individuo: individuo.fitness)
        self.poblacion.individuos.remove(peor_individuo1)

        torneo = random.sample(self.poblacion.individuos, self.params['kWorst'])
        peor_individuo2 = max(torneo, key=lambda individuo: individuo.fitness)
        self.poblacion.individuos.remove(peor_individuo2)

        # Añadir los hijos
        self.poblacion.individuos.extend([hijo1, hijo2])


    def condicion_parada(self):
        """
        Verifica si el algoritmo ha llegado al máximo de evaluaciones,
        o han transcurrido 60 segundos.
        """
        tiempo_transcurrido = time.time() - self.inicio_tiempo  # Tiempo transcurrido en segundos
        max_evaluaciones = self.params['max_evaluaciones']
        max_tiempo = self.params['tiempo']

        return self.evaluaciones >= max_evaluaciones or tiempo_transcurrido >= max_tiempo