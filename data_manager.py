import pandas as pd
import os
from datetime import datetime

FILE_NAME = "historial_partidas.csv"


def guardar_partida(jugador: str, dificultad: str, tiempo_segundos: int, resuelto: bool):
    """Guarda el resultado de la partida en un CSV usando Pandas."""
    nueva_fila = {
        "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Jugador": jugador,
        "Dificultad": dificultad,
        "Tiempo (s)": tiempo_segundos,
        "Resuelto": "Sí" if resuelto else "No"
    }

    df_nuevo = pd.DataFrame([nueva_fila])

    if not os.path.exists(FILE_NAME):
        df_nuevo.to_csv(FILE_NAME, index=False)
    else:
        # Cargar existente y concatenar (Limpieza y transformación)
        df_existente = pd.read_csv(FILE_NAME)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
        df_final.to_csv(FILE_NAME, index=False)


def obtener_estadisticas():
    """Analiza datos con Pandas para mostrar en consola o interfaz."""
    if not os.path.exists(FILE_NAME):
        return "No hay datos aún."

    try:
        df = pd.read_csv(FILE_NAME)
        if df.empty or "Tiempo (s)" not in df.columns:
            return "No hay suficientes datos."

        # Análisis estadístico simple
        partidas_ganadas = df[df["Resuelto"] == "Sí"]
        if partidas_ganadas.empty:
            return "Aún no se ha ganado ninguna partida."

        promedio_tiempo = partidas_ganadas["Tiempo (s)"].mean()
        mejor_tiempo = partidas_ganadas["Tiempo (s)"].min()
        total_jugadas = len(df)

        return (f"Total Partidas: {total_jugadas}\n"
                f"Tiempo Promedio (Victorias): {promedio_tiempo:.2f}s\n"
                f"Mejor Tiempo: {mejor_tiempo}s")
    except Exception as e:
        return f"Error leyendo estadísticas: {e}"