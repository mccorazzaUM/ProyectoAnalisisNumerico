from math import factorial
import os

# matplotlib es opcional: si no esta instalado, el programa sigue funcionando
# sin la parte grafica y avisa como instalarlo.
try:
    import matplotlib
    matplotlib.use("Agg")  # backend sin ventana, para poder exportar el PNG
    import matplotlib.pyplot as plt
    HAY_MATPLOTLIB = True
except ImportError:
    HAY_MATPLOTLIB = False


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
        encabezado += f"{'d^' + str(j) + 'y':>{ancho}}"
    print(encabezado)
    print("-" * len(encabezado))

    for i in range(n):
        fila = f"{x[i]:>{ancho}.4f}{tabla[i][0]:>{ancho}.4f}"
        for j in range(1, n - i):
            fila += f"{tabla[i][j]:>{ancho}.4f}"
        print(fila)


def evaluar_polinomio(x, tabla, h, valor, metodo="adelante"):
    if metodo == "adelante":
        resultado, _ = newton_adelante(x, tabla, h, valor)
    else:
        resultado, _ = newton_atras(x, tabla, h, valor)
    return resultado


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


def cargar_datos_archivo(ruta):
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontro el archivo: {ruta}")

    x, y = [], []
    with open(ruta, "r", encoding="utf-8") as f:
        for numero_linea, linea in enumerate(f, start=1):
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue

            # Permite coma, punto y coma, tabulacion o espacios como separador
            for separador in [",", ";", "\t"]:
                if separador in linea:
                    partes = linea.split(separador)
                    break
            else:
                partes = linea.split()

            partes = [p.strip() for p in partes if p.strip() != ""]
            if len(partes) < 2:
                raise ValueError(
                    f"Linea {numero_linea}: se esperaban 2 columnas (x, y) y se encontro: '{linea}'"
                )

            try:
                xi = float(partes[0])
                yi = float(partes[1])
            except ValueError:
                # si es la fila de encabezado se ignora :)
                if numero_linea == 1 or not x:
                    continue
                raise ValueError(
                    f"Linea {numero_linea}: no se pudieron convertir a numero los valores '{partes[0]}' y '{partes[1]}'."
                )

            if xi in x:
                raise ValueError(
                    f"Linea {numero_linea}: el valor x={xi} esta repetido. Los nodos no deben repetirse."
                )
            x.append(xi)
            y.append(yi)

    if len(x) < 2:
        raise ValueError("El archivo debe contener al menos 2 puntos (x, y) validos.")

    print(f"\nSe leyeron {len(x)} puntos desde '{ruta}'.")
    return x, y


def cargar_datos_ejemplo():
    x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    y = [95.0, 108.0, 124.0, 145.0, 172.0, 205.0, 246.0, 295.0, 355.0, 428.0]
    print("\nDataset de ejemplo cargado (Monitoreo de un servidor web bajo prueba de carga):")
    print("  Minuto de monitoreo -> Tiempo de respuesta promedio (ms)")
    for xi, yi in zip(x, y):
        print(f"    minuto {int(xi):>3} -> {yi:>7.1f} ms")
    return x, y

# FUNCION PARA GRAFICAR
def graficar(x, y, tabla, h, metodo, valor=None, resultado=None,
             ruta_png="grafico_interpolacion.png"):
    if not HAY_MATPLOTLIB:
        print("\n[Aviso] matplotlib no esta instalado; se omite el grafico.")
        print("        Para habilitarlo: pip install matplotlib")
        return None

    # Muestreo fino del polinomio. Si el valor estimado cae fuera del rango
    # de los nodos, se extiende el intervalo para que la curva llegue hasta el.
    n_muestras = 400
    x_min, x_max = min(x), max(x)
    if valor is not None:
        x_min = min(x_min, valor)
        x_max = max(x_max, valor)
    paso = (x_max - x_min) / (n_muestras - 1)
    xs = [x_min + i * paso for i in range(n_muestras)]
    ys = [evaluar_polinomio(x, tabla, h, xv, metodo) for xv in xs]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(xs, ys, color="#1f77b4", linewidth=2,
            label="Polinomio aproximante P(x)")
    ax.scatter(x, y, color="#d62728", zorder=5, s=45,
               label="Puntos medidos")

    if valor is not None and resultado is not None:
        ax.scatter([valor], [resultado], color="#2ca02c", zorder=6, s=90,
                   marker="X", label=f"Estimacion P({valor:g}) = {resultado:.2f}")
        ax.annotate(f"({valor:g}, {resultado:.2f})",
                    xy=(valor, resultado),
                    xytext=(8, 8), textcoords="offset points", fontsize=9)

    ax.set_title("Interpolacion de Newton - Monitoreo de servidor web")
    ax.set_xlabel("Minuto de monitoreo")
    ax.set_ylabel("Tiempo de respuesta (ms)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ruta_png, dpi=150)
    plt.close(fig)

    print(f"\nGrafico exportado a: {ruta_png}")
    return ruta_png


def main():
    print("\n" + "=" * 70)
    print(" INTERPOLACION DE NEWTON - DIFERENCIAS NO DIVIDIDAS")
    print("=" * 70)

    modo = pedir_opcion(
        "\nDe donde tomamos los datos?\n  [ejemplo/manual/archivo]: ",
        ["ejemplo", "manual", "archivo"],
    )

    if modo == "ejemplo":
        x, y = cargar_datos_ejemplo()  # EJEMPLO: MONITOREO DE SERVIDOR WEB
    elif modo == "archivo":
        while True:
            ruta = input("Ruta del archivo (.csv o .txt): ").strip()
            try:
                x, y = cargar_datos_archivo(ruta)
                break
            except (FileNotFoundError, ValueError) as e:
                print(f"  -> {e}")
                if pedir_opcion("Intentar con otro archivo? [si/no]: ", ["si", "no"]) == "no":
                    print("Operacion cancelada.")
                    return
    else:
        x, y = cargar_datos_manual()

    try:
        h = calcular_paso(x)
    except ValueError as e:
        print(f"\n[ERROR] No se puede continuar: {e}")
        return

    tabla = construir_tabla_diferencias(y)

    valor = pedir_flotante(
        "\nMinuto a estimar/predecir: "
    )

    if valor < min(x) or valor > max(x):
        print(
            f"  -> Aviso: {valor} esta fuera del rango monitoreado "
            f"[{min(x)}, {max(x)}] minutos (esto es una extrapolacion)."
        )

    metodo = pedir_opcion(
        "Metodo a utilizar [adelante/atras]: ",
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
    imprimir_tabla(x, tabla, nombre_x="minuto", nombre_y="ms")

    print(f"\nVariable s = {s:.6f}")
    print(f"P({valor}) ~= {resultado:.6f}")
    if modo == "ejemplo":
        situacion = "prediccion" if valor > max(x) else "estimacion"
        print(f"Interpretacion: en el minuto {valor:.1f}, la {situacion} del tiempo "
              f"de respuesta del servidor es de {resultado:.2f} ms.")

    # Grafico y exportacion a PNG
    graficar(x, y, tabla, h, metodo, valor, resultado)

    print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Programa interrumpido por el usuario. Saliendo...]")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] Ocurrio un problema no previsto: {e}")
        print("Por favor revisa los datos ingresados y volve a intentar.")
