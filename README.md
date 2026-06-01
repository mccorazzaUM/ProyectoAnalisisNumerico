<div align=center>

# Interpolación de Newton con Diferencias No Divididas
### María Cecilia Corazza, Navarro Melina
---

</div>

## Concepto de interpolación
Dado un conjunto de puntos de una función

$$ (x_0, y_0), (x_1, y_1), \dots\, (x_n, y_n)$$

la interpolación busca un polinomio P(x) que pase exactamente por todos esos puntos, para poder estimar el valor de la función en un punto intermedio donde no tenemos ese dato.

## Conceptos matemáticos
### Diferencias hacia adelante
$$ \Delta\ y_1 = y_{i+1} - y_i\ \text{(orden 1)} $$
$$ \Delta\ y_1 = \Delta\ y_{i+1} - \Delta\ y_i\ \text{(orden 2)} $$
$$ \text{fórmula general:} $$
$$ \Delta^k y_i = \Delta^{k-1} y_{i+1} - \Delta^{k-1} y_i\ \text{(orden k)} $$

