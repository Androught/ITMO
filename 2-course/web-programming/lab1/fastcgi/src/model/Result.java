package src.model;

import src.util.Json;

import java.math.BigDecimal;

/**
 * Модель успешного ответа
 */
public class Result {
    private final double x;
    private final double y;
    private final double r;
    private final boolean hit;
    private final String serverTime;
    private final BigDecimal workingTimeMs;

    /**
     * @param x координата x
     * @param y координата y
     * @param r радиус
     * @param hit признак попадания
     * @param serverTime время на сервере
     * @param workingTimeMs время выполнения в миллисекундах
     */
    public Result(double x, double y, double r, boolean hit, String serverTime, BigDecimal workingTimeMs) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.hit = hit;
        this.serverTime = serverTime;
        this.workingTimeMs = workingTimeMs;
    }

    /**
     * Сериализует данные
     *
     * @return строка JSON
     */
    public String toJson() {
        String inner = Json.obj(
                "x", x,
                "y", y,
                "r", r,
                "hit", hit,
                "serverTime", serverTime,
                "workingTime", workingTimeMs
        );
        return "{\"result\":" + inner + "}";
    }
}
