def euler(f, x0, y0, xn, h):
    result = []

    x = x0
    y = y0

    while x <= xn + 1e-9:
        result.append((x, y))
        y = y + h * f(x, y)
        x = x + h

    return result


def improved_euler(f, x0, y0, xn, h):
    result = []

    x = x0
    y = y0

    while x <= xn + 1e-9:
        result.append((x, y))

        y_pred = y + h * f(x, y)

        y = y + h / 2 * (
            f(x, y) + f(x + h, y_pred)
        )

        x = x + h

    return result


def milne(f, x0, y0, xn, h, eps):
    result = improved_euler(f, x0, y0, xn, h)

    if len(result) < 4:
        raise ValueError("Для метода Милна нужно минимум 4 точки")

    result = result[:4]

    while result[-1][0] + h <= xn + 1e-9:
        i = len(result)

        x_i = x0 + i * h

        x_im4, y_im4 = result[i - 4]
        x_im3, y_im3 = result[i - 3]
        x_im2, y_im2 = result[i - 2]
        x_im1, y_im1 = result[i - 1]

        f_im3 = f(x_im3, y_im3)
        f_im2 = f(x_im2, y_im2)
        f_im1 = f(x_im1, y_im1)

        y_pred = y_im4 + 4 * h / 3 * (
            2 * f_im3 - f_im2 + 2 * f_im1
        )

        for _ in range(100):
            f_pred = f(x_i, y_pred)

            y_corr = y_im2 + h / 3 * (
                f_im2 + 4 * f_im1 + f_pred
            )

            if abs(y_corr - y_pred) <= eps:
                break

            y_pred = y_corr

        result.append((x_i, y_corr))

    return result


def runge_error(method, f, x0, y0, xn, h, p):
    result_h = method(f, x0, y0, xn, h)
    result_h2 = method(f, x0, y0, xn, h / 2)

    y_h = result_h[-1][1]
    y_h2 = result_h2[-1][1]

    return abs(y_h - y_h2) / (2 ** p - 1)


def max_exact_error(result, exact, x0, y0):
    max_error = 0

    for x, y in result:
        exact_y = exact(x, x0, y0)
        max_error = max(max_error, abs(exact_y - y))

    return max_error