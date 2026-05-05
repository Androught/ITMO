from typing import List
import numpy as np


def solve_linear_system(a: List[List[float]], b: List[float]) -> List[float]:
    
    a_np = np.array(a, dtype=float)
    b_np = np.array(b, dtype=float)

    if a_np.shape[0] != a_np.shape[1]:
        raise ValueError("Матрица A должна быть квадратной")

    if a_np.shape[0] != b_np.shape[0]:
        raise ValueError("Размеры A и b не согласованы")

    try:
        solution = np.linalg.solve(a_np, b_np)
    except np.linalg.LinAlgError as e:
        raise ValueError(f"Не удалось решить систему: {e}")

    return solution.tolist()


def least_squares_polynomial(x: List[float], y: List[float], degree: int) -> List[float]:
    
    if len(x) != len(y):
        raise ValueError("Длины x и y должны совпадать")
    if len(x) == 0:
        raise ValueError("Списки x и y не должны быть пустыми")
    if degree < 1:
        raise ValueError("Степень полинома должна быть >= 1")
    if len(x) <= degree:
        raise ValueError("Количество точек должно быть больше степени полинома")

    n = len(x)
    m = degree

    
    matrix = []
    for row in range(m + 1):
        matrix_row = []
        for col in range(m + 1):
            value = sum((x_i ** (row + col)) for x_i in x)
            matrix_row.append(value)
        matrix.append(matrix_row)

    
    rhs = []
    for row in range(m + 1):
        value = sum((x[i] ** row) * y[i] for i in range(n))
        rhs.append(value)

    return solve_linear_system(matrix, rhs)


def evaluate_polynomial(coefficients: List[float], x_values: List[float]) -> List[float]:
    
    result = []

    for x in x_values:
        y = 0.0
        for power, coef in enumerate(coefficients):
            y += coef * (x ** power)
        result.append(y)

    return result