import json
import logging
import os
import requests
import redis

from app.main.config import Config
from app.main.model.redis_connection import RedisConnection
from app.main.model.config_on_redis import get_config_on_redis, get_list_on_redis, hget_config_on_redis
from app.main.model.outbound_message import OutboundMessage
from app.main.model.inbound_message import InboundMessage

redis = RedisConnection()
redis_con = redis.connect()

class OutputData(object):
    funcional_logger: logging.Logger
    terminal_reclamado: str #REDIS - msisdn
    nome_reclamante: str # pegar da aplicação
    telefone_contato: str #REDIS - (NUM_BINADO) - contexto ligação
    tipo_registro: str # REDIS - contexto ligação
    evento_fixo_numero: str #REDIS - msisdn
    evento_fixo_promessa: str #REDIS - msisdn
    evento_velox_numero: str #REDIS- msisdn
    evento_velox_datapromessa: str #REDIS - msisdn
    nota: str #construído por função
    flag_anatel: str #REDIS - contexto ligação

    def __init__(self):
        self.funcional_logger = logging.getLogger('funcional')

    def create_intent_note(self, outbound_message):
        last_intent = outbound_message.intent #TODO: mudar pra pegar intent do REDIS
        intent_note = get_config_on_redis('intent-nota', last_intent)

        if intent_note:
            final_intent_note = intent_note
        else:
            final_intent_note = ''     
        return final_intent_note

    
    def create_register_note(self, session, outbound_message):
        last_etapa = hget_config_on_redis(session, "etapa") #TODO: pegar do REDIS
        register_note = get_config_on_redis('registro-campo-nota', last_etapa)

        if last_etapa in ['motivo_contato', 'evento', 'instrucoes_finais']:
            note = register_note + self.create_intent_note(outbound_message)
        elif last_etapa == 'hang-up':
            note = register_note
        else:
            note = ''
        return note
    
    def set_evento(self, msisdn_reclamado):
        #TODO: verificar se a informação virá assim mesmo
        msisdn_context = redis_con.hgetall(msisdn_reclamado)
        if msisdn_context['evento_fixo'] == 'Y' and msisdn_context['evento_velox'] == 'N':
            evento = 'Somente Fixo'
        elif msisdn_context['evento_fixo'] == 'N' and msisdn_context['evento_velox'] == 'Y':
            evento = 'Somente Velox'
        elif msisdn_context['evento_fixo'] == 'Y' and msisdn_context['evento_velox'] == 'Y':
            evento = 'Fixo e Velox'

        return evento
    
    def set_prazo(self, msisdn_reclamado):
        msisdn_context = redis_con.hgetall(msisdn_reclamado)
        if msisdn_context['prazo_vencido'] == 'Y':
            prazo = 'tipo-registro-prazo-fora'
        else:
            prazo = 'tipo-registro-prazo-dentro'
        return prazo

    def set_tipo_registro(self, msisdn_reclamado):
        evento = self.set_evento(msisdn_reclamado)
        prazo = self.set_prazo(msisdn_reclamado)
        tipo_registro = get_config_on_redis(prazo, evento)

        return tipo_registro

    
    def get_output_data(self, msisdn_reclamado, outbound_message, inbound_message):
        #TODO: pegar dados do REDIS
        msisdn_context = redis_con.hgetall(msisdn_reclamado)
        self.logger = logging.getLogger('output oi')
        self.terminal_reclamado = msisdn_context['msisdn_reclamado']
        self.nome_reclamante = hget_config_on_redis(inbound_message.session_verbio, 'nome_reclamante')
        self.telefone_contato = inbound_message.msisdn_binado 
        self.tipo_registro = self.set_tipo_registro(msisdn_reclamado)
        self.evento_fixo_numero = msisdn_context['id_evento'] #TODO: como tratar?
        self.evento_fixo_promessa = msisdn_context['evento_datapromessa']  #TODO: como tratar?
        self.evento_velox_numero = msisdn_context['id_evento'] #TODO: como tratar?
        self.evento_velox_datapromessa = msisdn_context['evento_datapromessa']#TODO: como tratar
        self.nota = self.create_register_note(inbound_message.session_verbio,outbound_message)
        self.flag_anatel = redis_con.hget(inbound_message.session_verbio, 'flag_anatel')

        output = {"Terminal_Reclamado": self.terminal_reclamado,
                      "Nome_reclamante": self.nome_reclamante,
                      "Telefone_Contato": self.telefone_contato,
                      "Tipo_Registro": self.tipo_registro,
                      "Evento_Fixo_Numero": self.evento_fixo_numero,
                      "Evento_Fixo_DataPromessa": self.evento_fixo_promessa,
                      "Evento_Velox_Numero": self.evento_velox_numero,
                      "Evento_Velox_DataPromessa": self.evento_velox_datapromessa,
                      "Nota": self.nota,
                      "Flag_Anatel": self.flag_anatel}
        return output

    def post_output_data(self, inbound_message, outbound_message):
        #TODO: pegar registrar_atendimento do REDIS
        if redis_con.hget(inbound_message.session_verbio, 'registrar_atendimento') == 'Y': 
            endpoint = 'http://localhost:9100' #TODO: pegar do arquivo de configuração
            output = self.get_output_data(inbound_message.msisdn_reclamado, outbound_message, inbound_message)
            self.funcional_logger.info("[%s] Dados enviados para o STC/SAC: [%s]", inbound_message.session_verbio, output)
            #requests.post(url=endpoint, data=json.dumps(output))
        return outbound_message