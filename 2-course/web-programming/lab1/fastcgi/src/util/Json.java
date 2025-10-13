package src.util;

import java.util.Locale;

/**
 * Формирование JSON-строк
 */
public final class Json {
    private Json() {}

    /**
     * Строит JSON-объект из попарно переданных ключей и значений
     *
     * @param kv последовательность ключей и значений
     * @return строка JSON-объекта
     * @throws IllegalArgumentException если число аргументов нечетно
     */
    public static String obj(Object... kv) {
        if (kv.length % 2 != 0) throw new IllegalArgumentException("kv must be even length");
        StringBuilder sb = new StringBuilder().append('{');
        for (int i = 0; i < kv.length; i += 2) {
            if (i > 0) sb.append(',');
            sb.append(quote(String.valueOf(kv[i]))).append(':').append(encode(kv[i + 1]));
        }
        return sb.append('}').toString();
    }

    /**
     * Возвращает строку в кавычках с экранированием специальных символов
     *
     * @param s исходная строка
     * @return экранированная строка в двойных кавычках
     */
    public static String quote(String s) {

        return "\"" + escape(s) + "\"";
    }

    /**
     * Экранирует специальные символы
     *
     * @param s исходная строка
     * @return экранированная строка без кавычек
     */
    public static String escape(String s) {
        StringBuilder out = new StringBuilder(s.length() + 8);
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '\\' -> out.append("\\\\");
                case '\"' -> out.append("\\\"");
                case '\b' -> out.append("\\b");
                case '\f' -> out.append("\\f");
                case '\n' -> out.append("\\n");
                case '\r' -> out.append("\\r");
                case '\t' -> out.append("\\t");
                default -> out.append(c);
            }
        }
        return out.toString();
    }

    /**
     * Кодирует одиночное значение в представление JSON
     *
     * @param v  значение для сериализации
     * @return строковое JSON-представление значения
     */
    private static String encode(Object v) {
        return switch (v) {
            case null -> "null";
            case Boolean b -> b ? "true" : "false";
            case Number n -> String.format(Locale.ROOT, "%s", n);
            default -> quote(String.valueOf(v));
        };
    }
}