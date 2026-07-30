<div align=center>

# Interpolación de Newton con Diferencias No Divididas
### María Cecilia Corazza, Melina Navarro
---

</div>

## Concepto de interpolación
Dado un conjunto de puntos de una función

$$ (x_0, y_0), (x_1, y_1), \dots\, (x_n, y_n)$$

la interpolación es un procedimiento de aproximación de un conjunto de $$n$$ puntos con un polinomio de grado $$n-1$$. Ese polinomio cumple con la condición de que es único y debe pasar exactamente por todos los puntos dados.

## Conceptos matemáticos
### Fórmula de Newton Diferencias hacia adelante

$$ P(x) = \frac{1}{h} \left[ \Delta f(x_0) - \frac{1}{2}\Delta^2 f(x_0) + \frac{1}{3}\Delta^3 f(x_0) - \dots \right] $$
