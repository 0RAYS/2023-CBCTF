FROM openjdk:8u312-slim
    
COPY ./app /app/

RUN chmod +x /app/start.sh

WORKDIR /app

CMD ["/app/start.sh"]
