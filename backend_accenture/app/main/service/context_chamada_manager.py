from datetime import datetime
from ..model.redis_connection import RedisConnection
from ..model.inbound_message import InboundMessage
from ..model.context_chamada import ContextChamada
from ..config import Config
import redis
import os
import logging

class ContextChamadaManager(object):
    redis: ""
    redis_con: ""
    logger : logging.Logger
    context_chamada: ContextChamada

    def __init__(self, inbound_message):
        self.context_chamada = ContextChamada()
    
        # retrieving info from redis
        redis = RedisConnection()
        self.redis_con = redis.connect()
        session_info = self.redis_con.hgetall(inbound_message.session_verbio)

        # TODO: Verificar como o nome virá da URA
        
        self.context_chamada.conversation_id = inbound_message.session_verbio
        self.context_chamada.etapa = session_info["etapa"] if "etapa" in session_info else ""
        self.context_chamada.flag_anatel = session_info["flag_anatel"] if "flag_anatel" in session_info else ""
        self.context_chamada.context_watson = session_info["context_watson"] if "context_watson" in session_info else str(self.build_minimum_context(inbound_message))

        self.context_chamada.datetime_inicio = str(session_info["datetime_inicio"]) if "datetime_inicio" in session_info else str(datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
        self.context_chamada.datetime_final = str(datetime.now().__format__('%Y-%m-%d %H:%M:%S'))
        
        self.context_chamada.tempo_total = int((datetime.strptime(self.context_chamada.datetime_final, "%Y-%m-%d %H:%M:%S") - datetime.strptime(self.context_chamada.datetime_inicio,"%Y-%m-%d %H:%M:%S")).total_seconds())

    def save_actual_context(self, outbound_message) -> bool:
        self.context_chamada.context_watson = outbound_message.context
        self.context_chamada.etapa = outbound_message.context["etapa"] if "etapa" in outbound_message.context else ""
        self.context_chamada.flag_anatel = outbound_message.flag_anatel
        
        self.redis_con.hmset(self.context_chamada.conversation_id, self.context_chamada.get_json())
        self.redis_con.expire(self.context_chamada.conversation_id, 180)

    def build_minimum_context(self, inbound_message):
        sessao_anterior = self.redis_con.hmget(inbound_message.msisdn_reclamado, 'id_chamada_anterior')
        etapa_anterior = str(self.redis_con.hmget(sessao_anterior[0],'etapa')[0]) if self.redis_con.exists(sessao_anterior[0]) else ''
        minimum_context = { "conversation_id": inbound_message.session_verbio,
                            "timezone": "America/Sao_Paulo",
                            "name": "",
                            "time": datetime.now().isoformat(),
                            "etapa": "",
                            "evento_velox": str(self.redis_con.hmget(inbound_message.msisdn_reclamado, 'evento_velox')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else '',
                            "evento_fixo": str(self.redis_con.hmget(inbound_message.msisdn_reclamado, 'evento_fixo')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else '',
                            "ultima_etapa": etapa_anterior if etapa_anterior != 'welcome' else '',
                            "reaprazado" : str(self.redis_con.hmget(inbound_message.msisdn_reclamado,'reaprazado')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else '',
                            "protocolo": str(self.redis_con.hmget(inbound_message.msisdn_reclamado,'protocolo')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else '',
                            "evento_velox_tipo_evento" : str(self.redis_con.hmget(inbound_message.msisdn_reclamado,'evento_velox_tipo_evento')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else '',
                            "evento_fixo_tipo_evento" : str(self.redis_con.hmget(inbound_message.msisdn_reclamado,'evento_fixo_tipo_evento')[0]) if self.redis_con.exists(inbound_message.msisdn_reclamado) else ''
                            }

        return minimum_context