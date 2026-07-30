from math import factorial

# CALCULAR PASO (H)
def calcular_paso(x, tolerancia=1e-9):
    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos.")

    h = x[1] - x[0]
    for i in range(1, len(x)):
        paso_actual = x[i] - x[i - 1]
        if abs(paso_actual - h) > tolerancia:
            raise ValueError("Los nodos no estan igualmente espaciados.")
    return h

# DIFERENCIAS HACIA ADELANTE
def newton_adelante(x, tabla, h, valor):
    n = len(x)
    s = (valor - x[0]) / h

    resultado = tabla[0][0]
    producto = 1.0

    for j in range(1, n):
        producto *= (s - (j - 1))
        termino = producto * tabla[0][j] / factorial(j)
        resultado += termino

    return resultado, s

# DIFERENCIAS HACIA ATRAS
def newton_atras(x, tabla, h, valor):
    n = len(x)
    s = (valor - x[-1]) / h

    resultado = tabla[n - 1][0]
    producto = 1.0

    for j in range(1, n):
        producto *= (s + (j - 1)) 
        termino = producto * tabla[n - 1 - j][j] / factorial(j)
        resultado += termino

    return resultado, s

# FUNCIONES PARA CONSTRUIR LA TABLA
def construir_tabla_diferencias(y):
    n = len(y)
    tabla = [[0.0] * n for _ in range(n)]

    for i in range(n):
        tabla[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = tabla[i + 1][j - 1] - tabla[i][j - 1]

    return tabla

def imprimir_tabla(x, tabla):
    n = len(x)
    ancho = 12

    encabezado = f"{'x':>{ancho}}{'y':>{ancho}}"
    for j in range(1, n):
        encabezado += f"{'Δ^' + str(j) + 'y':>{ancho}}"
    print(encabezado)
    print("-" * len(encabezado))
    
    for i in range(n):
        fila = f"{x[i]:>{ancho}.4f}{tabla[i][0]:>{ancho}.4f}"
        for j in range(1, n - i):
            fila += f"{tabla[i][j]:>{ancho}.4f}"
        print(fila)

# FUNCION PRINCIPAL

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(" INTERPOLACIÓN DE NEWTON - DIFERENCIAS NO DIVIDIDAS")
    print("=" * 60)
    
    n = int(input("Cuantos puntos (x, y) vas a ingresar? "))
    x, y = [], []
    for i in range(n):
        xi = float(input(f"  x[{i}] = "))
        yi = float(input(f"  y[{i}] = "))
        x.append(xi)
        y.append(yi)
    valor = float(input("Valor de x a interpolar: "))
    h = calcular_paso(x)
    tabla = construir_tabla_diferencias(y)

    if metodo == "adelante":
        resultado, s = newton_adelante(x, tabla, h, valor)
    elif metodo == "atras":
        resultado, s = newton_atras(x, tabla, h, valor)
    else:
        raise ValueError("metodo debe ser 'adelante' o 'atras'.")

    print(f"\nPaso h = {h}")
    imprimir_tabla(x, tabla)

    print(f"Variable s = {s:.6f}")
    print(f"\n>>> P({valor}) ≈ {resultado:.6f}")
    print("=" * 60 + "\n")
