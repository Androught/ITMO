from io_utils import (
    choose_input_mode,
    choose_output_mode,
    choose_input_file,
    read_equation_data_keyboard,
    read_system_data_keyboard,
    read_equation_data_file,
    read_system_data_file,
    output_text,
    read_int,
)
from methods_equation import (
    fixed_chord_method,
    newton_method,
    simple_iteration_method,
    format_equation_result,
    count_sign_changes_on_subintervals,
)
from methods_system import (
    simple_iteration_system,
    format_system_result,
)

from equations import get_available_equations
from systems import get_available_systems
from graphs import plot_equation, plot_system

def choose_equation():
    equations = get_available_equations()
    print("Выберите уравнение для решения:")
    for i, eq in enumerate(equations, start=1):
        print(f"{i}. {eq.name}")
    choice = read_int("Введите номер уравнения: ", valid_values=set(range(1, len(equations) + 1)))
    return equations[choice - 1]


def choose_system_of_equations():
    systems = get_available_systems()
    print("Выберите систему уравнений для решения:")
    for i, sys in enumerate(systems, start=1):
        print(f"{i}. {sys.name}")
    choice = read_int("Введите номер системы уравнений: ", valid_values=set(range(1, len(systems) + 1)))
    return systems[choice - 1]


def choose_equation_method():
    print("Методы решения уравнения:")
    print("1. Метод хорд")
    print("2. Метод Ньютона")
    print("3. Метод простой итерации")
    return read_int("Введите номер метода: ", valid_values={1, 2, 3})


def solve_equation():
    eq = choose_equation()
    method = choose_equation_method()

    input_mode = choose_input_mode()
    if input_mode == "1":
        data = read_equation_data_keyboard(
            {
                1: "Метод хорд",
                2: "Метод Ньютона",
                3: "Метод простой итерации",
            }[method]
        )
    else:
        file_path = choose_input_file()
        data = read_equation_data_file(file_path)

    a = data["a"]
    b = data["b"]
    eps = data["eps"]

    sign_changes = count_sign_changes_on_subintervals(eq.f, a, b)
    if sign_changes == 0:
        raise ValueError("На интервале не найдено смены знака. Корень не обнаружен.")
    if sign_changes > 1:
        raise ValueError("На интервале обнаружено несколько смен знака. Нужен интервал с одним корнем.")

    if method == 1:
        result = fixed_chord_method(eq, a, b, eps)
    elif method == 2:
        result = newton_method(eq, a, b, eps)
    else:
        result = simple_iteration_method(eq, a, b, eps)

    text = format_equation_result(result)
    output_mode = choose_output_mode()
    output_text(text, output_mode)
    plot_equation(eq, a, b, result["root"])


def solve_system():
    system = choose_system_of_equations()

    print("Для систем реализован метод простой итерации.")
    input_mode = choose_input_mode()

    if input_mode == "1":
        data = read_system_data_keyboard()
    else:
        file_path = choose_input_file()
        data = read_system_data_file(file_path)

    x0 = data["x0"]
    y0 = data["y0"]
    eps = data["eps"]

    result = simple_iteration_system(system, x0, y0, eps)
    text = format_system_result(result)

    output_mode = choose_output_mode()
    output_text(text, output_mode)
    plot_system(system, x0, y0, span=5.0)


def main():
    while True:
        print("\n=== Лабораторная работа №2 ===")
        print("1. Решить нелинейное уравнение")
        print("2. Решить систему нелинейных уравнений")
        print("0. Выход")

        choice = read_int("Введите пункт меню: ", valid_values={0, 1, 2})

        try:
            if choice == 1:
                solve_equation()
            elif choice == 2:
                solve_system()
            else:
                print("Завершение программы.")
                break
        except Exception as e:
            print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()