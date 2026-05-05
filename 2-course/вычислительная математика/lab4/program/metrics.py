import math
from typing import List


def calc_s(y_true: List[float], y_pred: List[float]) -> float:

    if len(y_true) != len(y_pred):
        raise ValueError("Длины y_true и y_pred должны совпадать")

    s = 0.0
    for yt, yp in zip(y_true, y_pred):
        s += (yp - yt) ** 2
    return s


def calc_delta(y_true: List[float], y_pred: List[float]) -> float:
    
    if len(y_true) == 0:
        raise ValueError("Списки не должны быть пустыми")

    s = calc_s(y_true, y_pred)
    return math.sqrt(s / len(y_true))


def calc_r2(y_true: List[float], y_pred: List[float]) -> float:
    
    if len(y_true) != len(y_pred):
        raise ValueError("Длины y_true и y_pred должны совпадать")
    if len(y_true) == 0:
        raise ValueError("Списки не должны быть пустыми")

    y_mean = sum(y_true) / len(y_true)

    ss_res = 0.0
    ss_tot = 0.0

    for yt, yp in zip(y_true, y_pred):
        ss_res += (yt - yp) ** 2
        ss_tot += (yt - y_mean) ** 2

    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0

    return 1.0 - ss_res / ss_tot


def calc_pearson(x: List[float], y: List[float]) -> float:
    
    if len(x) != len(y):
        raise ValueError("Длины x и y должны совпадать")
    if len(x) == 0:
        raise ValueError("Списки не должны быть пустыми")

    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)

    numerator = 0.0
    sum_x = 0.0
    sum_y = 0.0

    for xi, yi in zip(x, y):
        dx = xi - x_mean
        dy = yi - y_mean
        numerator += dx * dy
        sum_x += dx ** 2
        sum_y += dy ** 2

    denominator = math.sqrt(sum_x * sum_y)

    if denominator == 0:
        raise ValueError("Невозможно вычислить коэффициент Пирсона: знаменатель равен нулю")

    return numerator / denominator


def get_r2_quality(r2: float) -> str:
    
    if r2 >= 0.95:
        return "Высокая точность аппроксимации"
    if r2 >= 0.75:
        return "Удовлетворительная аппроксимация"
    if r2 >= 0.5:
        return "Слабая аппроксимация"
    return "Точность аппроксимации недостаточна"


def calc_errors(y_true: List[float], y_pred: List[float]) -> List[float]:
    
    if len(y_true) != len(y_pred):
        raise ValueError("Длины y_true и y_pred должны совпадать")

    return [yp - yt for yt, yp in zip(y_true, y_pred)]