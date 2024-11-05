# main.py

# Importaciones de bibliotecas estándar
import sys, os, random

# Importaciones locales
from auxiliares.funciones_generales import generar_semillas
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
#from algoritmos.AlgGRE_Clase01_Grupo06 import GreedyAleatorio
#from modelos.poblacion import Poblacion
from algoritmos.AlgGEN_Clase01_Grupo06 import Generacional

# Importaciones de terceros
import numpy as np


def print_hi(name):
    """Muestra un mensaje de bienvenida."""
    print(f'👋 ¡Hola, {name}! Bienvenido al mundo de las soluciones optimizadas. 🚀🧬')


def procesar_archivos_tsp(archivos_tsp, params, semillas):
    # Todo: Procesamiento de los archivos .tsp
    for archivo in archivos_tsp:
        ruta_archivo = os.path.join('data', archivo)

        if not os.path.exists(ruta_archivo):
            print(f'Error: El archivo {ruta_archivo} no se encontró.')
            continue

        tsp = ProcesadorTSP(ruta_archivo)
        matriz, tour = tsp.cargar_datos_tsp()

        print('\n========================')
        print(f'Procesando {archivo}:')
        print('========================')

        for i, semilla in enumerate(semillas, start=1):
            random.seed(semilla)
            np.random.seed(semilla)

            # PRUEBA 01: Algoritmo Greedy Aleatorio
            # greedy = GreedyAleatorio(matriz, params)
            # tour, distancia_total = greedy.ejecutar()
            # tsp.mostrar_tour(tour)
            # print(f'>>> Distancia total del tour = {distancia_total:.2f} (metros)\n.')

            # PRUEBA 02: Instancias de Población
            # poblacion = Poblacion(t=0, matriz=matriz, params=params)
            # poblacion.inicializar()
            # for ind in poblacion.individuos:
            #     print(ind.tour)
            #     print(f'>>>distancia del tour = {ind.distancia}\n')

            # PRUEBA 03: Generacional
            # Ejecuta el algoritmo evolutivo generacional
            generacional = Generacional(matriz, params)  # Crea una instancia del algoritmo generacional
            generacional.ejecutar()  # Ejecuta el algoritmo

            # Muestra resultados
            print(f'Generación final alcanzada: {generacional.generacion}')
            print(f'Evaluaciones realizadas: {generacional.evaluaciones}')
            mejor_individuo = min(generacional.poblacion.individuos, key=lambda ind: ind.fitness)
            print(f'Mejor tour encontrado: {mejor_individuo.tour}')
            print(f'Distancia total del mejor tour: {mejor_individuo.distancia}\n')



def main():
    """Función principal"""

    # Comprueba que se pasen dos argumentos
    if len(sys.argv) != 2:
        print('Uso: (python | py) ./main.py ./config.txt')
        sys.exit(1)

    # Carga los datos del config.txt
    archivo_config = sys.argv[1]
    txt = ProcesadorTXT(archivo_config)
    params = txt.cargar_datos_txt()

    print('Parámetros procesados:')
    for clave, valor in params.items():
        print(f'{clave}: {valor}')

    # Genera las semillas pseudoaleatorias
    semillas = generar_semillas(params['dni_alumno'], params['num_ejecuciones'])

    print(f'n.º de semillas: {params["num_ejecuciones"]}')
    print('semillas:', semillas)

    # Carga los archivos .tsp
    archivos_tsp = params['archivos_tsp']

    # Procesa los archivos
    procesar_archivos_tsp(archivos_tsp, params, semillas)


if __name__ == '__main__':
    print_hi('Cristobal')
    main()