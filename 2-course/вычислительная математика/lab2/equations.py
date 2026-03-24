import math
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class Equation:
    name: str
    f: Callable[[float], float]
    df: Callable[[float], float]
    ddf: Callable[[float], float]


def eq1_f(x):
    return 2.74 * x**3 - 1.93 * x**2 - 15.28 * x - 3.72


def eq1_df(x):
    return 8.22 * x**2 - 3.86 * x - 15.28


def eq1_ddf(x):
    return 16.44 * x - 3.86


def eq2_f(x):
    return x**3 - 1.89 * x**2 - 2 * x + 1.76


def eq2_df(x):
    return 3 * x**2 - 3.78 * x - 2


def eq2_ddf(x):
    return 6 * x - 3.78


def eq3_f(x):
    return 3 * x**3 + 1.7 * x**2 - 15.42 * x + 6.89


def eq3_df(x):
    return 9 * x**2 + 3.4 * x - 15.42


def eq3_ddf(x):
    return 18 * x + 3.4


def eq4_f(x):
    return -1.8 * x**3 - 2.94 * x**2 + 10.37 * x + 5.38


def eq4_df(x):
    return -5.4 * x**2 - 5.88 * x + 10.37


def eq4_ddf(x):
    return -10.8 * x - 5.88


def eq5_f(x):
    return -x**3 + 5.67 * x**2 - 7.12 * x + 1.34


def eq5_df(x):
    return -3 * x**2 + 11.34 * x - 7.12


def eq5_ddf(x):
    return -6 * x + 11.34


def get_available_equations() -> List[Equation]:
    return [
        Equation("2.74x^3 - 1.93x^2 - 15.28x - 3.72 = 0", eq1_f, eq1_df, eq1_ddf),
        Equation("2.74x^3 - 1.93x^2 - 15.28x - 3.72 = 0", eq2_f, eq2_df, eq2_ddf),
        Equation("x^3 - 1.89x^2 - 2x + 1.76 = 0", eq3_f, eq3_df, eq3_ddf),
        Equation("-1.8x^3 - 2.94x^2 + 10.37x + 5.38 = 0", eq4_f, eq4_df, eq4_ddf),
        Equation("-x^3 + 5.67x^2 - 7.12x + 1.34 = 0", eq5_f, eq5_df, eq5_ddf),
    ]