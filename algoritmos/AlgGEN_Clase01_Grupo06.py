# algoritmos/AlgGEN_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.poblacion import Poblacion
from auxiliares.funciones_generales import cruce_ox2, cruce_moc

# Importaciones de tercero


class Generacional:
    """Implementa un algoritmo evolutivo generacional (GEN)."""

    def __init__(self, matriz, params):
        self.matriz = matriz
        self.params = params
        self.generacion = 0               # Será nuestra t
        self.evaluaciones = 0
        self.inicio_tiempo = time.time()  # Iniciar el tiempo de ejecución

        # Inicializar la población
        self.poblacion = Poblacion(self.generacion, self.matriz, self.params)

        # Número de élites a preservar
        self.num_elites = self.params['E']


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo generacional."""

        self.poblacion.inicializar()    # Inicializa la población P(t)
        self.evaluar(self.poblacion)  # Evalúa la población P(t)

        while not self.condicion_parada():
            self.generacion += 1    # t = t + 1

            # Obtiene el élite de P(t) para evitar perderlos
            elites = self.obtener_elites()

            # Selecciona la población intermedia P´ desde P(t - 1)
            poblacion_padres = self.seleccionar()

            # Recombina los individuos de la población P´ para obtener la descendencia
            nueva_poblacion = self.recombinar(poblacion_padres)

            # Aplica o no una mutación a cada individuo de la población descendiente
            self.mutar(nueva_poblacion)

            # Evalúa la población descendiente (nueva población) P(t)
            self.evaluar(nueva_poblacion)

            # Reemplaza la población P(t) a partir de P(t - 1) y P´
            self.reemplazar(nueva_poblacion, elites)


    def evaluar(self, poblacion):
        """Evalúa la población al completo."""

        # Asumimos que la distancia ya está calculada
        self.evaluaciones += len(poblacion.individuos)


    def seleccionar(self):
        """
        Operador de selección basado en un torneo binario con kBest
        Aplicándose tantas veces como individuos tenga la población.
        """
        poblacion_intermedia = Poblacion(self.generacion, self.matriz, self.params)  # Nueva generación

        for _ in range(len(self.poblacion.individuos)):
            # Selecciona kBest individuos distintos para el torneo
            while True:
                torneo = random.sample(self.poblacion.individuos, self.params['kBest'])
                if len(torneo) == len(set(torneo)):  # Asegura que los individuos son distintos
                    break

            # Selecciona el mejor individuo del torneo
            mejor_individuo = min(torneo, key=lambda individuo: individuo.fitness)
            poblacion_intermedia.individuos.append(mejor_individuo)

        return poblacion_intermedia


    def obtener_elites(self):
        """Obtiene el/los mejores individuos como élite."""
        ordenados_por_distancia = sorted(self.poblacion.individuos, key=lambda individuo: individuo.fitness)

        return ordenados_por_distancia[:self.num_elites]


    def recombinar(self, poblacion_padres):
        """Lanza una moneda y cruza aquellos individuos de la población para generar los hijos"""

        hijos = []
        num_lanzamientos = int(len(poblacion_padres.individuos) / 2)
        cruce = self.params['cruce']

        # Si el tamaño de la población es N, se requieren N/2 "cruces"
        for _ in range(num_lanzamientos):

            # Selecciono dos padres aleatoriamente
            padre1, padre2 = random.sample(poblacion_padres.individuos, 2)

            # Lanza una moneda aleatoriamente
            if random.random() < self.params['per_cruce']:

                if cruce == 'OX2':
                    hijo1, hijo2 = cruce_ox2(padre1, padre2)
                else:
                    hijo1, hijo2 = cruce_moc(padre1, padre2)
            else:
                hijo1, hijo2 = padre1, padre2

            # Añado cada hijo a la lista
            hijos.extend([hijo1, hijo2])

        # Una vez que tenemos todos los hijos creamos una nueva población de descendientes
        poblacion_descendiente = Poblacion(self.generacion, self.matriz, self.params)
        poblacion_descendiente.individuos = hijos[:len(poblacion_padres.individuos)]    # aseguro que sea del mismo tamaño

        return poblacion_descendiente


    def mutar(self, poblacion_descendiente):
        """Con una probabilidad %/individuo se aplica una mutación al individuo."""
        for individuo in poblacion_descendiente.individuos:
            if random.random() < self.params['per_mutacion']:   # Verificar con probabilidad %
                individuo.mutar()


    def reemplazar(self, nueva_poblacion, elites):
        """Reemplaza la población completa por la nueva población conservando el elitismo."""

        # Creamos un conjunto de élites
        conjunto_elites = set(elites)

        for elite in conjunto_elites:
            if elite not in nueva_poblacion.individuos:

                # Realiza un torneo de perdedores
                torneo = random.sample(nueva_poblacion.individuos, self.params['kWorst'])
                peor_individuo = max(torneo, key=lambda individuo: individuo.fitness)
                nueva_poblacion.individuos.remove(peor_individuo)
                nueva_poblacion.individuos.append(elite)

        # Reemplaza por la nueva población
        self.poblacion = nueva_poblacion


    def condicion_parada(self):
        """
        Verifica si el algoritmo ha llegado al máximo de evaluaciones,
        o han transcurrido 60 segundos.
        """
        tiempo_transcurrido = time.time() - self.inicio_tiempo  # Tiempo transcurrido en segundos
        max_evaluaciones = self.params['max_evaluaciones']
        max_tiempo = self.params['tiempo']

        return self.evaluaciones >= max_evaluaciones or tiempo_transcurrido >= max_tiempo