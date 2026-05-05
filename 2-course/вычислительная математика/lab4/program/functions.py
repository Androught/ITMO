import math
from typing import List, Dict, Any, Optional

from solver import least_squares_polynomial, evaluate_polynomial
from metrics import (
    calc_s,
    calc_delta,
    calc_r2,
    calc_pearson,
    calc_errors,
    get_r2_quality,
)


def build_result(
    name: str,
    formula: str,
    coefficients: Dict[str, float],
    x: List[float],
    y: List[float],
    y_pred: List[float],
    pearson: Optional[float] = None,
) -> Dict[str, Any]:
    
    eps = calc_errors(y, y_pred)
    s = calc_s(y, y_pred)
    delta = calc_delta(y, y_pred)
    r2 = calc_r2(y, y_pred)

    return {
        "name": name,
        "formula": formula,
        "coefficients": coefficients,
        "x": x,
        "y": y,
        "y_pred": y_pred,
        "eps": eps,
        "S": s,
        "delta": delta,
        "R2": r2,
        "R2_quality": get_r2_quality(r2),
        "pearson": pearson,
    }


def fit_linear(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    coeffs = least_squares_polynomial(x, y, 1)
    y_pred = evaluate_polynomial(coeffs, x)
    pearson = calc_pearson(x, y)

    a0, a1 = coeffs
    formula = f"y = {a0:.6f} + {a1:.6f} * x"

    return build_result(
        name="Линейная",
        formula=formula,
        coefficients={"a0": a0, "a1": a1},
        x=x,
        y=y,
        y_pred=y_pred,
        pearson=pearson,
    )


def fit_quadratic(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    coeffs = least_squares_polynomial(x, y, 2)
    y_pred = evaluate_polynomial(coeffs, x)

    a0, a1, a2 = coeffs
    formula = f"y = {a0:.6f} + {a1:.6f} * x + {a2:.6f} * x^2"

    return build_result(
        name="Квадратичная",
        formula=formula,
        coefficients={"a0": a0, "a1": a1, "a2": a2},
        x=x,
        y=y,
        y_pred=y_pred,
    )


def fit_cubic(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    coeffs = least_squares_polynomial(x, y, 3)
    y_pred = evaluate_polynomial(coeffs, x)

    a0, a1, a2, a3 = coeffs
    formula = f"y = {a0:.6f} + {a1:.6f} * x + {a2:.6f} * x^2 + {a3:.6f} * x^3"

    return build_result(
        name="Кубическая",
        formula=formula,
        coefficients={"a0": a0, "a1": a1, "a2": a2, "a3": a3},
        x=x,
        y=y,
        y_pred=y_pred,
    )


def fit_exponential(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    if any(yi <= 0 for yi in y):
        raise ValueError("Экспоненциальная аппроксимация невозможна: все y должны быть > 0")

    ln_y = [math.log(yi) for yi in y]

    coeffs = least_squares_polynomial(x, ln_y, 1)
    a0, a1 = coeffs

    a = math.exp(a0)
    b = a1

    y_pred = [a * math.exp(b * xi) for xi in x]
    formula = f"y = {a:.6f} * e^({b:.6f} * x)"

    return build_result(
        name="Экспоненциальная",
        formula=formula,
        coefficients={"a": a, "b": b},
        x=x,
        y=y,
        y_pred=y_pred,
    )


def fit_logarithmic(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    if any(xi <= 0 for xi in x):
        raise ValueError("Логарифмическая аппроксимация невозможна: все x должны быть > 0")

    ln_x = [math.log(xi) for xi in x]
    coeffs = least_squares_polynomial(ln_x, y, 1)

    b, a = coeffs
    y_pred = [a * math.log(xi) + b for xi in x]
    formula = f"y = {a:.6f} * ln(x) + {b:.6f}"

    return build_result(
        name="Логарифмическая",
        formula=formula,
        coefficients={"a": a, "b": b},
        x=x,
        y=y,
        y_pred=y_pred,
    )


def fit_power(x: List[float], y: List[float]) -> Dict[str, Any]:
    
    if any(xi <= 0 for xi in x):
        raise ValueError("Степенная аппроксимация невозможна: все x должны быть > 0")
    if any(yi <= 0 for yi in y):
        raise ValueError("Степенная аппроксимация невозможна: все y должны быть > 0")

    ln_x = [math.log(xi) for xi in x]
    ln_y = [math.log(yi) for yi in y]

    coeffs = least_squares_polynomial(ln_x, ln_y, 1)
    a0, a1 = coeffs

    a = math.exp(a0)
    b = a1

    y_pred = [a * (xi ** b) for xi in x]
    formula = f"y = {a:.6f} * x^({b:.6f})"

    return build_result(
        name="Степенная",
        formula=formula,
        coefficients={"a": a, "b": b},
        x=x,
        y=y,
        y_pred=y_pred,
    )


def fit_all_models(x: List[float], y: List[float]) -> List[Dict[str, Any]]:
    
    fit_functions = [
        fit_linear,
        fit_quadratic,
        fit_cubic,
        fit_exponential,
        fit_logarithmic,
        fit_power,
    ]

    results = []

    for fit_func in fit_functions:
        try:
            result = fit_func(x, y)
            results.append(result)
        except ValueError as e:
            results.append({
                "name": fit_func.__name__,
                "error": str(e),
            })

    return results


def get_best_model(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    valid_results = [result for result in results if "delta" in result]

    if not valid_results:
        raise ValueError("Нет ни одной корректно построенной модели")

    return min(valid_results, key=lambda result: result["delta"])