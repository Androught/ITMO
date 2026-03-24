import math

MAX_ITER = 1000


def check_system_iteration_convergence(system, x0, y0, h=1e-6):

    phi1 = system.phi1
    phi2 = system.phi2

    def dphidx(phi, x, y):
        return (phi(x + h, y) - phi(x - h, y)) / (2 * h)

    def dphidy(phi, x, y):
        return (phi(x, y + h) - phi(x, y - h)) / (2 * h)

    a11 = dphidx(phi1, x0, y0)
    a12 = dphidy(phi1, x0, y0)
    a21 = dphidx(phi2, x0, y0)
    a22 = dphidy(phi2, x0, y0)

    row1 = abs(a11) + abs(a12)
    row2 = abs(a21) + abs(a22)
    q = max(row1, row2)

    return q < 1, q, ((a11, a12), (a21, a22))


def simple_iteration_system(system, x0, y0, eps, max_iter=MAX_ITER):
    phi1 = system.phi1
    phi2 = system.phi2

    converges, q, jac = check_system_iteration_convergence(system, x0, y0)
    if not converges:
        raise ValueError(
            f"Достаточное условие сходимости не выполняется около начального приближения: q = {q:.6f} >= 1"
        )

    table = []

    x, y = x0, y0

    for i in range(1, max_iter + 1):
        x_next = phi1(x, y)
        y_next = phi2(x, y)

        dx = abs(x_next - x)
        dy = abs(y_next - y)

        table.append({
            "iter": i,
            "x": x,
            "y": y,
            "x_next": x_next,
            "y_next": y_next,
            "dx": dx,
            "dy": dy,
        })

        if max(dx, dy) <= eps:
            f1_val = system.f1(x_next, y_next) if hasattr(system, "f1") else None
            f2_val = system.f2(x_next, y_next) if hasattr(system, "f2") else None

            return {
                "x": x_next,
                "y": y_next,
                "iterations": i,
                "dx": dx,
                "dy": dy,
                "f1": f1_val,
                "f2": f2_val,
                "table": table,
                "method": "Метод простой итерации для системы",
                "q": q,
                "jacobian": jac,
            }

        x, y = x_next, y_next

    raise RuntimeError("Превышено максимальное число итераций для системы.")


def format_system_result(result):
    lines = []
    lines.append(f"Метод: {result['method']}")
    lines.append(f"Оценка q = {result['q']:.6f}")
    lines.append(f"x = {result['x']:.6f}")
    lines.append(f"y = {result['y']:.6f}")
    lines.append(f"Число итераций: {result['iterations']}")
    lines.append(f"Вектор погрешностей: (|dx|, |dy|) = ({result['dx']:.6f}, {result['dy']:.6f})")

    if result["f1"] is not None and result["f2"] is not None:
        lines.append(f"f1(x, y) = {result['f1']:.6f}")
        lines.append(f"f2(x, y) = {result['f2']:.6f}")

    lines.append("")

    header = (
        f"{'№':>4} | {'x_k':>12} | {'y_k':>12} | "
        f"{'x_k+1':>12} | {'y_k+1':>12} | {'|dx|':>12} | {'|dy|':>12}"
    )
    lines.append(header)
    lines.append("-" * len(header))

    for row in result["table"]:
        lines.append(
            f"{row['iter']:>4} | "
            f"{row['x']:>12.6f} | "
            f"{row['y']:>12.6f} | "
            f"{row['x_next']:>12.6f} | "
            f"{row['y_next']:>12.6f} | "
            f"{row['dx']:>12.6f} | "
            f"{row['dy']:>12.6f}"
        )

    return "\n".join(lines)