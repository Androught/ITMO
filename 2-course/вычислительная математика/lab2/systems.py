import math
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class System:
    name: str
    f1: Callable[[float, float], float]
    f2: Callable[[float, float], float]
    phi1: Callable[[float, float], float]
    phi2: Callable[[float, float], float]


def sys1_f1(x, y):
    return math.sin(x + 1) - y - 1.2


def sys1_f2(x, y):
    return 2 * x + math.cos(y) - 2


def sys1_phi1(x, y):
    return (2 - math.cos(y)) / 2


def sys1_phi2(x, y):
    return math.sin(x + 1) - 1.2


def sys2_f1(x, y):
    return math.sin(x) + 2 * y - 2


def sys2_f2(x, y):
    return x + math.cos(y - 1) - 0.7


def sys2_phi1(x, y):
    return 0.7 - math.cos(y - 1)


def sys2_phi2(x, y):
    return (2 - math.sin(x)) / 2


def sys3_f1(x, y):
    return 2 * x - math.sin(y - 0.5) - 1


def sys3_f2(x, y):
    return y + math.cos(x) - 1.5


def sys3_phi1(x, y):
    return (1 + math.sin(y - 0.5)) / 2


def sys3_phi2(x, y):
    return 1.5 - math.cos(x)


def get_available_systems() -> List[System]:
    return [
        System("sin(x + 1) - y = 1.2; 2x + cos(y) = 2", sys1_f1, sys1_f2, sys1_phi1, sys1_phi2),
        System("sin(x) + 2y = 2; x + cos(y - 1) = 0.7", sys2_f1, sys2_f2, sys2_phi1, sys2_phi2),
        System("2x - sin(y - 0.5) = 1; y + cos(x) = 1.5", sys3_f1, sys3_f2, sys3_phi1, sys3_phi2),
    ]