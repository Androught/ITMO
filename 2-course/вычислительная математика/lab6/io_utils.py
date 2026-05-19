def read_float(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Ошибка: введите число.")


def read_positive_float(message):
    while True:
        value = read_float(message)

        if value > 0:
            return value

        print("Ошибка: значение должно быть положительным.")


def choose_equation(equations):
    print("Выберите дифференциальное уравнение:")

    for i, equation in enumerate(equations, start=1):
        print(f"{i}. {equation['name']}")

    while True:
        try:
            choice = int(input("Ваш выбор: "))

            if 1 <= choice <= len(equations):
                return equations[choice - 1]

            print("Ошибка: такого варианта нет.")
        except ValueError:
            print("Ошибка: введите номер уравнения.")


def read_input_data():
    x0 = read_float("Введите x0: ")
    y0 = read_float("Введите y0: ")

    while True:
        xn = read_float("Введите xn: ")

        if xn > x0:
            break

        print("Ошибка: xn должен быть больше x0.")

    h = read_positive_float("Введите шаг h: ")
    eps = read_positive_float("Введите точность eps: ")

    if h > xn - x0:
        raise ValueError("Шаг h не должен быть больше длины интервала.")

    return x0, y0, xn, h, eps


def print_result_table(method_name, result, exact, x0, y0):
    print()
    print(method_name)
    print("-" * 72)
    print(f"{'i':<5}{'x_i':<15}{'y_i':<20}{'y_exact':<20}{'error':<15}")
    print("-" * 72)

    for i, (x, y) in enumerate(result):
        y_exact = exact(x, x0, y0)
        error = abs(y_exact - y)

        print(
            f"{i:<5}"
            f"{x:<15.6f}"
            f"{y:<20.10f}"
            f"{y_exact:<20.10f}"
            f"{error:<15.10f}"
        )

    print("-" * 72)


def print_errors(euler_error, improved_error, milne_error):
    print()
    print("Оценка погрешности:")
    print(f"Метод Эйлера по правилу Рунге: {euler_error:.10f}")
    print(f"Усовершенствованный метод Эйлера по правилу Рунге: {improved_error:.10f}")
    print(f"Метод Милна по точному решению: {milne_error:.10f}")