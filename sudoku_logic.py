from typing import Tuple
import numpy as np
import random

# Definimos el tablero como una Tupla de Tuplas (Inmutable)
Board = Tuple[Tuple[int, ...], ...]


def crear_tablero_vacio() -> Board:
    """Crea un tablero 9x9 lleno de ceros (vacío) de forma inmutable."""
    return tuple(tuple(0 for _ in range(9)) for _ in range(9))


def es_movimiento_valido_funcional(tablero: Board, fila: int, col: int, num: int) -> bool:
    """
    Validación usando estilo puramente funcional (sin if/for explícitos).
    """
    # Validar fila y columna usando generadores
    fila_ok = num not in tablero[fila]
    col_ok = num not in (tablero[r][col] for r in range(9))

    # Validar cuadrante usando lógica matemática y generadores
    r0, c0 = 3 * (fila // 3), 3 * (col // 3)
    cuadrante = (tablero[r][c] for r in range(r0, r0 + 3) for c in range(c0, c0 + 3))
    cuad_ok = num not in cuadrante

    # Retornar la conjunción de todas las condiciones
    return fila_ok and col_ok and cuad_ok


def colocar_numero(tablero: Board, fila: int, col: int, num: int) -> Board:
    """
    Aplica Inmutabilidad: No cambia el tablero original.
    Crea y retorna una NUEVA copia del tablero con el cambio.
    """
    # Convertimos a lista para editar (solo internamente)
    tablero_lista = [list(fila_t) for fila_t in tablero]
    tablero_lista[fila][col] = num

    # Convertimos de nuevo a tupla antes de retornar para mantener el contrato de inmutabilidad
    return tuple(tuple(fila_t) for fila_t in tablero_lista)


def generar_partida_numpy(cantidad_a_borrar: int = 40) -> Board:
    """
    Genera un tablero de Sudoku válido usando Numpy para la aleatoriedad.
    1. Crea un tablero base.
    2. Lo resuelve (para tener una solución válida).
    3. Elimina números aleatoriamente para crear el puzzle.
    """
    # Usamos Numpy para crear la matriz inicial de ceros
    matriz_np = np.zeros((9, 9), dtype=int)

    # Rellenar las diagonales principales (3 bloques de 3x3) independientemente
    # Esto asegura que el solucionador encuentre una solución válida rápido.
    for i in range(0, 9, 3):
        numeros = np.arange(1, 10)
        np.random.shuffle(numeros)  # Mezcla aleatoria con Numpy
        matriz_np[i:i + 3, i:i + 3] = numeros.reshape(3, 3)

    # Convertimos a nuestro formato inmutable (tupla) para usar el solver
    tablero_inicial = tuple(tuple(int(x) for x in fila) for fila in matriz_np)

    # Importamos aquí para evitar referencias circulares al inicio
    # (El solver necesita logic, y logic ahora necesita solver para generar)
    from sudoku_solver import resolver_sudoku

    # Resolvemos el tablero para tener un juego completo válido
    tablero_resuelto = resolver_sudoku(tablero_inicial)

    if not tablero_resuelto:
        return crear_tablero_vacio()  # Fallback por seguridad

    # Ahora "borramos" números para crear el desafío
    tablero_jugable = [list(fila) for fila in tablero_resuelto]

    # Usamos Numpy para elegir posiciones aleatorias a borrar
    posiciones = [(r, c) for r in range(9) for c in range(9)]
    indices_a_borrar = np.random.choice(len(posiciones), cantidad_a_borrar, replace=False)

    for indice in indices_a_borrar:
        fila, col = posiciones[indice]
        tablero_jugable[fila][col] = 0

    return tuple(tuple(fila) for fila in tablero_jugable)