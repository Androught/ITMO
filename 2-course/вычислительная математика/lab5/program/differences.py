def build_finite_differences(y_values):
    

    n = len(y_values)
    table = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        table[i][0] = y_values[i]

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]

    return table


def build_divided_differences(x_values, y_values):
    

    n = len(x_values)
    table = [[0.0 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        table[i][0] = y_values[i]

    for j in range(1, n):
        for i in range(n - j):
            numerator = table[i + 1][j - 1] - table[i][j - 1]
            denominator = x_values[i + j] - x_values[i]
            table[i][j] = numerator / denominator

    return table


def is_uniform_grid(x_values, eps=1e-9):

    if len(x_values) < 2:
        return False

    h = x_values[1] - x_values[0]

    for i in range(1, len(x_values) - 1):
        current_h = x_values[i + 1] - x_values[i]
        if abs(current_h - h) > eps:
            return False

    return True


def get_step(x_values):
    
    if not is_uniform_grid(x_values):
        raise ValueError("Узлы не являются равноотстоящими")

    return x_values[1] - x_values[0]


def print_difference_table(x_values, table, title="Таблица разностей"):

    print()
    print(title)

    n = len(x_values)

    header = "x".ljust(12)
    for j in range(n):
        if j == 0:
            header += "y".ljust(14)
        else:
            header += f"Δ^{j}".ljust(14)

    print(header)
    print("-" * len(header))

    for i in range(n):
        row = f"{x_values[i]:<12.6f}"

        for j in range(n - i):
            row += f"{table[i][j]:<14.6f}"

        print(row)