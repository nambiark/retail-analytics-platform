FROM metabase/metabase:v0.49.9

ENV MB_JETTY_HOST=0.0.0.0
ENV MB_JETTY_PORT=3000
ENV JAVA_OPTS="-Xmx512m"

EXPOSE 3000

CMD ["java", "-jar", "/app/metabase.jar"]
