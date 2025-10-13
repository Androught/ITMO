package src.time;

/**
 * Системные часы
 */
public class SystemClock {
    /**
     * @return текущее время в наносекундах
     */
    public long nanoTime() {
        return System.nanoTime();
    }
}
