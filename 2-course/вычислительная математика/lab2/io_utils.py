from pathlib import Path

DATA_DIR = Path("data")
DEFAULT_INPUT_FILE = DATA_DIR / "input.txt"
DEFAULT_OUTPUT_FILE = DATA_DIR / "output.txt"


def ensure_data_dir():
    DATA_DIR.mkdir(exist_ok=True)


def choose_input_mode():
    while True:
        print("Выберите способ ввода:")
        print("1. С клавиатуры")
        print("2. Из файла")
        choice = input("Введите ваш выбор (1 или 2): ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Ошибка: нужно ввести 1 или 2.")


def choose_output_mode():
    while True:
        print("Выберите способ вывода:")
        print("1. На экран")
        print("2. В файл")
        choice = input("Введите ваш выбор (1 или 2): ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Ошибка: нужно ввести 1 или 2.")


def choose_input_file():
    ensure_data_dir()
    file_path = input(
        f"Введите путь к входному файлу (по умолчанию: {DEFAULT_INPUT_FILE}): "
    ).strip()
    return Path(file_path) if file_path else DEFAULT_INPUT_FILE


def choose_output_file():
    ensure_data_dir()
    file_path = input(
        f"Введите путь к выходному файлу (по умолчанию: {DEFAULT_OUTPUT_FILE}): "
    ).strip()
    return Path(file_path) if file_path else DEFAULT_OUTPUT_FILE


def read_float(prompt):
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            return float(raw)
        except ValueError:
            print("Ошибка: введите число.")


def read_int(prompt, valid_values=None):
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if valid_values is not None and value not in valid_values:
                print(f"Ошибка: допустимые значения: {sorted(valid_values)}")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")


def read_equation_data_keyboard(method_name: str):
    print(f"\nВвод данных для метода: {method_name}")
    a = read_float("Введите левую границу интервала a: ")
    b = read_float("Введите правую границу интервала b: ")
    eps = read_float("Введите точность eps: ")
    return {"a": a, "b": b, "eps": eps}


def read_system_data_keyboard():
    print("\nВвод данных для системы")
    x0 = read_float("Введите начальное приближение x0: ")
    y0 = read_float("Введите начальное приближение y0: ")
    eps = read_float("Введите точность eps: ")
    return {"x0": x0, "y0": y0, "eps": eps}


def read_equation_data_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    content = file_path.read_text(encoding="utf-8").replace(",", ".").split()
    if len(content) < 3:
        raise ValueError("Во входном файле должно быть 3 числа: a b eps")

    a = float(content[0])
    b = float(content[1])
    eps = float(content[2])
    return {"a": a, "b": b, "eps": eps}


def read_system_data_file(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    content = file_path.read_text(encoding="utf-8").replace(",", ".").split()
    if len(content) < 3:
        raise ValueError("Во входном файле должно быть 3 числа: x0 y0 eps")

    x0 = float(content[0])
    y0 = float(content[1])
    eps = float(content[2])
    return {"x0": x0, "y0": y0, "eps": eps}


def output_text(text: str, output_mode: str):
    if output_mode == "1":
        print(text)
    else:
        file_path = choose_output_file()
        ensure_data_dir()
        file_path.write_text(text, encoding="utf-8")
        print(f"Результат записан в файл: {file_path}")