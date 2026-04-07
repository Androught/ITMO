def read_int(prompt: str, valid_values=None) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if valid_values is not None and value not in valid_values:
                print(f"Ошибка: допустимые значения {sorted(valid_values)}")
                continue
            return value
        except ValueError:
            print("Ошибка: нужно ввести целое число.")


def read_float(prompt: str) -> float:
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: нужно ввести число.")


def choose_function(functions):
    print("Выберите функцию для интегрирования:")
    for i, item in enumerate(functions, start=1):
        print(f"{i}. {item.name}")
    idx = read_int("Введите номер функции: ", valid_values=set(range(1, len(functions) + 1)))
    return functions[idx - 1]


def choose_method() -> str:
    print("Выберите метод:")
    print("1. Левые прямоугольники")
    print("2. Правые прямоугольники")
    print("3. Средние прямоугольники")
    print("4. Трапеции")
    print("5. Симпсон")
    return str(read_int("Введите номер метода: ", valid_values={1, 2, 3, 4, 5}))


def read_integration_data():
    a = read_float("Введите нижний предел интегрирования a: ")
    b = read_float("Введите верхний предел интегрирования b: ")
    eps = read_float("Введите точность eps: ")
    return a, b, eps

def validate_input(a: float, b: float, eps: float) -> None:
    if a == b:
        raise ValueError("Пределы интегрирования не должны совпадать.")
    if eps <= 0:
        raise ValueError("Точность eps должна быть положительной.")