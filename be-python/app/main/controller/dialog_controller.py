from flask import request, Response
from flask_restplus import Resource, Namespace, fields
import json
import logging
import datetime

# TODO: 
# from .decorators import check_headers
from .decorators import token_required, check_headers
from .dto import DialogDto
from ..service.dialog_service import DialogService
from ..service.uui_service import UUIService

api = DialogDto.api
_dialog = DialogDto.dialog

@api.route("/dialog")
class ClientDialog(Resource):
    # TODO: mapear response por aqui:
    # @api.marshal_list_with(_dialog, envelope='request')
    @token_required
    @check_headers
    @api.doc('Client dialog endpoint')
    def post(self):
        inicio = datetime.datetime.now()
        logger = logging.getLogger('controller')
        
        body = request.get_json(force=True)
        
        # LOG FUNCIONAL
        funcional_logger = logging.getLogger('funcional')
        funcional_logger.info(" ")
        funcional_logger.info("[%s] VERBIO ENTRADA:", body["request"]["session"])
        funcional_logger.info("[%s] Recebido da Verbio: %s", body["request"]["session"], body["request"]["transcript"])
        funcional_logger.info("[%s] Confiança: %s", body["request"]["session"], body["request"]["confidence"])
        
        msisdn_reclamado = request.headers.get('msisdn-reclamado')
        client_name = request.headers.get('client-name')
        protocolo = request.headers.get('protocolo')

        # TODO: Colocar a session no começo da mensagem
        logger.debug('REQUEST - VERBIO: [%s]', body)

        service = DialogService()
        output, response_text = service.get_response(body, msisdn_reclamado, client_name, protocolo)
        
        # Verificando tempo de resposta da solução
        fim = datetime.datetime.now()
        diff = fim-inicio
        
        funcional_logger.info(" ")
        funcional_logger.info("[%s] VERBIO SAIDA:", body["request"]["session"])
        funcional_logger.info("[%s] Resposta enviada para a Verbio: %s", body["request"]["session"], response_text)
        funcional_logger.info("[%s] Tempo total de processamento: %f", body["request"]["session"], diff.total_seconds())

        resp = Response(response=output,
                        status=200,
                        mimetype="application/json")
        return resp

@api.route("/uui")
class ClientDialog(Resource):
    # TODO: mapear response por aqui:
    # @api.marshal_list_with(_dialog, envelope='request')
    @token_required
    @check_headers
    @api.doc('Client uui endpoint')
    def post(self):
        
        logger = logging.getLogger('controller')
        
        body = request.get_json(force=True)        
        
        # TODO: Colocar a session no começo da mensagem
        logger.debug('REQUEST - UUI: [%s]', body)
        
        service = UUIService()
        output = json.dumps(service.get_response(body))
                
        resp = Response(response=output,
                        status=200,
                        mimetype="application/json")
        
        logger.debug('RESPONSE - UUI: [%s]', resp)
        return resp 

@api.route("/cci")
class ClientDialog(Resource):
    # TODO: mapear response por aqui:
    # @api.marshal_list_with(_dialog, envelope='request')
    @token_required    
    @api.doc('Mock CCI endpoint')
    def post(self):
        
        logger = logging.getLogger('controller')
        
        body = request.get_json(force=True) 
                
        # TODO: Colocar a session no começo da mensagem
        logger.debug('REQUEST - CCI: [%s]', body)
        
        with open('app/tests/mocks/registro/cci_%s.json' %str(request.headers['msisdn']), "w+",encoding='utf8') as data_file:
            data_file.write(json.dumps(body))	

        response = {
            "data": {
                "msg": "Gravado com Sucesso"
            }
        }
        output = json.dumps(response)
                
        resp = Response(response=output,
                        status=200,
                        mimetype="application/json")
        
        logger.debug('RESPONSE - UUI: [%s]', resp)
        return resp         