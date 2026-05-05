from typing import List, Dict, Any
import numpy as np
import matplotlib.pyplot as plt


def evaluate_model_on_grid(result: Dict[str, Any], x_grid: np.ndarray) -> np.ndarray:
    
    name = result["name"]
    coeffs = result["coefficients"]

    if name == "Линейная":
        a0 = coeffs["a0"]
        a1 = coeffs["a1"]
        return a0 + a1 * x_grid

    if name == "Квадратичная":
        a0 = coeffs["a0"]
        a1 = coeffs["a1"]
        a2 = coeffs["a2"]
        return a0 + a1 * x_grid + a2 * x_grid ** 2

    if name == "Кубическая":
        a0 = coeffs["a0"]
        a1 = coeffs["a1"]
        a2 = coeffs["a2"]
        a3 = coeffs["a3"]
        return a0 + a1 * x_grid + a2 * x_grid ** 2 + a3 * x_grid ** 3

    if name == "Экспоненциальная":
        a = coeffs["a"]
        b = coeffs["b"]
        return a * np.exp(b * x_grid)

    if name == "Логарифмическая":
        a = coeffs["a"]
        b = coeffs["b"]
        y_grid = np.full_like(x_grid, np.nan, dtype=float)
        valid = x_grid > 0
        y_grid[valid] = a * np.log(x_grid[valid]) + b
        return y_grid

    if name == "Степенная":
        a = coeffs["a"]
        b = coeffs["b"]
        y_grid = np.full_like(x_grid, np.nan, dtype=float)
        valid = x_grid > 0
        y_grid[valid] = a * (x_grid[valid] ** b)
        return y_grid

    raise ValueError(f"Неизвестный тип модели: {name}")


def plot_results(x: List[float], y: List[float], results: List[Dict[str, Any]]) -> None:

    valid_results = [result for result in results if "error" not in result]

    if not valid_results:
        raise ValueError("Нет корректных моделей для построения графика")

    x_min = min(x)
    x_max = max(x)

    span = x_max - x_min
    if span == 0:
        span = 1.0

    margin = span * 0.1
    left = x_min - margin
    right = x_max + margin

    x_grid = np.linspace(left, right, 400)

    plt.figure(figsize=(10, 6))

    plt.scatter(x, y, label="Исходные точки", s=40)

    for result in valid_results:
        y_grid = evaluate_model_on_grid(result, x_grid)
        plt.plot(x_grid, y_grid, label=result["name"])

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Аппроксимация функции методом наименьших квадратов")
    plt.grid(True)
    plt.legend()
    plt.xlim(left, right)

    y_all = list(y)
    for result in valid_results:
        y_all.extend(result["y_pred"])

    y_min = min(y_all)
    y_max = max(y_all)
    y_span = y_max - y_min
    if y_span == 0:
        y_span = 1.0

    y_margin = y_span * 0.1
    plt.ylim(y_min - y_margin, y_max + y_margin)

    plt.tight_layout()
    plt.show()