package src.util;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

/**
 * Парсер URL-кодированного QUERY_STRING
 */
public class QueryString {
    /**
     * Возвращает значение параметра из URL-кодированной строки запроса
     *
     * @param queryString сырой QUERY_STRING
     * @param name имя параметра
     * @return декодированное значение или {@code null}, если параметр отсутствует
     */
    public String get(String queryString, String name) {
        if (queryString == null || queryString.isEmpty()) return null;
        for (String pair : queryString.split("&")) {
            int i = pair.indexOf("=");
            String key = i < 0 ? pair : pair.substring(0, i);
            String value = i < 0 ? "" : pair.substring(i+1);

            try {
                key = URLDecoder.decode(key, StandardCharsets.UTF_8);
                value = URLDecoder.decode(value, StandardCharsets.UTF_8);
            } catch (Exception ignore) {}
            if (name.equals(key)) return value;
        }
        return null;
    }
}
