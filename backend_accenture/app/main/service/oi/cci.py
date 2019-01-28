import requests
from string import Template
import json
import logging
from app.main.config import Config

from ...model.event import Event

# TODO: Lembrar que funciona apenas pro velox
class CCI():
    __base_url__: str
    __port__: int
    __logger__: logging.Logger = logging.getLogger('cci')
    __query_result__: dict = dict(
        OK = 'OK',
        ERR = 'ERR'
    )
    __session__: str

    def __init__(self, session: str):
        self.__base_url__ = Config.find_in_dict(["backend-oi", "cci", "base-url"])
        self.__port__ = Config.find_in_dict(["backend-oi", "cci", "port"])
        self.__session__ = session

    def get_event_info(self, terminal: str):
        event = Event()

        result, response = self.__request_query__(terminal)
        if not result:
            return event

        if "id_ordem" not in response.keys():
            return event

        id_ordem = response["id_ordem"]
            
        result, response = self.__execute_query__(id_ordem)
        if not result:
            return event
        
        event.fill(response)
        return event

    # EXEMPLOS RESPOSTA:
    # https://e12b8a74-ec45-4c4a-8870-323f6632fd3b.mock.pstmn.io/VTTIntegrationWebservice/rs/rec/requestQueryOS/2112345678
    # {
    #     "idOrdem" : 1234567890,
    #     "msg":"",
    #     "result":"OK"
    # }    
    # {
    #     "idOrdem":"58459",
    #     "msg":"Nao Existe Requisicao para o Id Informado",
    #     "result":"OK"
    # }   
    # {
    #     "result":"ERR",
    #     "msg":"Dados nao encontrados"
    # }
    def __request_query__(self, terminal: str):
        request_data = { 
            'host': self.__base_url__,
            '__port__': self.__port__,
            'req_url': Config.find_in_dict(["backend-oi", "cci", "request-query-os"]),
            'terminal': terminal
        }
        
        request_url = Template('$host:$__port__/$req_url/$terminal')
        return self.__make_request__(request_url.substitute(request_data))

    # EXEMPLOS RESPOSTA:
    # { 
    #     "idOrdem":3456,
    #     "idEventRec":1,
    #     "eventNumber":"4733-09-2016",
    #     "forecastDate":'2016-09-13T00:47:48-03:00',
    #     "initialDate":'2016-09-12T18:47:48-03:00',
    #     "endDate":'31/07/2016',
    #     "requestDateREC":'2016-10-10T14:06:28-03:00',
    #     "resultDateREC":'2016-10-10T14:06:28-03:00',
    #     "descrEventType":"EXISTE EVENTO DE INTERRUPCAO NAO PROGRAMADA",
    #     "result":"OK",
    #     "msg":"Sucesso",
    #}
        
    #{
    #     "idOrdem":"3456",
    #     "msg":"Sem evento REC",
    #     "result":"OK"
    # }
    def __execute_query__(self, id_ordem):
        request_data = { 
            'host': self.__base_url__,
            '__port__': self.__port__,
            'req_url': Config.find_in_dict(["backend-oi", "cci", "query-os"]),
            'id_ordem': id_ordem
        }
        
        request_url = Template('$host:$__port__/$req_url/$id_ordem')
        return self.__make_request__(request_url.substitute(request_data))

    def __make_request__(self, url: str):
        self.__logger__.debug("[%s]REQUEST - URL: [%s]", self.__session__, url)
        
        res = requests.get(url)
        
        self.__logger__.debug("[%s]RESPONSE - Status: [%d]", self.__session__, res.status_code)
        if res.status_code != 200:
            return False, None

        response = res.json()
        self.__logger__.debug("[%s]RESPONSE - json: [%s]", self.__session__, response)
        if "result" not in response.keys():
            return False, None

        if response["result"] != self.__query_result__["OK"]:
            return False, None

        return True, response

    def create_bd(self):
        return True

    def create_bde(self):
        return True
    
    def create_bte(self):
        return True

    def create_btria(self):
        return True