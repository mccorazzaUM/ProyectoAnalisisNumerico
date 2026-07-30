<div align=center>

# Interpolación de Newton con Diferencias No Divididas
### María Cecilia Corazza, Melina Navarro
---

</div>

## Concepto de interpolación
Dado un conjunto de puntos de una función

$$ (x_0, y_0), (x_1, y_1), \dots\, (x_n, y_n)$$

la interpolación es un procedimiento de aproximación de un conjunto de $$n$$ puntos con un polinomio de grado $$n-1$$, ese polinomio cumple con la condición de que es único y debe pasar exactamente por todos los puntos dados.

## Conceptos matemáticos
### Diferencias hacia adelante

$$\Delta y_i = y_{i+1} - y_i \quad\text{(orden 1)}$$
$$\Delta^2 y_i = \Delta y_{i+1} - \Delta y_i \quad\text{(orden 2)}$$
$$\Delta^k y_i = \Delta^{k-1} y_{i+1} - \Delta^{k-1} y_i \quad\text{(orden } k\text{)}$$

Para simplificar la fórmula se hace un cambio de variable que mide a cuántos pasos h está el punto buscado respecto del nodo de referencia:

- Hacia adelante (referencia $x_0$): $\quad s = \dfrac{x - x_0}{h}$
- Hacia atrás (referencia $x_n$): $\quad s = \dfrac{x - x_n}{h}$

### Fórmula de Newton hacia adelante

$$P(x) = y_0 + s\,\Delta y_0 + \frac{s(s-1)}{2!}\,\Delta^2 y_0 + \frac{s(s-1)(s-2)}{3!}\,\Delta^3 y_0 + \dots$$

### Fórmula de Newton hacia ATRÁS

$$P(x) = y_n + s\,\nabla y_n + \frac{s(s+1)}{2!}\,\nabla^2 y_n + \frac{s(s+1)(s+2)}{3!}\,\nabla^3 y_n + \dots$$
