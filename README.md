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
$$ \Delta\ y_1 = y_{i+1} - y_i\ \text{(orden 1)} $$
$$ \Delta\ y_1 = \Delta\ y_{i+1} - \Delta\ y_i\ \text{(orden 2)} $$
$$ \text{fórmula general:} $$
$$ \Delta^k y_i = \Delta^{k-1} y_{i+1} - \Delta^{k-1} y_i\ \text{(orden k)} $$

## Funciones

## Estructura del proyecto
