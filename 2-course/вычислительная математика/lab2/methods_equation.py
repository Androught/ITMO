import math
from operator import eq


MAX_ITER = 1000


def validate_interval(a, b):
    if a >= b:
        raise ValueError("Должно выполняться a < b.")


def has_sign_change(f, a, b):
    return f(a) * f(b) < 0


def count_sign_changes_on_subintervals(f, a, b, parts=100):

    h = (b - a) / parts
    count = 0
    x_prev = a
    f_prev = f(x_prev)

    for i in range(1, parts + 1):
        x_cur = a + i * h
        f_cur = f(x_cur)
        if f_prev == 0:
            count += 1
        elif f_prev * f_cur < 0:
            count += 1
        x_prev, f_prev = x_cur, f_cur

    return count


def choose_initial_guess(eq, a, b):
    if eq.f(a) * eq.ddf(a) > 0:
        return a
    if eq.f(b) * eq.ddf(b) > 0:
        return b
    return a


def fixed_chord_method(eq, a, b, eps, max_iter=MAX_ITER):

    validate_interval(a, b)
    f = eq.f

    if not has_sign_change(f, a, b):
        raise ValueError("На интервале нет смены знака, корень не гарантирован.")                                                                                                                                           

    if f(a) * eq.ddf(a) > 0:
        fixed = a
        x_prev = b
    elif f(b) * eq.ddf(b) > 0:
        fixed = b
        x_prev = a
    else:
        fixed = a
        x_prev = b

    table = []

    for i in range(1, max_iter + 1):
        f_fixed = f(fixed)
        f_prev = f(x_prev)
        denom = f_fixed - f_prev

        if abs(denom) < 1e-14:
            raise ZeroDivisionError("Деление на ноль в методе хорд.")

        x_next = x_prev - ((fixed - x_prev) / denom) * f_prev
        diff = abs(x_next - x_prev)

        table.append({
            "iter": i,
            "fixed": fixed,
            "x": x_prev,
            "f_fixed": f_fixed,
            "f_x": f_prev,
            "x_next": x_next,
            "diff": diff,
        })

        if diff <= eps or abs(f(x_next)) <= eps:
            return {
                "root": x_next,
                "f_root": f(x_next),
                "iterations": i,
                "table": table,
                "method": "Метод хорд",
            }

        x_prev = x_next

    raise RuntimeError("Превышено максимальное число итераций в методе хорд.")


def newton_method(eq, a, b, eps, max_iter=MAX_ITER):
    validate_interval(a, b)
    f = eq.f
    df = eq.df

    if not has_sign_change(f, a, b):
        raise ValueError("На интервале нет смены знака, корень не гарантирован.")

    x = choose_initial_guess(eq, a, b)
    table = []

    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-14:
            raise ZeroDivisionError("Производная равна нулю в методе Ньютона.")

        x_next = x - fx / dfx
        diff = abs(x_next - x)

        table.append({
            "iter": i,
            "x": x,
            "fx": fx,
            "dfx": dfx,
            "x_next": x_next,
            "diff": diff,
        })

        if diff <= eps or abs(f(x_next)) <= eps:
            return {
                "root": x_next,
                "f_root": f(x_next),
                "iterations": i,
                "table": table,
                "method": "Метод Ньютона",
            }

        x = x_next

    raise RuntimeError("Превышено максимальное число итераций в методе Ньютона.")


def check_simple_iteration_convergence(eq, a, b, lam, samples=200):
    max_val = 0.0

    for i in range(samples + 1):
        x = a + (b - a) * i / samples
        dphi = 1 + lam * eq.df(x)
        max_val = max(max_val, abs(dphi))

    return max_val < 1, max_val


