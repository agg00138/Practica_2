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