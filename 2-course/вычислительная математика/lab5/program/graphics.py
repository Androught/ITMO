import matplotlib.pyplot as plt

from interpolation import (
    lagrange_interpolation,
    newton_divided_auto,
    newton_finite_auto,
)

from differences import is_uniform_grid


def _build_graph_points(x_values, y_values, method):
    x_min = min(x_values)
    x_max = max(x_values)

    graph_x = []
    graph_y = []

    points_count = 300
    step = (x_max - x_min) / (points_count - 1)

    for i in range(points_count):
        x = x_min + i * step
        y = method(x_values, y_values, x)

        graph_x.append(x)
        graph_y.append(y)

    return graph_x, graph_y


def _draw_interpolation_point(method, x_values, y_values, interpolation_x):
    if interpolation_x is None:
        return

    interpolation_y = method(x_values, y_values, interpolation_x)

    plt.scatter(
        [interpolation_x],
        [interpolation_y],
        color="purple",
        label=f"Точка интерполяции x={interpolation_x}",
        zorder=6
    )

    plt.axvline(
        interpolation_x,
        color="purple",
        linestyle="--",
        alpha=0.5
    )

    plt.axhline(
        interpolation_y,
        color="purple",
        linestyle="--",
        alpha=0.5
    )


def plot_lagrange(x_values, y_values, interpolation_x=None):

    graph_x, graph_y = _build_graph_points(
        x_values,
        y_values,
        lagrange_interpolation
    )

    plt.figure(figsize=(10, 6))

    plt.scatter(
        x_values,
        y_values,
        color="black",
        label="Узлы интерполяции",
        zorder=5
    )

    plt.plot(
        graph_x,
        graph_y,
        color="blue",
        label="Многочлен Лагранжа"
    )

    _draw_interpolation_point(
        lagrange_interpolation,
        x_values,
        y_values,
        interpolation_x
    )

    plt.title("Интерполяционный многочлен Лагранжа")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.grid(True)
    plt.legend()
    plt.show()


def plot_newton(x_values, y_values, interpolation_x=None):
 

    plt.figure(figsize=(10, 6))

    plt.scatter(
        x_values,
        y_values,
        color="black",
        label="Узлы интерполяции",
        zorder=5
    )

    divided_x, divided_y = _build_graph_points(
        x_values,
        y_values,
        newton_divided_auto
    )

    plt.plot(
        divided_x,
        divided_y,
        color="red",
        label="Ньютон с разделёнными разностями"
    )

    if is_uniform_grid(x_values):
        finite_x, finite_y = _build_graph_points(
            x_values,
            y_values,
            newton_finite_auto
        )

        plt.plot(
            finite_x,
            finite_y,
            color="green",
            linestyle="--",
            label="Ньютон с конечными разностями"
        )

    _draw_interpolation_point(
        newton_divided_auto,
        x_values,
        y_values,
        interpolation_x
    )

    plt.title("Интерполяционные многочлены Ньютона")
    plt.xlabel("x")
    plt.ylabel("y")

    plt.grid(True)
    plt.legend()
    plt.show()