import tkinter as tk
from tkinter import messagebox
import sudoku_logic
import sudoku_solver
import data_manager
import time


class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Funcional - UTP")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Iniciamos con un juego generado por Numpy
        # Borramos 40 números para una dificultad media
        self.tablero_actual = sudoku_logic.generar_partida_numpy(cantidad_a_borrar=40)

        self.celdas = {}
        self.start_time = time.time()

        self.crear_interfaz()
        self.actualizar_gui(self.tablero_actual)  # Llenar la vista con los números

    def crear_interfaz(self):
        # Título
        lbl_titulo = tk.Label(self.root, text="Sudoku Funcional", font=('Arial', 20, 'bold'))
        lbl_titulo.pack(pady=10)

        # Frame para el tablero
        frame_tablero = tk.Frame(self.root, bg="black", bd=2)
        frame_tablero.pack(pady=5)

        # Crear Grilla 9x9
        for r in range(9):
            for c in range(9):
                # Color diferenciado para subcuadrantes 3x3
                bg_color = "#ffffff"

                # Lógica para "pintar" el tablero como tablero de ajedrez por bloques de 3x3
                bloque_fila = r // 3
                bloque_col = c // 3
                if (bloque_fila + bloque_col) % 2 == 1:
                    bg_color = "#e0e0e0"

                e = tk.Entry(frame_tablero, width=2, font=('Arial', 18), justify='center', bg=bg_color, relief="flat")
                e.grid(row=r, column=c, padx=1, pady=1, ipady=5)  # ipady para hacer las celdas mas altas
                self.celdas[(r, c)] = e

        # Botonera
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=20)

        # Botones con diseño un poco más limpio
        # CORRECCIÓN AQUÍ: Quitamos el '#' de lightblue o usamos códigos hexadecimales válidos
        tk.Button(btn_frame, text="Nuevo Juego", command=self.nuevo_juego, bg="#dddddd").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Validar", command=self.validar_manual, bg="#dddddd").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Resolver", command=self.resolver_auto, bg="lightblue").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Stats", command=self.guardar_stats, bg="#dddddd").grid(row=0, column=3, padx=5)

    def obtener_tablero_de_gui(self):
        """Lee la GUI y crea una estructura de tablero (tupla)."""
        lista_temp = []
        for r in range(9):
            fila = []
            for c in range(9):
                val = self.celdas[(r, c)].get()
                if val.isdigit():
                    fila.append(int(val))
                else:
                    fila.append(0)
            lista_temp.append(tuple(fila))
        return tuple(lista_temp)

    def actualizar_gui(self, tablero):
        for r in range(9):
            for c in range(9):
                self.celdas[(r, c)].delete(0, tk.END)
                if tablero[r][c] != 0:
                    self.celdas[(r, c)].insert(0, str(tablero[r][c]))

    def validar_manual(self):
        # Capturamos el tablero actual de la GUI
        tablero_gui = self.obtener_tablero_de_gui()

        # Verificamos si es valido
        es_valido = True
        # Revisamos celda por celda (versión simplificada)
        for r in range(9):
            for c in range(9):
                num = tablero_gui[r][c]
                if num != 0:
                    # Truco: Quitamos el número temporalmente para validar si puede ir ahí
                    tablero_temp = list(list(f) for f in tablero_gui)
                    tablero_temp[r][c] = 0
                    tablero_temp = tuple(tuple(f) for f in tablero_temp)

                    if not sudoku_logic.es_movimiento_valido(tablero_temp, r, c, num):
                        es_valido = False
                        self.celdas[(r, c)].config(bg="#ffcccc")  # Marcar error en rojo
                    else:
                        # Restaurar color si estaba marcado
                        bloque_fila, bloque_col = r // 3, c // 3
                        bg = "#e0e0e0" if (bloque_fila + bloque_col) % 2 == 1 else "#ffffff"
                        self.celdas[(r, c)].config(bg=bg)

        if es_valido:
            messagebox.showinfo("Validación", "¡El tablero actual es válido!")
        else:
            messagebox.showwarning("Cuidado", "Hay errores en el tablero (marcados en rojo).")

    def resolver_auto(self):
        tablero_gui = self.obtener_tablero_de_gui()
        start = time.time()
        solucion = sudoku_solver.resolver_sudoku(tablero_gui)
        end = time.time()

        if solucion:
            self.actualizar_gui(solucion)
            tiempo = end - start
            messagebox.showinfo("Éxito", f"¡Resuelto en {tiempo:.4f} segundos!")
        else:
            messagebox.showerror("Error", "Este tablero no tiene solución.")

    def guardar_stats(self):
        tiempo_total = int(time.time() - self.start_time)
        data_manager.guardar_partida("Jugador 1", "Normal", tiempo_total, True)
        stats = data_manager.obtener_estadisticas()
        messagebox.showinfo("Estadísticas (Pandas)", stats)

    def nuevo_juego(self):
        """Genera un nuevo tablero aleatorio y reinicia el contador."""
        try:
            self.tablero_actual = sudoku_logic.generar_partida_numpy(40)
            self.actualizar_gui(self.tablero_actual)
            self.start_time = time.time()
            # Restaurar colores por si había errores marcados
            for r in range(9):
                for c in range(9):
                    bloque_fila, bloque_col = r // 3, c // 3
                    bg = "#e0e0e0" if (bloque_fila + bloque_col) % 2 == 1 else "#ffffff"
                    self.celdas[(r, c)].config(bg=bg)

            messagebox.showinfo("Nuevo Juego", "¡Tablero generado con Numpy!")
        except Exception as e:
            messagebox.showerror("Error", f"Error generando juego: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()