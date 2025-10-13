FROM eclipse-temurin:22-jre
WORKDIR /app

COPY out/artifacts/back_jar/back.jar /app/back.jar

CMD ["java", "-DFCGI_PORT=9000", "-jar", "/app/back.jar"]

EXPOSE 9000








