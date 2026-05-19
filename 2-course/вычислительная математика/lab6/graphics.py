import matplotlib.pyplot as plt


def plot_results(results, exact, x0, y0, xn):
    for method_name, points in results.items():
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]

        plt.plot(xs, ys, marker="o", label=method_name)

    exact_xs = []
    exact_ys = []

    steps = 200
    step = (xn - x0) / steps

    for i in range(steps + 1):
        x = x0 + i * step
        exact_xs.append(x)
        exact_ys.append(exact(x, x0, y0))

    plt.plot(exact_xs, exact_ys, label="Точное решение")

    plt.title("Численное решение ОДУ")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()