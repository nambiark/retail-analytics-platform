FROM metabase/metabase:latest

ENV MB_JETTY_HOST=0.0.0.0
ENV MB_JETTY_PORT=3000
ENV JAVA_OPTS="-Xmx512m"

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
  CMD curl -f http://localhost:3000/api/health || exit 1

CMD ["java", "-jar", "/app/metabase.jar"]