def compute_lambda(eq, a, b, samples=200):
    min_df = float("inf")
    max_df = float("-inf")
    max_abs_df = 0.0

    for i in range(samples + 1):
        x = a + (b - a) * i / samples
        d = eq.df(x)

        min_df = min(min_df, d)
        max_df = max(max_df, d)
        max_abs_df = max(max_abs_df, abs(d))

    if max_abs_df == 0:
        raise ValueError("Производная равна нулю на интервале.")

    if min_df > 0:
        return -1 / max_abs_df

    if max_df < 0:
        return 1 / max_abs_df

    raise ValueError(
        "Для метода простой итерации на этом интервале f'(x) меняет знак. "
        "Нужно выбрать другой интервал."
    )


def simple_iteration_method(eq, a, b, eps, max_iter=MAX_ITER):
    validate_interval(a, b)
    f = eq.f

    lam = compute_lambda(eq, a, b)

    def phi(x):
        return x + lam * f(x)

    converges, q = check_simple_iteration_convergence(eq, a, b, lam)
    if not converges:
        raise ValueError(
            f"Достаточное условие сходимости не выполняется: max|phi'(x)| = {q:.6f} >= 1"
        )

    x = choose_initial_guess(eq, a, b)
    table = []

    for i in range(1, max_iter + 1):
        x_next = phi(x)
        diff = abs(x_next - x)
        fx_next = f(x_next)

        table.append({
            "iter": i,
            "x": x,
            "x_next": x_next,
            "fx_next": fx_next,
            "diff": diff,
        })

        if diff <= eps or abs(fx_next) <= eps:
            return {
                "root": x_next,
                "f_root": fx_next,
                "iterations": i,
                "table": table,
                "method": "Метод простой итерации",
                "q": q,
                "lambda": lam,
            }

        x = x_next

    raise RuntimeError("Превышено максимальное число итераций в методе простой итерации.")

def format_equation_result(result):
    lines = []
    lines.append(f"Метод: {result['method']}")
    if "q" in result:
        lines.append(f"Оценка q = {result['q']:.6f}")
    lines.append(f"Корень: {result['root']:.6f}")
    lines.append(f"f(x): {result['f_root']:.6f}")
    lines.append(f"Число итераций: {result['iterations']}")
    lines.append("")

    if result["method"] == "Метод хорд":
        header = (
            f"{'№':>4} | {'x_fix':>12} | {'x_k':>12} | {'f(x_fix)':>12} | "
            f"{'f(x_k)':>12} | {'x_k+1':>12} | {'|Δx|':>12}"
        )
        lines.append(header)
        lines.append("-" * len(header))

        for row in result["table"]:
            lines.append(
                f"{row['iter']:>4} | "
                f"{row['fixed']:>12.6f} | "
                f"{row['x']:>12.6f} | "
                f"{row['f_fixed']:>12.6f} | "
                f"{row['f_x']:>12.6f} | "
                f"{row['x_next']:>12.6f} | "
                f"{row['diff']:>12.6f}"
            )

    elif result["method"] == "Метод Ньютона":
        header = (
            f"{'№':>4} | {'x_k':>12} | {'f(x_k)':>12} | {'f\'(x_k)':>12} | "
            f"{'x_k+1':>12} | {'|Δx|':>12}"
        )
        lines.append(header)
        lines.append("-" * len(header))

        for row in result["table"]:
            lines.append(
                f"{row['iter']:>4} | "
                f"{row['x']:>12.6f} | "
                f"{row['fx']:>12.6f} | "
                f"{row['dfx']:>12.6f} | "
                f"{row['x_next']:>12.6f} | "
                f"{row['diff']:>12.6f}"
            )

    else:
        header = (
            f"{'№':>4} | {'x_k':>12} | {'x_k+1':>12} | {'f(x_k+1)':>12} | {'|Δx|':>12}"
        )
        lines.append(header)
        lines.append("-" * len(header))

        for row in result["table"]:
            lines.append(
                f"{row['iter']:>4} | "
                f"{row['x']:>12.6f} | "
                f"{row['x_next']:>12.6f} | "
                f"{row['fx_next']:>12.6f} | "
                f"{row['diff']:>12.6f}"
            )

    return "\n".join(lines)