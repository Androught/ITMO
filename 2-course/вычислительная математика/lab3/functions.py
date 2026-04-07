from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Integrand:
    name: str
    f: Callable[[float], float]



def f1(x: float) -> float:
    return -x**3 - x**2 + x + 3



def f2(x: float) -> float:
    return 2 * x**3 - 3 * x**2 + 5 * x - 9



def f3(x: float) -> float:
    return 4 * x**3 - 3 * x**2 + 5 * x - 20


def get_functions() -> List[Integrand]:
    return [
        Integrand("Функция 1: -x^3 - x^2 + x + 3", f1),
        Integrand("Функция 2: 2x^3 - 3x^2 + 5x - 9", f2),
        Integrand("Функция 3: 4x^3 - 3x^2 + 5x - 20", f3),
    ]