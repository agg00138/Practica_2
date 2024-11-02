# main.py

# Importaciones de bibliotecas estándar
import sys
import os
import random

# Importaciones locales
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
from auxiliares.funciones_generales import generar_semillas
from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio

# Importaciones de terceros
import numpy as np


def print_hi(name):
    # Muestra un mensaje de bienvenida.
    print(f'¡Hola {name}! 👋 Esperamos que te guste nuestra práctica. ¡Estamos muy emocionados! 😊🚀💻\n')

def main():
    # Comprueba que se pasen 2 argumentos por consola
    if len(sys.argv) != 2:
        print('Uso: (python | py) ./main.py ./config.txt')
        sys.exit(1)

    # Almacena el fichero config.txt
    archivo_config = sys.argv[1]
    txt = ProcesadorTXT(archivo_config)
    parametros = txt.cargar_datos()

    print('Parámetros procesados:')
    for clave, valor in parametros.items():
        print(f'{clave} = {valor}')

    # Genera las semillas
    semillas = generar_semillas(parametros['dni'], parametros['num_ejecuciones'])

    print('Semillas generadas:', semillas)

    # Obtiene los archivos .tsp
    archivos_tsp = parametros['archivos']

    # Procesa un archivo .tsp
    for archivo_tsp in archivos_tsp:
        ruta_archivo = os.path.join('data', archivo_tsp)
        tsp = ProcesadorTSP(ruta_archivo)
        matriz, tour = tsp.cargar_datos()
        print('\n======================')
        print(f'Procesando {archivo_tsp}:')
        print('======================')

        # Ejecuta el algoritmo greedy aleatorio (comprobación)
        for i, semilla in enumerate(semillas, start=1):
            # Configura la semilla para esta ejecución
            random.seed(semilla)
            np.random.seed(semilla)

            # Ejecuta el algoritmo Greedy como ejemplo (esto también aplicaría a otros algoritmos)
            greedy = GreedyAleatorio(matriz, parametros)
            tour, distancia = greedy.ejecutar()
            tsp.mostrar_tour(tour)
            print(f'Distancia: {distancia}\n')

# Presiona el botón de 'play' para ejecutar el script.
if __name__ == '__main__':
    print_hi('Cristobal')
    main()