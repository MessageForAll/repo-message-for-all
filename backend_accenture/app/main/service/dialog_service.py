from flask import request, Response
import json
import logging
import threading

from ..config import Config
from app.main.model.config_on_redis import get_config_on_redis
from .nlu.watson import Watson
from ..model.inbound_message import InboundMessage
from ..model.outbound_message import OutboundMessage
from ..model.context_chamada import ContextChamada
from .context_chamada_manager import ContextChamadaManager
from ..model.chamada import Chamada
from ..model.adcc import Adcc
from ..model.interacao import Interacao
from .oi.cci import CCI
from app.main.service.verbio_response import VerbioResponse
from app.main.service.oi.registro_chamada import OutputData
from app.main.service.context_msisdn_manager import ContextMsisdnManager
from app.main.model.database_generic import DatabaseGeneric
from app.main.model.redis_connection import RedisConnection

class DialogService(object):
    logger: logging.Logger
    
    def __init__(self):
        self.logger = logging.getLogger('service')

    def get_response(self, req: dict, msisdn_reclamado: str, client_name:str, protocolo: str):
        # TODO: capturar headers
        self.logger.debug("[%s]######################### Iniciando Dialogo #########################", req["request"]["session"])
        inbound_message = InboundMessage(req)
        
        # Busca informações do evento do CCI
        # TODO: Buscar apenas na primeira interação. Comentado porque ainda não está usando
        # cci = CCI(inbound_message.session_verbio)
        # event = cci.get_event_info(msisdn_reclamado)

        if inbound_message.user_message.lower() == 'hola':
            context_msisdn_manager = ContextMsisdnManager()
            build_context_msisdn = threading.Thread(target=context_msisdn_manager.build_context_msisdn(inbound_message),args=())           
            build_context_msisdn.start()    
        
        context_chamada_manager = ContextChamadaManager(inbound_message)
        context_chamada = context_chamada_manager.context_chamada        
        etapa_anterior = context_chamada.etapa

        # TODO: Inbound message / context / outbound message - criar metodo __str__
        self.logger.debug("[%s]Contexto Watson: [%s]", inbound_message.session_verbio, context_chamada.context_watson)
        
        # Verifica silêncio
        if not inbound_message.user_message and etapa_anterior != 'welcome':
            inbound_message.user_message = 'silence'
            self.logger.debug('[%s]REPONSE - MUTE DETECTED', inbound_message.session_verbio)
        
        #Cria outbound_message.
        outbound_message = self.__create_outbound_message__(inbound_message.user_message, context_chamada)

        # # Verifica se recebemos hangup da verbio
       
        if inbound_message.user_message == 'hang-up':                       
            registrar_atendimento_thread = threading.Thread(target=self.registrar_atendimento(inbound_message, outbound_message),args=())
            registrar_atendimento_thread.start()
            return self.__build_answer__(outbound_message, inbound_message)
        
        #Instancia e cria resposta do Watson
        nlp_adapter = Watson()
        outbound_message = nlp_adapter.execute_dialog(inbound_message,outbound_message,context_chamada)

        #Cria/Atualiza contexto de chamada
        context_chamada_manager.save_actual_context(outbound_message)
        
        #Grava a Chamada/Interação no Mongo e Elastic
        interacao = Interacao(inbound_message, outbound_message, context_chamada)
        interacao.save()

        # Workaround para testar registro de chamada apenas pelas etapas
        if outbound_message.etapa == 'transferir_atendente':                      
            registrar_atendimento_thread = threading.Thread(target=self.registrar_atendimento(inbound_message, outbound_message),args=())
            registrar_atendimento_thread.start()                       
            return self.__build_answer__(outbound_message, inbound_message)        
        
        #Feira
        if outbound_message.intent == 'pedirSegundaVia':
            self.logger.debug("[%s]ADCC: [%s]", inbound_message.session_verbio, 'Enviando Conta')
            adcc = Adcc()
            adcc.enviar()

        #Identifica nome reclamante
        if etapa_anterior == "welcome":
           save_name = threading.Thread(target=self.save_name(inbound_message.session_verbio, inbound_message.user_message),args=())
           save_name.start()

        #Retorna response Verbio    
        return self.__build_answer__(outbound_message, inbound_message)

    
    def __create_outbound_message__(self, response_utter, context):
        outbound_message = OutboundMessage()
        outbound_message.output_text = [response_utter]
        outbound_message.conversation_id = context.conversation_id        
        outbound_message.context = context.context_watson

        return outbound_message      
    
    #Cria Response Verbio
    def __build_answer__(self, outbound_message, inbound_message):        
        response_verbio = VerbioResponse()
        message, text = response_verbio.construct_response(outbound_message, inbound_message.msisdn_reclamado)        
        
        #tag next": valores possiveis hangup, tranfer, ask perguntar e aguartar resposta
        answer = {
            "answer": {
                "grammar": "",
                "next": response_verbio.next_step(outbound_message, inbound_message.msisdn_reclamado),
                "question": message,
                #"times" : outbound_message.watson_times_response,
                "session": outbound_message.conversation_id,
                "to": response_verbio.transfer_to
            }
        }
                
        self.logger.debug('RESPONSE - VERBIO: %s', json.dumps(answer))
        return json.dumps(answer), text

    def find_name(self, input):
        db = DatabaseGeneric()          
        collection = db.connect('nomes')
        input_upper = input.upper()
        input_splited = input_upper.split()
        name = ""
        for word in input_splited:
            name_found = collection.find_one({"nome": word})
            if name_found != None:
                name = name_found["nome"]
                return name
        return name

    def save_name(self, session, input):
        name = self.find_name(input) 
        if name:
            redis = RedisConnection()
            redis_cache = redis.connect()            
            db = DatabaseGeneric()                
            collection = db.connect('chamada')
            redis_cache.hset(session, 'nome_reclamante', name if name else "Não identificado")
            collection.update({'session':session},{'$set': {"nome_reclamante": name if name else "Não identificado"}}, upsert = True)

    def registrar_atendimento(self, inbound_message, outbound_message):
        registrar_atendimento = OutputData()
        registrar_atendimento.post_output_data(inbound_message,outbound_message)     