
import requests
import json

class Adcc(object):    
    ses: str
   

    # TODO:
    # msisdn_binado: str
    # repetida: str

    def __init__(self):
        self.ses = "Ok"

    def enviar(self):        
        url = "http://adcc-hom.digitaltechstudio.net/app/api/input/message"
        texto_ura = "Olá, segue a segunda via de conta que você solicitou. Se precisar de alguma coisa é só me ligar."

        payload = {
        "header": {
        "timeModified": "2017-10-05T00:16:22.000-03:00",
        "requestSystem": "ADCC",
        "tenant": "x",
        "objectModelName": "FUTURECOM",
        "groupId": "20",
        "eventId": "1"
        },
        "data": {
        "ID": 5,
        "Pais": "BR",
        "Nome_cliente": "Ana",
        "Nome_tecnico": "Pedro",
        "Contato_1" : "21991278493",
        "Email" : "no.reply.adcc@gmail.com",
        "Mes" : "julho",
        "pdf" : "https://www.boletobancario.com/boletofacil/img/boleto-facil-exemplo.pdf",
        "ura" : texto_ura,
        "assuntoemail" : "Segunda via de conta"
        }
        }

        headers = {
            'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBRENDIiwiaWF0IjoxNTIwOTUwMjg3LCJleHAiOjI0OTMwMzY2ODcsImF1ZCI6IiIsInN1YiI6IiIsInVzZXIiOiJQb3N0bWFuIn0.C5lhl8HL3opXzIO_dzXp2hFBhZJbqXzVLmD3V6oWSyc",
            'Content-Type': "application/json",
            'cache-control': "no-cache",
            'Postman-Token': "60c52d5b-86d8-4d11-b0e7-79fc857a4f8d"
            }

        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

