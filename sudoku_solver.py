from typing import Optional
from sudoku_logic import es_movimiento_valido, colocar_numero, Board


def encontrar_vacio(tablero: Board):
    """Encuentra la primera celda vacía (con 0). Retorna (fila, col) o None."""
    for r in range(9):
        for c in range(9):
            if tablero[r][c] == 0:
                return r, c
    return None


def resolver_sudoku(tablero: Board) -> Optional[Board]:
    """
    Algoritmo Recursivo de Backtracking.
    Retorna un NUEVO tablero resuelto o None si no tiene solución.
    """
    vacio = encontrar_vacio(tablero)

    # Caso Base: Si no hay vacíos, ya terminamos
    if not vacio:
        return tablero

    fila, col = vacio

    # Intentar números del 1 al 9
    for num in range(1, 10):
        if es_movimiento_valido(tablero, fila, col, num):
            # Paso Recursivo: Crear nuevo estado del tablero
            nuevo_tablero = colocar_numero(tablero, fila, col, num)

            # Llamada recursiva con el nuevo estado
            resultado = resolver_sudoku(nuevo_tablero)

            if resultado is not None:
                return resultado

    return None  # Si ningún número funciona, esta rama no tiene solución