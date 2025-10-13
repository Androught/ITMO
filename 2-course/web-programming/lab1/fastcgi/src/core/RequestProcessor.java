package src.core;

import src.http.HttpWriter;
import src.model.ErrorPayLoad;
import src.model.Result;
import src.util.QueryString;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

/**
 * Производит парсинг, валидацию, бизнес-логику и формирование ответа для 1 запроса
 */
public class RequestProcessor {
    private final QueryString qs;
    private final Validator validator;
    private final HitService hitService;
    private final HttpWriter http;

    private static final DateTimeFormatter TS_FMT =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");


    /**
     * @param qs парсер query-string
     * @param validator валидатор входных данных
     * @param hitService сервис вычисления попадания точки в область
     * @param http вывод HTTP-ответа
     */
    public RequestProcessor(QueryString qs, Validator validator, HitService hitService, HttpWriter http) {
        this.qs = qs;
        this.validator = validator;
        this.hitService = hitService;
        this.http = http;
    }

    /**
     * Обработчик запроса
     * @param queryString исходный QUERY_STRING
     * @param startNs время старта обработки запроса
     */
    public void requestHandler(String queryString, long startNs) {

        String stringX = qs.get(queryString, "x");
        String stringY = qs.get(queryString, "y");
        String stringR = qs.get(queryString, "r");

        if (stringX == null || stringY == null || stringR == null) {
            writeBadRequest("missing params (need x, y, r)");
            return;
        }

        Double x = tryParseDouble(stringX);
        Double y = tryParseDouble(stringY);
        Double r = tryParseDouble(stringR);
        if (x == null || y == null || r == null) {
            writeBadRequest("bad number format");
            return;
        }

        if (!validator.isAllowedX(x)) {
            writeBadRequest("wrong x");
            return;
        }
        if (!validator.isAllowedY(y)) {
            writeBadRequest("wrong y");
            return;
        }
        if (!validator.isAllowedR(r)) {
            writeBadRequest("wrong r");
            return;
        }

        boolean hit = hitService.checkHit(x, y, r);
        double workingMsDouble = (System.nanoTime() - startNs) / 1_000_000.0;
        BigDecimal workingMs = BigDecimal.valueOf(workingMsDouble).setScale(2, RoundingMode.HALF_UP);
        String serverTime = ZonedDateTime.now(ZoneOffset.ofHours(3))
                .truncatedTo(ChronoUnit.SECONDS)
                .format(TS_FMT);

        Result result = new Result(x, y, r, hit, serverTime, workingMs);
        http.writeJson(200, result.toJson());
    }

    private void writeBadRequest(String msg) {
        http.writeJson(400, new ErrorPayLoad(msg).toJson());
    }

    private static Double tryParseDouble(String s) {
        try {
            return Double.parseDouble(s);
        } catch (NumberFormatException exception) {
            return null;
        }
    }
}
