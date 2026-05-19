from differences import (
    build_finite_differences,
    build_divided_differences,
    print_difference_table,
    is_uniform_grid,
)

from interpolation import (
    lagrange_interpolation,
    newton_divided_auto,
    newton_finite_auto,
)

from input_output import (
    read_float,
    read_from_console,
    read_from_file,
    generate_function_table,
    validate_points,
    print_source_table,
    print_results,
)

from graphics import plot_lagrange, plot_newton


def choose_input_method():
    print("Выберите способ ввода данных:")
    print("1. Ввести таблицу с клавиатуры")
    print("2. Прочитать таблицу из файла")
    print("3. Сгенерировать таблицу по функции")

    return input("Ваш выбор: ")


def get_data():
    choice = choose_input_method()

    if choice == "1":
        return read_from_console()

    if choice == "2":
        filename = input("Введите путь к файлу: ")
        return read_from_file(filename)

    if choice == "3":
        return generate_function_table()

    raise ValueError("Неизвестный способ ввода.")


def calculate_methods(x_values, y_values, x):
    results = {}

    results["Многочлен Лагранжа"] = lagrange_interpolation(
        x_values,
        y_values,
        x
    )

    results["Ньютон с разделёнными разностями"] = (
        newton_divided_auto(x_values, y_values, x)
    )

    if is_uniform_grid(x_values):
        results["Ньютон с конечными разностями"] = (
            newton_finite_auto(x_values, y_values, x)
        )
    else:
        print()
        print("Узлы не равноотстоящие.")
        print("Метод Ньютона с конечными разностями не применяется.")

    return results


def main():
    try:
        x_values, y_values = get_data()
        x_values, y_values = validate_points(x_values, y_values)

        print_source_table(x_values, y_values)

        divided_table = build_divided_differences(x_values, y_values)
        print_difference_table(
            x_values,
            divided_table,
            "Таблица разделённых разностей"
        )

        if is_uniform_grid(x_values):
            finite_table = build_finite_differences(y_values)
            print_difference_table(
                x_values,
                finite_table,
                "Таблица конечных разностей"
            )
        else:
            print()
            print("Таблица конечных разностей не строится, так как сетка неравномерная.")

        x = read_float("\nВведите точку интерполяции x: ")

        if x < min(x_values) or x > max(x_values):
            raise ValueError("Точка находится вне интервала узлов.")
           

        results = calculate_methods(x_values, y_values, x)
        print_results(results)

        plot_lagrange(x_values, y_values, x)
        plot_newton(x_values, y_values, x)

    except ValueError as error:
        print()
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()