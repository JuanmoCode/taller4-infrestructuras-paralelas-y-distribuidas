import time
import numpy as np

N = 1000
# Matrices de 1000x1000 con flotantes aleatorios, usando ndarray de NumPy
matrizA = np.random.rand(N, N)
matrizB = np.random.rand(N, N)

def numpy_multiply(A, B):
    # Verifica que las dimensiones sean compatibles para la multiplicación
    if A.shape[1] != B.shape[0]:
        raise ValueError("Las matrices no se pueden multiplicar debido a dimensiones incompatibles.")
    # Realiza la multiplicación de matrices usando NumPy
    resultado = A @ B
    return resultado

def matrix_multiply(A, B):
    # Verifica que las dimensiones sean compatibles para la multiplicación
    if len(A[0]) != len(B):
        raise ValueError("Las matrices no se pueden multiplicar debido a dimensiones incompatibles.")
    # Inicializa la matriz resultado con ceros
    resultado = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    # Realiza la multiplicación de matrices
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                resultado[i][j] += A[i][k] * B[k][j]
    return resultado

#Version numpy
inicio = time.perf_counter()
C_numpy = numpy_multiply(matrizA, matrizB)
fin = time.perf_counter()
t_numpy = fin - inicio
print(f"NumPy:  {t_numpy:.6f} segundos")

#Version secuencial
# Convertimos las matrices de NumPy a listas para la versión secuencial
matrizA_list = matrizA.tolist()
matrizB_list = matrizB.tolist()

inicio = time.perf_counter()
C_secuencial = matrix_multiply(matrizA_list, matrizB_list)
fin = time.perf_counter()
t_secuencial = fin - inicio
print(f"Secuencial:  {t_secuencial:.6f} segundos")

# --- Comparación ---
print(f"\nNumPy fue {t_secuencial / t_numpy:.1f} veces más rápido que el bucle tradicional")
print("¿Resultados iguales?", np.allclose(C_numpy, np.array(C_secuencial)))