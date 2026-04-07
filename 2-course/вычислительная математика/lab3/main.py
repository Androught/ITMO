
from functions import get_functions

from io_utils import choose_function, choose_method, read_integration_data, validate_input
from methods_integration import solve_integral, format_result


def main():
    print("Начальное число разбиений: n = 4\n")

    functions = get_functions()
    chosen = choose_function(functions)
    method = choose_method()
    a, b, eps = read_integration_data()

    try:
        validate_input(a, b, eps)
        result = solve_integral(chosen.f, a, b, eps, method)
        print()
        print(f"Функция: {chosen.name}")
        print(f"Пределы интегрирования: [{a}, {b}]")
        print(f"Точность: {eps}")
        print()
        print(format_result(result))
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()