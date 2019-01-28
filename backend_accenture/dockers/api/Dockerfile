FROM python:3.7

ENV PAV_OI_ENV=prod 
ENV TZ=America/Sao_Paulo

RUN pip install flask-bcrypt;\
    pip install --upgrade "watson-developer-cloud>=1.5.0";\
    pip install flask;\
    pip install flask-script;\
    pip install flask-restplus;\
    pip install redis;\
    pip install pymongo
WORKDIR /pav-oi/
COPY . /pav-oi/
EXPOSE 8081 
RUN chmod a+x ./run.sh
 