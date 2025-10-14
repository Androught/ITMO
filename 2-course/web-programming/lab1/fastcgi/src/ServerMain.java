package src;

import com.fastcgi.FCGIInterface;
import src.core.HitService;
import src.core.RequestProcessor;
import src.core.Validator;
import src.http.HttpWriter;
import src.time.SystemClock;
import src.util.Json;
import src.util.Logger;
import src.util.QueryString;

/**
 * Точка входа в программу и цикл принятия fcgi-запросов
 */
public class ServerMain {
    public static void main(String[] args) {
        FCGIInterface fcgi = new FCGIInterface();
        Logger logger = new Logger();
        HttpWriter http = new HttpWriter(logger);
        SystemClock systemClock = new SystemClock();
        RequestProcessor processor = new RequestProcessor(
                new QueryString(),
                new Validator(),
                new HitService(),
                http
        );

        while (fcgi.FCGIaccept() >= 0) {
            long startNs = systemClock.nanoTime();
            try {
                String queryString = System.getProperty("QUERY_STRING");
                processor.requestHandler(queryString, startNs);
            } catch (Throwable t) {
                logger.error("ERROR: " + t);
                http.writeJson(500, Json.obj("error", "internal"));
            }
        }

    }
















}
