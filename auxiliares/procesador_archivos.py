# auxiliares/procesador_archivos.py

# Importaciones de bibliotecas estándar
import re

# Importaciones de terceros
import numpy as np
from scipy.spatial.distance import cdist


class ProcesadorTSP:
    """"Procesa archivos de tipo .tsp para leer instancias de problemas específicos"""

    def __init__(self, archivo):
        self.archivo = archivo
        self.matriz_distancias = None
        self.tour = None
        self.identificadores = []

    def cargar_datos(self):
        # Lógica para cargar y procesar el archivo .tsp
        with open(self.archivo, 'r') as archivo:
            lineas = archivo.readlines()

        coordenadas = []
        dimension = 0

        for i, linea in enumerate(lineas):
            if 'DIMENSION' in linea:
                dimension = int(linea.split(':')[1].strip())
                self.matriz_distancias = np.zeros((dimension, dimension))
            elif 'NODE_COORD_SECTION' in linea:
                for j in range(dimension):
                    ciudad, x, y = map(float, lineas[i + 1 + j].split())
                    coordenadas.append((x, y))
                    self.identificadores.append(int(ciudad))
            elif 'EOF' in linea:
                break

        # Calcula la matriz de distancias
        self.matriz_distancias = cdist(coordenadas, coordenadas, 'euclidean')

        # Inicializa el tour
        self.tour = list(range(dimension))
        return self.matriz_distancias, self.tour

    def mostrar_tour(self, tour):
        # Muestra el tour mostrando los identificadores de las ciudades
        identificadores_tour = [self.identificadores[i] for i in tour]
        print("Tour:", identificadores_tour)


class ProcesadorTXT:
    """"Procesa archivos de tipo .txt para leer otros datos específicos"""

    def __init__(self, archivo):
        self.archivo = archivo
        self.parametros = {}

    def cargar_datos(self):
        # Lógica para cargar y procesar el archivo .txt
        with open(self.archivo, 'r') as archivo:
            lineas = archivo.readlines()

        for linea in lineas:
            linea = linea.strip()
            if linea.startswith('#') or not linea:
                continue

            match = re.match(r'(\w+)\s*=\s*(.+)', linea)
            if match:
                clave = match.group(1)
                valor = match.group(2).strip()

                # Convierte los valores a los tipos adecuados
                if valor.startswith('[') and valor.endswith(']'):
                    valor = [x.strip() for x in valor[1:-1].split(',')]
                elif valor.isdigit():
                    valor = int(valor)
                elif valor.replace('.', '', 1).isdigit():
                    valor = float(valor)
                elif valor.lower() in ['yes', 'no']:
                    valor = valor.lower() == 'yes'

                # Almacena en el diccionario los parámetros leídos
                self.parametros[clave] = valor

        return self.parametros