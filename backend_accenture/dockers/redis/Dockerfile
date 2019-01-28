FROM redis
COPY ./dockers/redis/redis.conf /usr/local/etc/redis/redis.conf
EXPOSE 6000
ENV TZ=America/Sao_Paulo
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]