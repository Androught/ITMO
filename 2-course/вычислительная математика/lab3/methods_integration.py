from typing import Callable, Dict, List


INITIAL_N = 4
MAX_ITER = 25



def left_rectangles(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))


def right_rectangles(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(1, n + 1))


def middle_rectangles(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5) * h) for i in range(n))


def trapezoid_method(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    h = (b - a) / n
    s = (f(a) + f(b)) / 2
    s += sum(f(a + i * h) for i in range(1, n))
    return h * s


def simpson_method(f: Callable[[float], float], a: float, b: float, n: int) -> float:
    if n % 2 != 0:
        raise ValueError("Для метода Симпсона число разбиений n должно быть четным.")

    h = (b - a) / n
    odd_sum = sum(f(a + i * h) for i in range(1, n, 2))
    even_sum = sum(f(a + i * h) for i in range(2, n, 2))
    return h / 3 * (f(a) + f(b) + 4 * odd_sum + 2 * even_sum)


def check_runge(i_h: float, i_h2: float, k: int) -> float:
    return abs(i_h2 - i_h) / (2**k - 1)


def solve_integral(
    f: Callable[[float], float],
    a: float,
    b: float,
    eps: float,
    method_name: str,
) -> Dict:
    methods = {
        "1": ("Левые прямоугольники", left_rectangles, 1),
        "2": ("Правые прямоугольники", right_rectangles, 1),
        "3": ("Средние прямоугольники", middle_rectangles, 2),
        "4": ("Трапеции", trapezoid_method, 2),
        "5": ("Симпсон", simpson_method, 4),
    }

    if method_name not in methods:
        raise ValueError("Неизвестный метод.")

    display_name, method_func, k = methods[method_name]

    n = INITIAL_N
    if method_name == "5" and n % 2 != 0:
        n += 1

    iterations: List[Dict] = []

    current = method_func(f, a, b, n)

    for _ in range(MAX_ITER):
        n2 = n * 2
        if method_name == "5" and n2 % 2 != 0:
            n2 += 1

        next = method_func(f, a, b, n2)
        err = check_runge(current, next, k)

        iterations.append({
            "n": n,
            "i_n": current,
            "n2": n2,
            "i_n2": next,
            "runge": err,
        })

        if err <= eps:
            return {
                "method": display_name,
                "value": next,
                "n": n2,
                "runge": err,
                "iterations": iterations,
            }

        n = n2
        current = next

    raise RuntimeError(f"Не удалось достичь требуемой точности за '{MAX_ITER}' итераций.")


def format_result(result: Dict) -> str:
    lines = []
    lines.append(f"Метод: {result['method']}")
    lines.append(f"Значение интеграла: {result['value']:.10f}")
    lines.append(f"Число разбиений n: {result['n']}")
    lines.append(f"Оценка по правилу Рунге: {result['runge']:.10f}")
    lines.append("")

    header = (
        f"{'n':>8} | {'I_n':>16} | {'2n':>8} | "
        f"{'I_2n':>16} | {'Runge':>16}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for row in result["iterations"]:
        lines.append(
            f"{row['n']:>8} | "
            f"{row['i_n']:>16.10f} | "
            f"{row['n2']:>8} | "
            f"{row['i_n2']:>16.10f} | "
            f"{row['runge']:>16.10f}"
        )

    return "\n".join(lines)