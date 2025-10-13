package src.core;

/**
 * Правила валидации x, y, r
 */
public class Validator {
    private static final double[] X_ALLOWED = {-3, -2, -1, 0, 1, 2, 3, 4, 5};
    private static final double[]   R_ALLOWED = {1, 1.5, 2, 2.5, 3};
    private static final double Y_MIN = -5;
    private static final double Y_MAX = 3;

    /**
     * Проверяет, принадлежит ли x заданному множеству
     *
     * @param x координата x
     * @return {@code true}, если x допустим
     */
    public boolean isAllowedX(double x) {
        return isInSet(x, X_ALLOWED);
    }

    /**
     * Проверяет, попадает ли y в диапазон
     *
     * @param y координата y
     * @return {@code true}, если y диапазоне
     */
    public boolean isAllowedY(double y) {
        return y >= Y_MIN && y <= Y_MAX;
    }

    /**
     * Проверяет, принадлежит ли r заданному множеству
     *
     * @param r радиус
     * @return {@code true}, если r допустимо
     */
    public boolean isAllowedR(double r) {
        return isInSet(r, R_ALLOWED);
    }

    private static boolean isInSet(double d, double[] arr) {
        for (double v : arr) {
            if (Double.compare(d, v) == 0) {
                return true;
            }
        }
        return false;
    }
}
