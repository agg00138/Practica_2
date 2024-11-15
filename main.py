# main.py

# Importaciones de bibliotecas estándar
import sys, os, random

# Importaciones locales
from auxiliares.crear_logs import Logger
from auxiliares.funciones_generales import generar_semillas
from auxiliares.procesador_archivos import ProcesadorTXT, ProcesadorTSP
from algoritmos.AlgGEN_Clase01_Grupo06 import Generacional
from algoritmos.AlgEST_Clase01_Grupo06 import Estacionario

# Importaciones de terceros
import numpy as np


def procesar_archivos_tsp(archivos_tsp, params, semillas):
    """Procesamiento de los archivos (.tsp)."""

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

            # Crea los ficheros logs
            log_gen = Logger(nombre_algoritmo='GEN',archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i, echo=params['echo'])
            log_est = Logger(nombre_algoritmo='EST',archivo_tsp={'nombre': archivo}, semilla=semilla, num_ejecucion=i, echo=params['echo'])

            # PRUEBA 03: Generacional
            # Ejecuta el algoritmo evolutivo generacional
            log_gen.registrar_evento(f'Ejecutando Algoritmo GENERACIONAL con la semilla {semilla}:')
            generacional = Generacional(matriz, params)  # Crea una instancia del algoritmo generacional
            generacional.ejecutar(logger=log_gen)  # Ejecuta el algoritmo

            # Muestra resultados
            log_gen.registrar_evento(f'Generación final alcanzada: {generacional.generacion}')
            log_gen.registrar_evento(f'Evaluaciones realizadas: {generacional.evaluaciones}')
            mejor_individuo = min(generacional.poblacion.individuos, key=lambda ind: ind.fitness)
            log_gen.registrar_evento(f'Mejor tour encontrado: {mejor_individuo.tour}')
            log_gen.registrar_evento(f'Distancia total del mejor tour: {mejor_individuo.distancia:.2f}\n')

            # PRUEBA 04: Estacionario
            # Ejecuta el algoritmo evolutivo estacionario
            log_est.registrar_evento(f'Ejecutando Algoritmo ESTACIONARIO con la semilla {semilla}:')
            estacionario = Estacionario(matriz, params)  # Crea una instancia del algoritmo estacionario
            estacionario.ejecutar(logger=log_est)  # Ejecuta el algoritmo

            # Muestra resultados
            log_est.registrar_evento(f'Generación final alcanzada: {estacionario.generacion}')
            log_est.registrar_evento(f'Evaluaciones realizadas: {estacionario.evaluaciones}')
            mejor_individuo = min(estacionario.poblacion.individuos, key=lambda ind: ind.fitness)
            log_est.registrar_evento(f'Mejor tour encontrado: {mejor_individuo.tour}')
            log_est.registrar_evento(f'Distancia total del mejor tour: {mejor_individuo.distancia:.2f}\n')



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

    # Crear logs si params['echo'] es False
    if not params['echo']:
        os.makedirs('logs', exist_ok=True)

    # Procesa los archivos
    procesar_archivos_tsp(archivos_tsp, params, semillas)


if __name__ == '__main__':
    main()