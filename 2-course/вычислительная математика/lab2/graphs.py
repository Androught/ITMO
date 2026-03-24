import math
from typing import Optional

import numpy as np
import matplotlib.pyplot as plt


def plot_equation(eq, a: float, b: float, root: Optional[float] = None):

    if a >= b:
        raise ValueError("Для построения графика должно выполняться a < b.")

    margin = 0.1 * (b - a) if b > a else 1.0
    x_min = a - margin
    x_max = b + margin

    xs = np.linspace(x_min, x_max, 1000)
    ys = np.array([eq.f(x) for x in xs])

    plt.figure(figsize=(10, 6))
    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)
    plt.axvspan(a, b, alpha=0.15, label=f"Исследуемый интервал [{a:.3f}; {b:.3f}]")

    if root is not None:
        plt.scatter([root], [eq.f(root)], s=50, label=f"Корень x ≈ {root:.6f}")

    plt.title(f"График уравнения: {eq.name}")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_system(system, x_center: float = 0.0, y_center: float = 0.0, span: float = 5.0):

    if span <= 0:
        raise ValueError("span должен быть положительным.")

    x_min = x_center - span
    x_max = x_center + span
    y_min = y_center - span
    y_max = y_center + span

    x = np.linspace(x_min, x_max, 500)
    y = np.linspace(y_min, y_max, 500)
    X, Y = np.meshgrid(x, y)

    f1_vec = np.vectorize(system.f1)
    f2_vec = np.vectorize(system.f2)

    Z1 = f1_vec(X, Y)
    Z2 = f2_vec(X, Y)

    plt.figure(figsize=(10, 8))

    contour1 = plt.contour(X, Y, Z1, levels=[0], linewidths=2)
    contour2 = plt.contour(X, Y, Z2, levels=[0], linewidths=2, linestyles="dashed")

    line1_proxy = plt.Line2D([0], [0], linewidth=2, label="f1(x, y) = 0")
    line2_proxy = plt.Line2D([0], [0], linewidth=2, linestyle="dashed", label="f2(x, y) = 0")

    plt.axhline(0, linewidth=1)
    plt.axvline(0, linewidth=1)

    plt.title(f"Графики системы: {system.name}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend(handles=[line1_proxy, line2_proxy])
    plt.tight_layout()
    plt.show()