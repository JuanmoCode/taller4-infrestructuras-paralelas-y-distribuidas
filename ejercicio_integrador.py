import threading
import time
import numpy as np

np.random.seed(42)

N = 10000                 
NUM_HILOS = 1000         
CHUNK = N // NUM_HILOS    
ITERACIONES = 10

# Matriz de 10000x10000 con enteros aleatorios entre 0 y 101 (como en el ejercicio 1), en un ndarray de NumPy
matriz = np.random.randint(0, 102, size=(N, N), dtype=np.int32)

# Versión secuencial
matriz_list = matriz.tolist()

def suma_secuencial(m):
    return sum(sum(fila) for fila in m)

# Versión paralela híbrida (SMP + SIMD):
# - SMP: un hilo por bloque de 1000x1000, sin locks, cada hilo escribe en su propia celda de resultados (ejercicio 1)
# - SIMD: dentro de cada hilo, NumPy suma las filas del bloque con instrucciones vectoriales (ejercicio 2)
def suma_paralela(CHUNK, NUM_HILOS, m):
    def tarea(hilo_id_i, hilo_id_j):
        bloque = m[NUM_HILOS*hilo_id_i:NUM_HILOS*(hilo_id_i+1), NUM_HILOS*hilo_id_j:NUM_HILOS*(hilo_id_j+1)]
        suma_filas = bloque.sum(axis=1, dtype=np.int64)       # suma de filas (SIMD)
        resultados[hilo_id_i][hilo_id_j] = int(suma_filas.sum())

    resultados = [[0 for _ in range(CHUNK)] for _ in range(CHUNK)]

    threads = [threading.Thread(target=tarea, args=(i, j)) for i in range(CHUNK) for j in range(CHUNK)]

    for i in threads:
        i.start()
    for i in threads:
        i.join()
    resultado_final = sum(sum(fila) for fila in resultados)
    return resultado_final

def main():
    tiempos_s = []
    tiempos_p = []
    for i in range(ITERACIONES):
        t0 = time.perf_counter(); rs = suma_secuencial(matriz_list); t1 = time.perf_counter()
        t2 = time.perf_counter(); rp = suma_paralela(CHUNK, NUM_HILOS, matriz); t3 = time.perf_counter()
        tiempos_s.append(t1 - t0)
        tiempos_p.append(t3 - t2)
        print("\n")
        print(f"Iteración {i+1}")
        print(f"Secuencial: {rs}  {t1-t0:.4f}s")
        print(f"Paralela  : {rp}  {t3-t2:.4f}s")
        print("Coinciden:", rs == rp)

    prom_s = sum(tiempos_s) / ITERACIONES
    prom_p = sum(tiempos_p) / ITERACIONES
    print("\n")
    print(f"Promedio secuencial: {prom_s:.4f}s")
    print(f"Promedio paralela  : {prom_p:.4f}s")
    print(f"La versión paralela fue {prom_s / prom_p:.1f} veces más rápida que la secuencial")

if __name__ == "__main__":
    main()