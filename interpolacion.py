from math import factorial

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


if __name__ == "__main__":
  # todavia no terminamos aaa
