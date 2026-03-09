
def read_input_keyboard():
    while True:
        first_line = input("Введите размерность(1 < n <= 20) и точность (через пробел): ").split()

        if len(first_line) != 2:
            print("Нужно ввести два значения — n и ε.")
            continue

        try:
            n = int(first_line[0])
            eps = float(first_line[1])
        except ValueError:
            print("n должно быть целым числом, ε — числом.")
            continue

        if n <= 1 or n > 20:
            print("Размерность должна быть 1 < n ≤ 20.")
            continue

        if eps <= 0:
            print("Точность должна быть положительной.")
            continue

        break


    A = []
    b = []

    print(f"Введите {n} строк по {n + 1} чисел (коэффициенты и b):")

    for i in range(n):
        while True:
            row_input = input(f"Строка {i + 1}: ").split()

            if len(row_input) != n + 1:
                print(f"Должно быть {n + 1} чисел.")
                continue

            try:
                row = list(map(float, row_input))
            except ValueError:
                print("Все элементы должны быть числами.")
                continue

            A.append(row[:n])
            b.append(row[n])
            break

    return n, A, b, eps

def read_input_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise ValueError(f"Файл '{filename}' не найден.")
    except OSError as e:
        raise ValueError(f"Ошибка при открытии файла: {e}")
    
    if len(lines) < 2:
        raise ValueError("Недостаточно данных в файле.")
    
    first_line = lines[0].split()
    if len(first_line) != 2:
        raise ValueError("Первая строка должна содержать два значения: n и ε.")

    try:
        n = int(first_line[0])
        eps = float(first_line[1])
    except ValueError:
        raise ValueError("n должно быть целым числом, ε — числом.")

    if n <= 1 or n > 20:
        raise ValueError("Размерность должна быть 1 < n ≤ 20.")

    if eps <= 0:
        raise ValueError("Точность должна быть положительной.")

    A = []
    b = []

    for i in range(1, n + 1):
        if i >= len(lines):
            raise ValueError(f"Недостаточно строк в файле. Требуется {n + 1} строк, найдено {len(lines) - 1}.")

        row_input = lines[i].split()
        if len(row_input) != n + 1:
            raise ValueError(f"Строка {i} должна содержать {n + 1} чисел.")

        try:
            row = list(map(float, row_input))
        except ValueError:
            raise ValueError(f"Все элементы строки {i} должны быть числами.")

        A.append(row[:n])
        b.append(row[n])

    return n, A, b, eps

def choose_input():
    while True:
        choice = input("Выберите способ ввода данных (1 - с клавиатуры, 2 - из файла): ")
        if choice == "1":
            return read_input_keyboard()
        elif choice == "2":
            filename = input("Введите имя файла: ")
            return read_input_file(filename)
        else:
            print("Неверный выбор. Введите 1 или 2.")

def check_matrix(A, n):
    strict_more = False
    for i in range(n):
        if (A[i][i] == 0):
            return False
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)

        if abs(A[i][i]) < row_sum:
            return False
        if abs(A[i][i]) > row_sum:
            strict_more = True

    return strict_more

def print_system(A, b):
    print("Система уравнений:")
    for i in range(len(A)):
        row_str = " ".join(f"{A[i][j]:10.6f}" for j in range(len(A[i])))
        print(f"| {row_str} | |x{i + 1}| = {b[i]:10.6f}")

def make_diagonal_dominant(A, b, n): 
    n = len(A)
    for i in range(n):
        best_row = -1
        for k in range(i, n):
            row_sum = sum(abs(A[k][j]) for j in range(n) if j != i)
            
            if abs(A[k][i]) > row_sum:
                best_row = k
                break
        if best_row == -1:
            return A, b, False
        if best_row != i:
            A[i], A[best_row] = A[best_row], A[i]
            b[i], b[best_row] = b[best_row], b[i]
    return A, b, True

def build_C_and_d(A, b, n):
    C = []
    d = []
    for i in range(n):
        if A[i][i] == 0:
            raise ValueError(f"Элемент A[{i}][{i}] равен нулю, невозможно построить матрицу C.")
        row = []
        for j in range(n):
            if i == j:
                row.append(0)
            else:
                row.append(-A[i][j]/A[i][i])
        C.append(row)
        d.append(b[i]/A[i][i])
    return C, d

def matrix_norm_inf(C, n):
    return max(sum(abs(C[i][j]) for j in range(n)) for i in range(n))

def calculate_next_x(C, d, x_prev, n):
    x_cur = []
    for i in range(n):
        s = 0
        for j in range(n):
            s += C[i][j] * x_prev[j]
        x_cur.append(s + d[i])
    return x_cur

def vector_diff(x_cur, x_prev):
    return [abs(x_cur[i] - x_prev[i]) for i in range(len(x_cur))]

def solve_simple_iterations(A, b, n, eps, max_iterations=1000):
    if not check_matrix(A, n):
        print("Матрица не имеет диагонального преобладания. Попытка привести ее к нужному виду...")
        A_new, b_new, success = make_diagonal_dominant(A, b, n)
        if not success:
            raise ValueError("Не удалось привести матрицу к диагональному преобладанию.")
        else:
            A = A_new
            b = b_new
            print("Матрица успешно приведена к диагональному преобладанию.")
    C, d = build_C_and_d(A, b, n)
    norm_C = matrix_norm_inf(C, n)
    
    print(f"Норма матрицы C: {norm_C:.6f}")
    
    if norm_C >= 1:
        raise ValueError("Норма матрицы C должна быть меньше 1 для сходимости метода.")
    x_prev = d[:]
    iterations = 0
    while iterations < max_iterations:
        x_cur = calculate_next_x(C, d, x_prev, n)
        diff = vector_diff(x_cur, x_prev)
        iterations += 1
        if max(diff) < eps:
            return x_cur, iterations, diff, norm_C, A, b
        x_prev = x_cur
    raise ValueError(f"Метод не сошелся за {max_iterations} итераций.")

def print_vector(name, v):
    print(name)
    for i, value in enumerate(v, start=1):
        print(f"{name}[{i}] = {value:.10f}")

def main():
    try:
        n, A, b, eps = choose_input()
        print()
        print("Исходные данные:")
        print_system(A, b)
        print(f"Точность ε = {eps}")
        print()

        solution, iterations, errors, norm_C, A_used, b_used = solve_simple_iterations(A, b, n, eps)

        print()
        print("Матрица, использованная в вычислениях:")
        print_system(A_used, b_used)
        print()

        print(f"Норма матрицы C: {norm_C:.10f}")
        print()

        print("Решение:")
        for i, x in enumerate(solution, start=1):
            print(f"x{i} = {x:.10f}")

        print()
        print(f"Количество итераций: {iterations}")

        print()
        print("Вектор погрешностей:")
        for i, err in enumerate(errors, start=1):
            print(f"|x{i}(k) - x{i}(k-1)| = {err:.10f}")

    except ValueError as e:
        print(f"Ошибка: {e}")
        
main()