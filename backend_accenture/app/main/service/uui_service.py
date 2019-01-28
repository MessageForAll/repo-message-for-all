from flask import request, Response
import json
import logging

from app.main.model.config_on_redis import set_list_on_redis

class UUIService(object):
    logger: logging.Logger    
    
    def __init__(self):
        self.logger = logging.getLogger('service')

    def get_response(self, request: dict):
        try:
            _list = {}
            _list['protocolo'] = request["request"]['protocolo']

            set_list_on_redis(request["request"]['callid'],_list)

            response = {
                "data": {
                    "Status": "Sucesso"
                }
            }

        except BaseException:
           response = {
                "data": {
                    "Status": "Erro"
                }
            }

        return response


      
