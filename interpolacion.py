from math import factorial

# FUNCIONES IMPORTANTES

def diferenciasAdelante(x, tabla, h, valor):
    n = len(x)
    s = (valor - x[0]) / h

    resultado = tabla[0][0]
    producto = 1.0

    for j in range (1,n):
        producto *= (s - (j - 1))
        termino = producto * tabla[0][j] / factorial(j)
        resultado += termino

    return resultado, s

# FUNCIÓN PARA INTERACTUAR CON EL USUARIO

def leer_datos():
    n = int(input('Cuantos puntos (x,y) va a ingresar?'))
    x, y = [], []
    for i in range(n):
        xi = float(input(f'x[{i}] = '))
        yi = float(input(f'y[{i}] = '))
        x.append(xi)
        y.append(yi)
    valor = float(input('Valor de x a interpolar: '))
    return x, y, valor