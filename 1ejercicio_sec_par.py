import random
import threading
import time



random.seed(42)




def suma_secuencial(m):
    return sum(sum(fila) for fila in m)

#solucion paralela sin usar locks, usando hilos y dividiendo la matriz en 100 partes iguales, cada hilo suma una parte de la matriz 
# y luego se suman los resultados parciales para obtener el resultado final
def suma_paralela( CHUNK, NUM_HILOS,m):
    def tarea(hilo_id_i,hilo_id_j):
        suma = 0
        for i in range(NUM_HILOS*hilo_id_i, NUM_HILOS*(hilo_id_i+1)):
            for j in range(NUM_HILOS*hilo_id_j, NUM_HILOS*(hilo_id_j+1)):
                suma += m[i][j]
        resultados[hilo_id_i][hilo_id_j] = suma



    resultados = [[0 for _ in range(CHUNK )] for _ in range(CHUNK )]



    threads = [threading.Thread(target=tarea, args=(i, j)) for i in range(CHUNK) for j in range(CHUNK)]


    for i in threads:
        i.start()
    for i in threads:
        i.join()
    resultado_final = sum(sum(fila) for fila in resultados)
    print(f"Resultado final: {resultado_final}")
    return resultado_final

def main():
    for i in range(0,5):
        NUM_HILOS = 100
        N= 1000
        CHUNK = N // NUM_HILOS
        m = [[round(random.randint(0, 101)) for _ in range(N)] for _ in range(N)]
        t0 = time.perf_counter(); rs = suma_secuencial(m); t1 = time.perf_counter()
        t2 = time.perf_counter(); rp = suma_paralela(CHUNK,NUM_HILOS,m);  t3 = time.perf_counter()
        print("\n")
        print(f"Iteración {i+1}")
        print(f"Secuencial: {rs}  {t1-t0:.4f}s")
        print(f"Paralela  : {rp}  {t3-t2:.4f}s")
        print("Coinciden:", rs == rp)

if __name__ == "__main__":
    main()


