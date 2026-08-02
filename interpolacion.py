from math import factorial

# DIFERENCIAS HACIA ADELANTE
def newton_adelante(x, tabla, h, valor):
    n = len(x)
    s = (valor - x[0]) / h

    resultado = tabla[0][0]      # primer termino: y0
    producto = 1.0               # ira acumulando s(s-1)(s-2)...

    for j in range(1, n):
        producto *= (s - (j - 1))                  # factor nuevo
        termino = producto * tabla[0][j] / factorial(j)
        resultado += termino

    return resultado, s

# DIFERENCIAS HACIA ATRAS
def newton_atras(x, tabla, h, valor):
    n = len(x)
    s = (valor - x[-1]) / h

    resultado = tabla[n - 1][0]  # primer termino: yn
    producto = 1.0

    for j in range(1, n):
        producto *= (s + (j - 1))                  # factor nuevo
        termino = producto * tabla[n - 1 - j][j] / factorial(j)
        resultado += termino

    return resultado, s

# CALCULO PASO H
def calcular_paso(x, tolerancia=1e-9):
    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos.")

    h = x[1] - x[0]
    for i in range(1, len(x)):
        paso_actual = x[i] - x[i - 1]
        if abs(paso_actual - h) > tolerancia:
            raise ValueError(
                "Los nodos NO estan igualmente espaciados. "
                "Use el metodo de diferencias DIVIDIDAS en su lugar.\n"
                f"  Se esperaba h = {h}, pero entre x[{i-1}] y x[{i}] "
                f"el paso es {paso_actual}."
            )
    return h


def construir_tabla_diferencias(y):
    n = len(y)
    tabla = [[0.0] * n for _ in range(n)]

    # Primera columna = valores originales
    for i in range(n):
        tabla[i][0] = y[i]

    # Diferencias de orden creciente
    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = tabla[i + 1][j - 1] - tabla[i][j - 1]

    return tabla

def imprimir_tabla(x, tabla):
    n = len(x)
    ancho = 12

    # Encabezado
    encabezado = f"{'x':>{ancho}}{'y':>{ancho}}"
    for j in range(1, n):
        encabezado += f"{'Δ^' + str(j) + 'y':>{ancho}}"
    print(encabezado)
    print("-" * len(encabezado))

    # Filas
    for i in range(n):
        fila = f"{x[i]:>{ancho}.4f}{tabla[i][0]:>{ancho}.4f}"
        for j in range(1, n - i):
            fila += f"{tabla[i][j]:>{ancho}.4f}"
        print(fila)

# PROGRAMA PRINCIPAL
if __name__ == "__main__":
    n = int(input("¿Cuantos puntos (x, y) va a ingresar? "))
    x, y = [], []
    for i in range(n):
        x.append(float(input(f"  x[{i}] = ")))
        y.append(float(input(f"  y[{i}] = ")))
    valor = float(input("Valor de x a interpolar: "))

    print("=" * 60)
    print(" INTERPOLACIÓN DE NEWTON - DIFERENCIAS FINITAS")
    print("=" * 60)

    print("\nDatos ingresados:")
    for xi, yi in zip(x, y):
        print(f"   x = {xi:<10} y = {yi}")

    # 1) Validar espaciamiento y obtener el paso h
    h = calcular_paso(x)
    print(f"\nPaso h = {h}")

    # 2) Construir y mostrar la tabla de diferencias
    tabla = construir_tabla_diferencias(y)
    print("\nTabla de diferencias finitas:\n")
    imprimir_tabla(x, tabla)

    # 3) Elegir el metodo segun la posicion del valor:
    #    primera mitad -> adelante ; segunda mitad -> atras
    punto_medio = (x[0] + x[-1]) / 2
    if valor <= punto_medio:
        resultado, s = newton_adelante(x, tabla, h, valor)
        metodo = "ADELANTE"
    else:
        resultado, s = newton_atras(x, tabla, h, valor)
        metodo = "ATRAS"

    # 4) Mostrar el resultado
    print(f"\nMetodo utilizado: Newton hacia {metodo}")
    print(f"Variable s = {s:.6f}")
    print(f"\n>>> P({valor}) ≈ {resultado:.6f}")
    print("=" * 60)