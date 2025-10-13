FROM eclipse-temurin:22-jre
WORKDIR /app

COPY out/artifacts/server_jar/server.jar /app/server.jar

CMD ["java", "-DFCGI_PORT=9000", "-jar", "/app/server.jar"]

EXPOSE 9000








