import math


def f1(x, y):
    return x + y


def exact1(x, x0, y0):
    c = (y0 + x0 + 1) / math.exp(x0)
    return c * math.exp(x) - x - 1


def f2(x, y):
    return y - x ** 2


def exact2(x, x0, y0):
    c = (y0 - x0 ** 2 - 2 * x0 - 2) / math.exp(x0)
    return x ** 2 + 2 * x + 2 + c * math.exp(x)


def f3(x, y):
    return math.sin(x) - y


def exact3(x, x0, y0):
    c = (y0 - 0.5 * (math.sin(x0) - math.cos(x0))) * math.exp(x0)
    return 0.5 * (math.sin(x) - math.cos(x)) + c * math.exp(-x)


EQUATIONS = [
    {
        "name": "y' = x + y",
        "f": f1,
        "exact": exact1
    },
    {
        "name": "y' = y - x^2",
        "f": f2,
        "exact": exact2
    },
    {
        "name": "y' = sin(x) - y",
        "f": f3,
        "exact": exact3
    }
]