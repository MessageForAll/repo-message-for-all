FROM mongo:3.6
LABEL mantainer="eduardo.s.dos.santos@accenture.com"
COPY ./dockers/mongo/mongod.conf /etc/mongod.conf
ENV TZ=America/Sao_Paulo
RUN apt-get update; \
apt-get install -y  python-software-properties; \
apt-get install -y apt-file; \
apt-file update; \
apt-get install -y  software-properties-common; \
apt-get install -y vim
EXPOSE 6001
CMD ["mongod"]