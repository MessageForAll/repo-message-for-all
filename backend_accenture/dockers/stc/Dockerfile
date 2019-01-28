FROM python:3.7

ENV PAV_OI_ENV=prod
ENV TZ=America/Sao_Paulo
WORKDIR /app/
RUN pip install flask-bcrypt;\
    pip install --upgrade "watson-developer-cloud>=1.5.0";\
    pip install flask;\
    pip install flask-script;\
    pip install flask-restplus;\
    pip install redis;\
    pip install pymongo
RUN cd /app;\
    mkdir registro;\
    chmod -R 777 registro
COPY ./app/tests/mocks/mock_stc_sac.py /app/
EXPOSE 8083
RUN chmod a+x ./mock_stc_sac.py
 