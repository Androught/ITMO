package src.util;

/**
 * Печатает ошибки в STDERR
 */
public class Logger {
    /**
     * Печатает сообщение об ошибке
     *
     * @param msg текст сообщения
     */
    public void error(String msg) {
        try {
            System.err.println(msg);
        } catch (Exception ignore) {}
    }
}
