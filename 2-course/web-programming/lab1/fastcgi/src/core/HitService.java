package src.core;

/**
 * Вычисляет, попала ли точка с координатами (x, y) в заданную область
 */
public class HitService {

    /**
     * Проверяет попадание точки в заданную область
     *
     * @param x координата x
     * @param y координата y
     * @param r радиус
     * @return {@code true}, если точка внутри заданной области
     */
    public boolean checkHit(double x, double y, double r) {
        boolean quarter1 = (0 <= x && x <= r) && (0 <= y && y <= r/2);
        boolean quarter2 = (x <= 0 && y >= 0) && (x*x + y*y <= (r/2)*(r/2));
        boolean quarter4 = (x >= 0 && y <=0) && (y >= x - r/2);

        return quarter1 || quarter2 || quarter4;
    }
}
