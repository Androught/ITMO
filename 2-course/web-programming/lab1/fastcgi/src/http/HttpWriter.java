package src.http;

import src.util.Logger;

import java.nio.charset.StandardCharsets;

/**
 * Пишет HTTP-заголовки и JSON-тело в STDOUT
 */
public class HttpWriter {
    private final Logger log;

    /**
     * @param log логгер для сообщений об ошибках записи
     */
    public HttpWriter(Logger log){
        this.log = log;
    }

    /**
     * Выводит JSON-ответ
     *
     * @param status HTTP-код статуса
     * @param json тело ответа
     */
    public void writeJson(int status, String json) {
        try {
            byte[] body = json.getBytes(StandardCharsets.UTF_8);
            String headers =
                    "Status: " + status + (reason(status).isEmpty() ? "" : " " + reason(status)) + "\r\n" +
                            "Content-Type: application/json; charset=utf-8\r\n" +
                            "Content-Length: " + body.length + "\r\n" +
                            "\r\n";

            System.out.write(headers.getBytes(StandardCharsets.ISO_8859_1));
            System.out.write(body);
            System.out.flush();
        } catch (Exception e) {
            log.error("WRITE_FAIL" + e);
        }
    }

    private static String reason(int status) {
        return switch (status) {
            case 200 -> "OK";
            case 400 -> "Bad Request";
            case 404 -> "Not Found";
            case 500 -> "Internal Server Error";
            default -> "";
        };


    }
}
