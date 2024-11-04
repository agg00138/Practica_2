# auxiliares/funciones_generales.py

# Importaciones de bibliotecas estándar
import random

# Importaciones locales
# Importaciones de terceros


def generar_semillas(dni_alumno, num_semillas, offset=0):
    """Genera un número de semillas pseudoaleatorias"""
    if not isinstance(num_semillas, int) or num_semillas <= 0:
        raise ValueError("num_semillas debe ser un entero positivo.")

    random.seed(dni_alumno + offset)
    semillas = [random.randint(1, 100000) for _ in range(num_semillas)]

    return semillas


def factorizacion(tour, matriz, i, j):
    """Calcula eficientemente la distancia de un tour tras un intercambio 2-opt."""
    n = len(tour)

    # Manejar el caso cuando las ciudades son consecutivas
    if abs(i - j) == 1 or (i == 0 and j == n - 1) or (i == n - 1 and j == 0):
        arcos_desaparecen = matriz[tour[i - 1], tour[i]] + matriz[tour[j], tour[(j + 1) % n]]
        arcos_nuevos = matriz[tour[i - 1], tour[j]] + matriz[tour[i], tour[(j + 1) % n]]
    else:
        arcos_desaparecen = (
                matriz[tour[i - 1], tour[i]] + matriz[tour[i], tour[(i + 1) % n]] +
                matriz[tour[j - 1], tour[j]] + matriz[tour[j], tour[(j + 1) % n]]
        )
        arcos_nuevos = (
                matriz[tour[i - 1], tour[j]] + matriz[tour[j], tour[(i + 1) % n]] +
                matriz[tour[j - 1], tour[i]] + matriz[tour[i], tour[(j + 1) % n]]
        )

    return arcos_desaparecen, arcos_nuevos