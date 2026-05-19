import math


def read_float(message):
    while True:
        try:
            return float(input(message).replace(",", "."))
        except ValueError:
            print("Ошибка: введите число.")


def read_int(message):
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            print("Ошибка: число должно быть положительным.")
        except ValueError:
            print("Ошибка: введите целое число.")


def read_from_console():
    n = read_int("Введите количество точек: ")

    if n < 2:
        raise ValueError("Для интерполяции нужно минимум 2 точки.")

    x_values = []
    y_values = []

    print("Введите пары x y:")

    for i in range(n):
        x = read_float(f"x[{i}] = ")
        y = read_float(f"y[{i}] = ")

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


def read_from_file(filename):
    x_values = []
    y_values = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.replace(",", ".").split()

            if len(parts) != 2:
                raise ValueError("В каждой строке файла должно быть два числа: x y.")

            x_values.append(float(parts[0]))
            y_values.append(float(parts[1]))

    if len(x_values) < 2:
        raise ValueError("В файле должно быть минимум 2 точки.")

    return x_values, y_values


def generate_function_table():
    print("Выберите функцию:")
    print("1. sin(x)")
    print("2. cos(x)")
    print("3. x^2")

    choice = input("Ваш выбор: ")

    if choice == "1":
        function = math.sin
        function_name = "sin(x)"
    elif choice == "2":
        function = math.cos
        function_name = "cos(x)"
    elif choice == "3":
        function = lambda x: x ** 2
        function_name = "x^2"
    else:
        raise ValueError("Неизвестная функция.")

    a = read_float("Введите начало интервала a: ")
    b = read_float("Введите конец интервала b: ")
    n = read_int("Введите количество точек: ")

    if n < 2:
        raise ValueError("Нужно минимум 2 точки.")

    if a >= b:
        raise ValueError("Начало интервала должно быть меньше конца.")

    h = (b - a) / (n - 1)

    x_values = []
    y_values = []

    for i in range(n):
        x = a + i * h
        y = function(x)

        x_values.append(x)
        y_values.append(y)

    print(f"Выбрана функция: {function_name}")

    return x_values, y_values


def validate_points(x_values, y_values):
    if len(x_values) != len(y_values):
        raise ValueError("Количество x и y не совпадает.")

    if len(x_values) < 2:
        raise ValueError("Для интерполяции нужно минимум 2 точки.")

    if len(set(x_values)) != len(x_values):
        raise ValueError("Значения x не должны повторяться.")

    pairs = sorted(zip(x_values, y_values), key=lambda pair: pair[0])

    sorted_x = [pair[0] for pair in pairs]
    sorted_y = [pair[1] for pair in pairs]

    return sorted_x, sorted_y


def print_source_table(x_values, y_values):
    print()
    print("Исходная таблица:")
    print("-" * 25)
    print(f"{'i':<5}{'x':<10}{'y':<10}")
    print("-" * 25)

    for i in range(len(x_values)):
        print(f"{i:<5}{x_values[i]:<10.6f}{y_values[i]:<10.6f}")


def print_results(results):
    print()
    print("Результаты интерполяции:")
    print("-" * 60)

    for method_name, value in results.items():
        print(f"{method_name:<45} {value:.6f}")