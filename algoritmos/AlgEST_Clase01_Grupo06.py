# algoritmos/AlgEST_Clase01_Grupo06.py

# Importaciones de bibliotecas estándar
import random, time

# Importaciones locales
from modelos.poblacion import Poblacion
from modelos.individuo import Individuo
from auxiliares.funciones_generales import cruce_ox2, cruce_moc

# Importaciones de tercero


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


    def ejecutar(self):
        """Ejecuta el algoritmo evolutivo estacionario."""

        self.poblacion.inicializar()  # Inicializa la población P(t)
        self.evaluar()  # Evalúa la población P(t)

        while not self.condicion_parada():

            # Selecciona los padres
            padre1, padre2 = self.seleccionar()

            # Cruzamos los padres para generar los hijos (probabilidad 100%)
            hijo1, hijo2 = self.recombinar(padre1, padre2)

            # Mutación de los hijos con una cierta probabilidad
            self.mutar(hijo1)
            self.mutar(hijo2)

            # Evaluación de los hijos
            # El fitness se calcula automáticamente al generar el Hijo
            # Siempre se generan 2 hijos, por ello evaluamos 2 veces
            self.evaluaciones += 2

            # Reemplazo de los peores individuos en la población
            self.reemplazar(hijo1, hijo2)


    def evaluar(self):
        """Evalúa la población (NOTA: Las distancias ya están pre calculadas)."""
        self.evaluaciones += len(self.poblacion.individuos)


    def seleccionar(self):
        """Selecciona dos individuos distintos mediante torneo binario con kBest."""
        while True:
            torneo1 = random.sample(self.poblacion.individuos, self.params['kBest'])
            torneo2 = random.sample(self.poblacion.individuos, self.params['kBest'])

            # Selecciona el mejor individuo de cada torneo
            padre1 = min(torneo1, key=lambda individuo: individuo.fitness)
            padre2 = min(torneo2, key=lambda individuo: individuo.fitness)

            # Asegura que los padres seleccionados sean distintos
            if padre1 != padre2:
                break

        return padre1, padre2


    def recombinar(self, padre1, padre2):
        """Recombina dos padres para generar dos hijos (probabilidad 100%)."""
        cruce = self.params['cruce']

        if cruce == 'OX2':
            hijo1, hijo2 = cruce_ox2(padre1, padre2)
        else:
            hijo1, hijo2 = cruce_moc(padre1, padre2)

        return hijo1, hijo2


    def mutar(self, individuo):
        """Aplica mutación a un individuo con probabilidad per_mutacion."""
        if random.random() < self.params['per_mutacion']:
            individuo.mutar()


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