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
WORKDIR /app/
COPY ./app/tests/mocks/mock_cci.py /app/
COPY ./app/tests/mocks/registro/mock_cci.json /app/registro/mock_cci.json
EXPOSE 8082
RUN chmod -R 777 /app/registro
RUN chmod a+x ./mock_cci.py
 