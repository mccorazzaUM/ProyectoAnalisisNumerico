from math import factorial


def calcular_paso(x, tolerancia=1e-9):
    if len(x) < 2:
        raise ValueError("Se necesitan al menos 2 puntos para interpolar.")

    h = x[1] - x[0]
    if abs(h) < tolerancia:
        raise ValueError(
            "Los valores de x no pueden repetirse."
        )

    for i in range(1, len(x)):
        paso_actual = x[i] - x[i - 1]
        if abs(paso_actual - h) > tolerancia:
            raise ValueError(
                "Los nodos no estan igualmente espaciados.\n"
            )
    return h


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


def construir_tabla_diferencias(y):
    n = len(y)
    tabla = [[0.0] * n for _ in range(n)]

    for i in range(n):
        tabla[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            tabla[i][j] = tabla[i + 1][j - 1] - tabla[i][j - 1]

    return tabla


def imprimir_tabla(x, tabla, nombre_x="x", nombre_y="y"):
    n = len(x)
    ancho = 12

    encabezado = f"{nombre_x:>{ancho}}{nombre_y:>{ancho}}"
    for j in range(1, n):
        encabezado += f"{'Δ^' + str(j) + 'y':>{ancho}}"
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(n):
        fila = f"{x[i]:>{ancho}.4f}{tabla[i][0]:>{ancho}.4f}"
        for j in range(1, n - i):
            fila += f"{tabla[i][j]:>{ancho}.4f}"
        print(fila)


def pedir_entero(mensaje, minimo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"El valor debe ser mayor o igual a {minimo}. Intenta de nuevo.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Debes ingresar un numero entero. Intenta de nuevo.")


def pedir_flotante(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada invalida. Debes ingresar un numero (ej: 3.5). Intenta de nuevo.")


def pedir_opcion(mensaje, opciones):
    opciones_norm = [o.lower() for o in opciones]
    while True:
        respuesta = input(mensaje).strip().lower()
        if respuesta in opciones_norm:
            return respuesta
        print(f"  -> Opcion invalida. Elegi una de estas: {', '.join(opciones)}. Intenta de nuevo.")


def cargar_datos_manual():
    n = pedir_entero("Cuantos puntos (x, y) vas a ingresar? (minimo 2): ", minimo=2)
    x, y = [], []
    for i in range(n):
        xi = pedir_flotante(f"  x[{i}] = ")
        if xi in x:
            print(f"  -> Aviso: el valor x={xi} ya fue ingresado. Los nodos no deben repetirse.")
            while xi in x:
                xi = pedir_flotante(f"  x[{i}] = (valor repetido, ingresa otro) ")
        yi = pedir_flotante(f"  y[{i}] = ")
        x.append(xi)
        y.append(yi)
    return x, y


def cargar_datos_ejemplo():
    x = [0, 5, 10, 15, 20]
    y = [95.0, 110.0, 140.0, 195.0, 280.0]
    print("\nDataset de ejemplo cargado (Monitoreo de un servidor web):")
    print("  Minuto de monitoreo -> Tiempo de respuesta promedio (ms)")
    for xi, yi in zip(x, y):
        print(f"    minuto {int(xi):>3} -> {yi:>6.1f} ms")
    return x, y


def main():
    print("\n" + "=" * 70)
    print(" INTERPOLACION DE NEWTON - DIFERENCIAS NO DIVIDIDAS")
    print(" Caso de aplicacion: Prediccion del tiempo de respuesta de un servidor")
    print("=" * 70)

    modo = pedir_opcion(
        "\nQuerés usar el dataset de ejemplo (monitoreo de servidor) o cargar "
        "datos propios?\n  [ejemplo/manual]: ",
        ["ejemplo", "manual"],
    )

    if modo == "ejemplo":
        x, y = cargar_datos_ejemplo()
    else:
        x, y = cargar_datos_manual()

    try:
        h = calcular_paso(x)
    except ValueError as e:
        print(f"\n[ERROR] No se puede continuar: {e}")
        return

    tabla = construir_tabla_diferencias(y)

    valor = pedir_flotante(
        "\nInstante de tiempo (minutos) a estimar/predecir: "
    )

    if valor < min(x) or valor > max(x):
        print(
            f"  -> Aviso: {valor} esta fuera del rango monitoreado "
            f"[{min(x)}, {max(x)}] minutos. El resultado sera una "
            "PREDICCION/extrapolacion, valida solo para el corto plazo "
            "inmediato posterior al ultimo dato."
        )

    metodo = pedir_opcion(
        "Metodo a utilizar [adelante=interpolar / atras=predecir a futuro]: ",
        ["adelante", "atras"],
    )

    try:
        if metodo == "adelante":
            resultado, s = newton_adelante(x, tabla, h, valor)
        else:
            resultado, s = newton_atras(x, tabla, h, valor)
    except OverflowError:
        print("\n[ERROR] El calculo produjo un desbordamiento numerico (valor "
              "demasiado grande). Revisa los datos ingresados.")
        return

    print(f"\nPaso h = {h}")
    imprimir_tabla(x, tabla, nombre_x="t(min)", nombre_y="t.resp(ms)")

    print(f"\nVariable s = {s:.6f}")
    print(f">>> P({valor}) ≈ {resultado:.6f}")
    if modo == "ejemplo":
        etiqueta = "prediccion" if valor > max(x) else "estimacion"
        print(f">>> Interpretacion: en el minuto {valor:.1f}, la {etiqueta} del")
        print(f"    tiempo de respuesta del servidor es {resultado:.2f} ms.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Programa interrumpido por el usuario. Saliendo...]")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] Ocurrio un problema no previsto: {e}")
        print("Por favor revisa los datos ingresados y volve a intentar.")
