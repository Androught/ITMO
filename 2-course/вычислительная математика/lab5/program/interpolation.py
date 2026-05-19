from math import factorial

from differences import (
    build_finite_differences,
    build_divided_differences,
    get_step,
)


def lagrange_interpolation(x_values, y_values, x):
    
    n = len(x_values)
    result = 0.0

    for i in range(n):
        basis_polynomial = 1.0

        for j in range(n):
            if i != j:
                numerator = x - x_values[j]
                denominator = x_values[i] - x_values[j]
                basis_polynomial *= numerator / denominator

        result += y_values[i] * basis_polynomial

    return result


def newton_divided_forward(x_values, y_values, x):

    table = build_divided_differences(x_values, y_values)
    n = len(x_values)

    result = table[0][0]
    product = 1.0

    for k in range(1, n):
        product *= x - x_values[k - 1]
        result += table[0][k] * product

    return result


def newton_divided_backward(x_values, y_values, x):

    table = build_divided_differences(x_values, y_values)
    n = len(x_values)

    result = table[n - 1][0]
    product = 1.0

    for k in range(1, n):
        product *= x - x_values[n - k]
        result += table[n - k - 1][k] * product

    return result


def newton_finite_forward(x_values, y_values, x):

    table = build_finite_differences(y_values)
    h = get_step(x_values)
    n = len(x_values)

    t = (x - x_values[0]) / h

    result = table[0][0]
    product = 1.0

    for k in range(1, n):
        product *= t - (k - 1)
        result += product * table[0][k] / factorial(k)

    return result


def newton_finite_backward(x_values, y_values, x):

    table = build_finite_differences(y_values)
    h = get_step(x_values)
    n = len(x_values)

    t = (x - x_values[n - 1]) / h

    result = table[n - 1][0]
    product = 1.0

    for k in range(1, n):
        product *= t + (k - 1)
        result += product * table[n - k - 1][k] / factorial(k)

    return result

def is_closer_to_start(x_values, x):
    start = x_values[0]
    end = x_values[-1]

    return abs(x - start) <= abs(x - end)


def newton_divided_auto(x_values, y_values, x):

    if is_closer_to_start(x_values, x):
        return newton_divided_forward(x_values, y_values, x)

    return newton_divided_backward(x_values, y_values, x)


def newton_finite_auto(x_values, y_values, x):

    if is_closer_to_start(x_values, x):
        return newton_finite_forward(x_values, y_values, x)

    return newton_finite_backward(x_values, y_values, x)

def interpolate_all_methods(x_values, y_values, x):

    return {
        "Лагранж": lagrange_interpolation(x_values, y_values, x),
        "Ньютон с разделёнными разностями, вперёд":
            newton_divided_forward(x_values, y_values, x),
        "Ньютон с разделёнными разностями, назад":
            newton_divided_backward(x_values, y_values, x),
        "Ньютон с конечными разностями, вперёд":
            newton_finite_forward(x_values, y_values, x),
        "Ньютон с конечными разностями, назад":
            newton_finite_backward(x_values, y_values, x),
    }