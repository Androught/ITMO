from io_utils import (
    read_from_console,
    read_from_file,
    print_all_results,
    save_results_to_file,
)
from functions import fit_all_models, get_best_model
from graphics import plot_results


def choose_input_method():
    
    print("Выберите способ ввода данных:")
    print("1 - ввод из консоли")
    print("2 - ввод из файла")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        return read_from_console()
    if choice == "2":
        filename = input("Введите имя файла: ").strip()
        return read_from_file(filename)

    raise ValueError("Некорректный выбор способа ввода")


def choose_output_method(results, best_model):
    print("Выберите способ вывода данных:")
    print("1 - вывод в консоль")
    print("2 - сохранение в файл")
    choice = input("Ваш выбор: ").strip().lower()

    if choice == "2":
        filename = input("Введите имя выходного файла: ").strip()
        save_results_to_file(filename, results, best_model)
        print(f"Результаты сохранены в файл: {filename}")
    if choice == "1":
        print_all_results(results, best_model)
    


def main():
    try:
        x, y = choose_input_method()

        results = fit_all_models(x, y)
        best_model = get_best_model(results)

        choose_output_method(results, best_model)
        plot_results(x, y, results)

    except ValueError as error:
        print(f"Ошибка: {error}")
    except Exception as error:
        print(f"Неожиданная ошибка: {error}")


if __name__ == "__main__":
    main()