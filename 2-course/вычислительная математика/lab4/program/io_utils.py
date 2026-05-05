from typing import List, Tuple, Dict, Any


def validate_points(x: List[float], y: List[float]) -> None:
    
    if len(x) != len(y):
        raise ValueError("Количество x и y должно совпадать")

    if not (8 <= len(x) <= 12):
        raise ValueError("Таблица должна содержать от 8 до 12 точек")

    if len(set(x)) != len(x):
        raise ValueError("Значения x не должны повторяться")


def read_from_console() -> Tuple[List[float], List[float]]:
    
    try:
        n = int(input("Введите количество точек (от 8 до 12): ").strip())
    except ValueError:
        raise ValueError("Количество точек должно быть целым числом")

    if not (8 <= n <= 12):
        raise ValueError("Количество точек должно быть от 8 до 12")

    x = []
    y = []

    print("Введите точки построчно в формате: x y")

    for i in range(n):
        line = input(f"Точка {i + 1}: ").strip().replace(",", ".")
        parts = line.split()

        if len(parts) != 2:
            raise ValueError(f"Некорректный ввод в строке {i + 1}: нужно ввести два числа")

        try:
            xi = float(parts[0])
            yi = float(parts[1])
        except ValueError:
            raise ValueError(f"Некорректный ввод в строке {i + 1}: x и y должны быть числами")

        x.append(xi)
        y.append(yi)

    validate_points(x, y)
    return x, y


def read_from_file(filename: str) -> Tuple[List[float], List[float]]:
    
    x = []
    y = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise ValueError(f"Файл не найден: {filename}")

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        line = line.replace(",", ".")
        parts = line.split()

        if len(parts) != 2:
            raise ValueError(
                f"Некорректный формат в строке {line_number}: должно быть ровно два числа"
            )

        try:
            xi = float(parts[0])
            yi = float(parts[1])
        except ValueError:
            raise ValueError(
                f"Некорректные данные в строке {line_number}: x и y должны быть числами"
            )

        x.append(xi)
        y.append(yi)

    validate_points(x, y)
    return x, y


def save_results_to_file(filename: str, results: List[Dict[str, Any]], best_model: Dict[str, Any]) -> None:
    
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Результаты аппроксимации\n")

        for result in results:
            if "error" in result:
                file.write(f"Модель: {result['name']}\n")
                file.write(f"Ошибка: {result['error']}\n")
                file.write("-" * 60 + "\n")
                continue

            file.write(f"Модель: {result['name']}\n")
            file.write(f"Формула: {result['formula']}\n")
            file.write("Коэффициенты:\n")

            for key, value in result["coefficients"].items():
                file.write(f"  {key} = {value:.6f}\n")

            file.write(f"S = {result['S']:.6f}\n")
            file.write(f"delta = {result['delta']:.6f}\n")
            file.write(f"R^2 = {result['R2']:.6f}\n")
            file.write(f"Оценка по R^2: {result['R2_quality']}\n")

            if result["pearson"] is not None:
                file.write(f"Коэффициент Пирсона = {result['pearson']:.6f}\n")

            file.write(f"x      = {format_list(result['x'])}\n")
            file.write(f"y      = {format_list(result['y'])}\n")
            file.write(f"phi(x) = {format_list(result['y_pred'])}\n")
            file.write(f"eps    = {format_list(result['eps'])}\n")
            file.write("-" * 60 + "\n")

        file.write("\nЛучшая модель\n")

        file.write(f"{best_model['name']}\n")
        file.write(f"Формула: {best_model['formula']}\n")
        file.write(f"delta = {best_model['delta']:.6f}\n")


def format_list(values: List[float], digits: int = 6) -> str:
    
    return "[" + ", ".join(f"{value:.{digits}f}" for value in values) + "]"


def print_model_result(result: Dict[str, Any]) -> None:
    
    if "error" in result:
        print(f"Модель: {result['name']}")
        print(f"Ошибка: {result['error']}")
        print("-" * 60)
        return

    print(f"Модель: {result['name']}")
    print(f"Формула: {result['formula']}")
    print("Коэффициенты:")

    for key, value in result["coefficients"].items():
        print(f"  {key} = {value:.6f}")

    print(f"S = {result['S']:.6f}")
    print(f"delta = {result['delta']:.6f}")
    print(f"R^2 = {result['R2']:.6f}")
    print(f"Оценка по R^2: {result['R2_quality']}")

    if result["pearson"] is not None:
        print(f"Коэффициент Пирсона = {result['pearson']:.6f}")

    print(f"x      = {format_list(result['x'])}")
    print(f"y      = {format_list(result['y'])}")
    print(f"phi(x) = {format_list(result['y_pred'])}")
    print(f"eps    = {format_list(result['eps'])}")
    print("-" * 60)


def print_all_results(results: List[Dict[str, Any]], best_model: Dict[str, Any]) -> None:
    
    print("\nРезультаты аппроксимации")


    for result in results:
        print_model_result(result)

    print("\nЛучшая модель")
    print(f"Название: {best_model['name']}")
    print(f"Формула: {best_model['formula']}")
    print(f"delta = {best_model['delta']:.6f}")