FROM metabase/metabase:v0.49.9

ENV MB_JETTY_HOST=0.0.0.0
ENV MB_JETTY_PORT=3000
ENV JAVA_OPTS="-Xmx512m -Dfile.encoding=UTF-8"
ENV MB_APPLICATION_DB_MAX_CONNECTION_POOL_SIZE=2

EXPOSE 3000

USER root

ENTRYPOINT []
CMD ["java", "-Xmx512m", "-Dfile.encoding=UTF-8", "-jar", "/app/metabase.jar"]
