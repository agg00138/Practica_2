# algoritmos/AlgGEN_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.poblacion import Poblacion
from modelos.individuo import Individuo

# Importaciones de tercero
import numpy as np


class Generacional:
    """Implementa un algoritmo evolutivo generacional (GEN)."""

    def __init__(self, matriz, params):
        self.matriz = matriz
        self.params = params
        self.generacion = 0
        self.evaluaciones = 0

        # Inicializar la población
        self.poblacion = Poblacion(self.generacion, self.matriz, self.params)

        # Número de élites a preservar
        self.num_elites = self.params['E']


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo generacional."""
        self.evaluar()  # Evalua la población actual
        while not self.condicion_parada():
            self.generacion += 1

            # Obtiene el élite
            elites = self.obtener_elites()

            # Selecciona la población intermedia P´ desde P(t - 1)
            poblacion_intermedia = self.seleccionar()

            # Recombina los individuos de la población P´ para obtener la descendencia
            poblacion_descendiente = self.recombinar(poblacion_intermedia)

            # Aplica o no una mutación a cada individuo de la población descendiente
            self.mutar(poblacion_descendiente)

            # Evalua la población descendiente después de la mutación
            self.evaluar(poblacion_descendiente)

            # Reemplaza la población P(t) a partir de P(t - 1) y P´
            self.reemplazar(poblacion_descendiente, elites)


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
        """
        Operador de selección basado en un torneo binario con kBest
        Aplicándose tantas veces como individuos tenga la población.
        """
        poblacion_intermedia = Poblacion(self.generacion + 1, self.matriz, self.params)  # Nueva generación

        for _ in range(len(self.poblacion.individuos)):
            # Selecciona kBest individuos aleatoriamente
            torneo = random.sample(self.poblacion.individuos, self.params['kBest'])

            # Compara ambos individuos
            mejor_individuo = min(torneo, key=lambda individuo: individuo.fitness)
            poblacion_intermedia.individuos.append(mejor_individuo)

        return poblacion_intermedia


    def obtener_elites(self):
        """Obtiene el/los mejores individuos como élite."""
        ordenados_por_distancia = sorted(self.poblacion.individuos, key=lambda individuo: individuo.fitness)

        return ordenados_por_distancia[:self.num_elites]


    def recombinar(self, poblacion_intermedia):
        """Recombina una lista de individuos seleccionados en pares."""
        hijos = []

        # Itera sobre la población intermedia en pares
        for i in range(0, len(poblacion_intermedia.individuos), 2):
            padre1 = poblacion_intermedia.individuos[i]
            padre2 = poblacion_intermedia.individuos[i + 1] if i + 1 < len(poblacion_intermedia.individuos) else poblacion_intermedia.individuos[0]

            # Recombina el par de padres seleccionados
            hijo1, hijo2 = self.recombinar_par(padre1, padre2)

            # Añade los hijos a la población descendiente
            hijos.extend([hijo1, hijo2])

        # Crear la población descendiente como una instancia de Población
        poblacion_descendiente = Poblacion(self.generacion + 1, self.matriz, self.params)
        poblacion_descendiente.individuos = hijos[:len(poblacion_intermedia.individuos)]  # Limita el número de hijos

        return poblacion_descendiente


    def recombinar_par(self, padre1, padre2):
        """Aplica recombinación entre dos individuos (padres) para producir dos hijos."""
        # Inicializar los hijos como copias de los padres
        hijo1 = Individuo(padre1.tour.copy(), padre1.matriz)
        hijo2 = Individuo(padre2.tour.copy(), padre2.matriz)

        # Aplicar cruce con una probabilidad del 70%
        if random.random() < self.params['per_cruce']:
            # Elegir al azar entre OX2 y MOC
            if random.random() < 0.5:
                # Aplicar cruce OX2
                hijo1, hijo2 = self.cruce_ox2(padre1, padre2)
            else:
                # Aplicar cruce MOC
                hijo1, hijo2 = self.cruce_moc(padre1, padre2)

        return hijo1, hijo2


    @staticmethod
    def cruce_ox2(padre1, padre2):
        """Aplica el cruce OX2 entre dos padres para generar un hijo."""
        n = len(padre1.tour)    # Número de ciudades en el tour

        # Elegir al azar varias posiciones del padre2
        num_positions = random.randint(1, max(1, n // 3))  # Selecciona aproximadamente el 33% del tour
        posiciones_p2 = np.random.choice(range(n), size=num_positions, replace=False)
        posiciones_p2.sort()

        # Seleccionamos los elementos en esas posiciones
        elementos_p2 = padre2.tour[posiciones_p2]

        # Localizamos las posiciones que ocupan esos elementos en padre1
        posiciones_p1 = np.where(np.isin(padre1.tour[:], elementos_p2))[0]

        # Crea un nuevo individuo hijo
        hijo_tour = padre1.tour.copy()
        hijo_tour[posiciones_p1] = -1   # equivale a '*'

        # Completa con los elementos no repetidos de padre2
        elementos_no_repe_p2 = padre2.tour[~np.isin(padre2.tour, padre1.tour)]
        hijo_tour[posiciones_p1] = elementos_no_repe_p2

        hijo = Individuo(hijo_tour, padre1.matriz)  # El fitness se calcula automáticamente

        return hijo


    @staticmethod
    def cruce_moc(padre1, padre2):
        """Aplica el cruce MOC entre dos padres para generar un hijo."""
        n = len(padre1.tour)    # Número de ciudades en el tour

        # Elegir un punto de cruce al azar
        punto_cruce = random.randint(1, n - 2)  # Se elige el punto evitando los extremos

        # Identifica la mitad derecha de padre2
        mitad_der_padre2 = padre2.tour[punto_cruce:]

        # Verificar si cada elemento de padre1 está en mitad_der_padre2
        esta_en_padre2 = np.isin(padre1, mitad_der_padre2)
        indices_padre1 = np.where(esta_en_padre2)[0]    # índices de los elementos de padre1 que están en padre2

        hijo_tour = padre1.tour.copy()
        hijo_tour[indices_padre1] = -1  # equivale a '*'

        # Completa las posiciones '*' con los elementos de la mitad derecha de padre2
        hijo_tour[indices_padre1] = mitad_der_padre2

        hijo = Individuo(hijo_tour, padre1.matriz)  # El fitness se calcula automáticamente

        return hijo


    def mutar(self, poblacion_descendiente):
        """Con una probabilidad %/individuo se aplica una mutación al individuo."""
        for individuo in poblacion_descendiente.individuos:
            if random.random() < self.params['per_mutacion']:   # Verificar con probabilidad %
                individuo.mutar()


    def reemplazar(self, poblacion_descendiente, elites):
        """
        Reemplaza la población completa por la población descendiente,
        conservando el elitismo si es necesario.
        """
        # Crear un conjunto de élites para facilitar la verificación
        elites_set = set(elites)
        poblacion_descendiente_set = set(poblacion_descendiente.individuos)

        # Comprobar si el/los individuos élites están en la población descendiente
        todos_elites_en_poblacion = elites_set.issubset(poblacion_descendiente_set)

        if todos_elites_en_poblacion:
            # Si todos los individuos élites están en la población descendiente, simplemente
            # asignamos la nueva población descendiente
            self.poblacion.individuos = poblacion_descendiente.individuos[:len(self.poblacion.individuos)]
        else:
            # Sí faltan élites, proceder a realizar el torneo para reemplazar
            for elite in elites:
                if elite not in poblacion_descendiente_set:
                    # Realizar el torneo para elegir un peor individuo
                    torneo = random.sample(poblacion_descendiente.individuos, min(self.params['kWorst'], len(poblacion_descendiente.individuos)))

                    # Identificar el peor individuo en el torneo
                    peor_individuo = min(torneo, key=lambda individuo: individuo.fitness)

                    # Reemplazar al peor individuo por el individuo élite
                    poblacion_descendiente.individuos.remove(peor_individuo)
                    poblacion_descendiente.individuos.append(elite)

            # Asignar la nueva población asegurando el tamaño correcto
            self.poblacion.individuos = poblacion_descendiente.individuos[:len(self.poblacion.individuos)]


    def condicion_parada(self):
        """
        Verifica si el algoritmo ha llegado al máximo de evaluaciones,
        o han transcurrido 60 segundos.
        """
        tiempo_transcurrido = time.time() - self.inicio_tiempo  # Tiempo transcurrido en segundos
        max_evaluaciones = self.params['max_evaluaciones']
        max_tiempo = self.params['tiempo']

        return self.evaluaciones >= max_evaluaciones or tiempo_transcurrido >= max_tiempo