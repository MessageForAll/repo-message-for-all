# coding: utf8
# -*- coding: utf-8 -*-
import datetime
import logging
import json
from watson_developer_cloud import ConversationV1
from urllib3.exceptions import HTTPError
from app.main.config import Config
from app.main.model.redis_connection import RedisConnection
from app.main.model.config_on_redis import get_config_on_redis
from app.main.model.config_on_redis import get_list_on_redis
from random import randint

class Watson(object):
    ADAPTER_TYPE: str
    VERSION_API: str
    API_KEY: str
    API_URL: str
    API_WORKSPACE: str
    API_USER: str
    API_PASS: str
    logger: logging.Logger

    def __init__(self):
        self.ADAPTER_TYPE = Config.find_in_dict(["nlu", "engine"], "Watson")
        self.VERSION_API = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'version'])
        self.API_KEY = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'apikey'], "")
        self.API_USER = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'username'], "")
        self.API_PASS = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'password'], "")
        self.API_URL = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'url'])
        self.API_WORKSPACE = Config.find_in_dict(['nlu', self.ADAPTER_TYPE, 'workspace_id'])
        self.logger = logging.getLogger('watson')

    def execute_dialog(self, inbound_message, outbound_message,context_chamada):
        if self.API_KEY:
            conversation = ConversationV1(
                version=self.VERSION_API,
                iam_apikey=self.API_KEY,
                url=self.API_URL
            )
        else:
            conversation = ConversationV1(
                version=self.VERSION_API,
                username=self.API_USER,
                password=self.API_PASS,
                url=self.API_URL
            )

        # Obtem o response
        try:
            self.logger.debug('[%s]INPUT - Workspace: [%s]', inbound_message.session_verbio, self.API_WORKSPACE)            
            self.logger.debug('[%s]INPUT - Text: [%s]', inbound_message.session_verbio, inbound_message.user_message)        
            # valida os objetos dict dentro do dicionário context
            inicio = datetime.datetime.now()
            response = conversation.message(
                            workspace_id=self.API_WORKSPACE,
                            input = {
                                "text": inbound_message.user_message
                            },
                            context = eval(context_chamada.context_watson)
                        )

            # Verificando tempo de resposta do watson
            fim = datetime.datetime.now()
            diff = fim-inicio
            #response = response.result            
            # LOG FUNCIONAL
            funcional_logger = logging.getLogger('funcional')
            funcional_logger.info(" ")
            funcional_logger.info("[%s] PROCESSADO PELO WATSON:", inbound_message.session_verbio)
            funcional_logger.info("[%s] Tempo de processo do Watson: %f:", inbound_message.session_verbio, diff.total_seconds()) 
            
            self.logger.debug("[%s]OUTPUT - Secs: [%f]", inbound_message.session_verbio, diff.total_seconds())
            self.logger.debug("[%s]OUTPUT - Watson Response: [%s]", inbound_message.session_verbio, response) 

            # Verificando se o watson retornou alguma frase para a sequência            
            if len(response["output"]["text"]) <= 0:
                funcional_logger.info("[%s] Erro Watson: Nenhum texto retornado", inbound_message.session_verbio)
                # Caso o watson não responda nada, solicita que o cliente repita. Representa uma falha no watson                                
                #Obtem uma resposta aleatoria de nao entendimento.
                misunderstood = get_list_on_redis('nao-entendimento')
                misunderstood = misunderstood.get(str(randint(1, len(misunderstood))),'Não entendi, você pode repetir')
                response = self.__change_answer_and_context__(response, misunderstood)

                self.logger.critical("[%s]OUTPUT - Empty text from Watson", inbound_message.session_verbio)
                self.logger.debug("[%s]OUTPUT - Code Response: [%s]", inbound_message.session_verbio, response)
            else:
                text_response = response["output"]["text"]
                funcional_logger.info("[%s] Resposta do Watson: %s", inbound_message.session_verbio, text_response)
            
            etapa_anterior = context_chamada.etapa            
            if len(response["intents"]) <= 0:                                                       
                funcional_logger.info("[%s] Erro Watson: Intent não identificada", inbound_message.session_verbio)
            else:
                intent = response["intents"][0]["intent"] if "intent" in response["intents"][0] else ""               	
                confidence = response["intents"][0]["confidence"] if "confidence" in response["intents"][0] else "" 
                funcional_logger.info("[%s] Intenção identificada: %s", inbound_message.session_verbio, intent)
                funcional_logger.info("[%s] Confiança: %f", inbound_message.session_verbio, confidence)
           
            # Valida confiaça retornada da intent dentro dos thresholds configurados
            # e muda a resposta se for necessário
            #response = self.__check_intent_confidence__(response, context_chamada,etapa_anterior)

            # Constrói o outbound_message e atualiza o contexto
            outbound_message = self.__create_outbound_message__(outbound_message,response)            
            outbound_message = self.set_registrar_chamada(outbound_message, inbound_message, context_chamada)
            outbound_message = self.set_flag_anatel(outbound_message, inbound_message)                        
            # TODO: Verificar se tem status no retorno da mensagem: if response.status != 200:  

        except HTTPError as err:
            # TODO: lançar exception correta
            raise err
        except BaseException as err:
            raise err

        return outbound_message

    def __check_intent_confidence__(self, response, context_chamada,etapa_anterior):
        #Faixas: 0 = Ignorado ou Condidence inexistente | 1,2,3 = faixa de intendimento.
        response["intervalo_confianca"] = 0
        
        #etapas ignoradas
        if etapa_anterior =="welcome":            
            return response

        if len(response["intents"]) <= 0:            
            return response

        intents = response["intents"] 
        intent = intents[0]["intent"] if "intent" in intents[0] else ""
        confidence = intents[0]["confidence"] if "confidence" in intents[0] else "0"
        
        # Define threshold de entendimento      
        #misunderstood = Config.find_in_dict(['intent-confidence', 'misunderstood'])
        misunderstood = get_config_on_redis('intent-confidence', 'misunderstood')                
        ask_confirmation = get_config_on_redis('intent-confidence', 'ask-confirmation')                
        
        #Obtem uma resposta aleatoria de nao entendimento.
        misunderstood_utter = get_list_on_redis('nao-entendimento')
        misunderstood_utter = misunderstood_utter.get(str(randint(1, len(misunderstood_utter))),'Não entendi, você pode repetir')
        confirmation_utter = get_config_on_redis('entendimento-parcial', intent)
        
        if confidence < misunderstood:
            response["intervalo_confianca"] = 1
            return self.__change_answer_and_context__(response, misunderstood_utter)
        
        elif confidence < ask_confirmation:
            response["intervalo_confianca"] = 2
            return self.__change_answer_and_context__(response, confirmation_utter)
        else: 
            response["intervalo_confianca"] = 3
            
        return response

    def __change_answer_and_context__(self, response, answer):
        if answer is not None:
            response["output"]["text"].append(answer)        
        return response

    def __create_outbound_message__(self, outbound_message,watson_response):        
        intents = watson_response["intents"] if "intents" in watson_response else []
        output = watson_response["output"] if "output" in watson_response else []        
        context_response = watson_response["context"] if "context" in watson_response else {}  
           
        #cria objeto de resposta                
        outbound_message.intent = intents[0]["intent"] if len(intents) > 0 and "intent" in intents[0] else ""        
        outbound_message.watson_confidence = intents[0]["confidence"] if len(intents) > 0 and "confidence" in intents[0] else 0
        outbound_message.watson_response = output["text"][0] if len(output) > 0 and "text" in output else ""
        outbound_message.output_text = output["text"] if "text" in output else ""
        outbound_message.context = context_response
        outbound_message.watson_times_response = output["times"] if "times" in output else [{"silence": "31","interval": "5","max": "300"}]        
        outbound_message.etapa = context_response.get("etapa","") 
        outbound_message.intervalo_confianca = watson_response["intervalo_confianca"] if "intervalo_confianca" in watson_response else 0

        return outbound_message

    def set_registrar_chamada(self, outbound_message, inbound_message, context_chamada):
        if outbound_message.etapa == 'welcome':
            return outbound_message
        else:
            etapa_valida = get_list_on_redis('etapa-valida')
            if outbound_message.etapa in etapa_valida:
                redis = RedisConnection()
                redis_cache = redis.connect()
                outbound_message.registrar_atendimento = etapa_valida[outbound_message.etapa]
                context_chamada.registrar_atendimento = etapa_valida[outbound_message.etapa]
                redis_cache.hset(inbound_message.msisdn_reclamado, 'registrar_atendimento', etapa_valida[outbound_message.etapa])          
        
            return outbound_message

    def set_flag_anatel(self, outbound_message, inbound_message):
        if outbound_message.etapa == 'welcome':
            return outbound_message
        else:
            redis = RedisConnection()
            redis_cache = redis.connect()
            if outbound_message.intent == 'AmeacarAnatel':
                outbound_message.flag_anatel = 'Y'
                redis_cache.hset(inbound_message.session_verbio, 'flag_anatel', 'Y')     
            else:
                redis_cache.hset(inbound_message.session_verbio, 'flag_anatel', 'N')     

        return outbound_message


