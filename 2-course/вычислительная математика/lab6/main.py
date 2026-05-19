from equations import EQUATIONS
from methods import (
    euler,
    improved_euler,
    milne,
    runge_error,
    max_exact_error
)
from graphics import plot_results
from io_utils import (
    choose_equation,
    read_input_data,
    print_result_table,
    print_errors
)


def main():
    equation = choose_equation(EQUATIONS)

    f = equation["f"]
    exact = equation["exact"]

    x0, y0, xn, h, eps = read_input_data()

    euler_result = euler(f, x0, y0, xn, h)
    improved_result = improved_euler(f, x0, y0, xn, h)
    milne_result = milne(f, x0, y0, xn, h, eps)

    euler_runge_error = runge_error(
        euler,
        f,
        x0,
        y0,
        xn,
        h,
        p=1
    )

    improved_runge_error = runge_error(
        improved_euler,
        f,
        x0,
        y0,
        xn,
        h,
        p=2
    )

    milne_exact_error = max_exact_error(
        milne_result,
        exact,
        x0,
        y0
    )

    print_result_table(
        "Метод Эйлера",
        euler_result,
        exact,
        x0,
        y0
    )

    print_result_table(
        "Усовершенствованный метод Эйлера",
        improved_result,
        exact,
        x0,
        y0
    )

    print_result_table(
        "Метод Милна",
        milne_result,
        exact,
        x0,
        y0
    )

    print_errors(
        euler_runge_error,
        improved_runge_error,
        milne_exact_error
    )

    results = {
        "Метод Эйлера": euler_result,
        "Усовершенствованный метод Эйлера": improved_result,
        "Метод Милна": milne_result
    }

    plot_results(results, exact, x0, y0, xn)


if __name__ == "__main__":
    main()