package src.model;

import src.util.Json;

/**
 * Модель ответа с ошибкой
 */
public class ErrorPayLoad {
    private final String message;

    /**
     * @param message сообщение об ошибке
     */
    public ErrorPayLoad(String message) {
        this.message = message;
    }

    /**
     * Сериализует ошибку в JSON
     *
     * @return строка JSON
     */
    public String toJson() {
        return Json.obj("error", message);
    }

}
