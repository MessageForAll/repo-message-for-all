import os
import logging
import requests
import json
from datetime import datetime, timedelta
from ..config import Config
from ..model.context_msisdn import ContextMsisdn
from ..model.redis_connection import RedisConnection
from ..model.config_on_redis import get_config_on_redis
from ..model.inbound_message import InboundMessage
import os
import os.path

class ContextMsisdnManager(object):
    env : str 
    logger : logging.Logger
    
    #cci connection
    cci_url: str
    cci_port: int
    cci_request_query: str
    cci_query_os: str
    env : str

    def __init__(self):
        #CCI
        self.env = os.getenv('PAV_OI_ENV') or 'dev'
        self.cci_url = Config.find_in_dict(['backend-oi-'+ self.env, 'cci', 'base-url'])
        self.cci_port = Config.find_in_dict(["backend-oi-"+ self.env, "cci", 'port'])

    def build_context_msisdn(self,inbound_message):
        #cci con
        # url = self.cci_url + ':' + str(self.cci_port)
        # headers = {'content-type': "application/json",'msisdn': inbound_message.msisdn_reclamado}        
        # doc_cci = json.loads(requests.request("GET", url, headers=headers).text)
        #with open('...tests/mocks/registro/cci_%s.json' %str(inbound_message.msisdn_reclamado), encoding='utf-8') as data_file:
        arquivo = 'app/tests/mocks/registro/cci_%s.json' %str(inbound_message.msisdn_reclamado)
        if os.path.isfile(arquivo):            
            with open(arquivo,'r', encoding='utf-8') as data_file:
                doc_cci = json.load(data_file)
        else:            
            with open('app/tests/mocks/registro/mock_cci.json','r', encoding='utf-8') as data_file:
                doc_cci = json.load(data_file)
        

        context_msisdn = ContextMsisdn()
        context_msisdn.msisdn_reclamado = inbound_message.msisdn_reclamado
        context_msisdn.id_chamada = inbound_message.session_verbio
        context_msisdn.cpf = doc_cci["cpf"]
        context_msisdn.protocolo = doc_cci["protocolo"]
        context_msisdn.evento_fixo = doc_cci["evento_fixo"]
        context_msisdn.evento_velox = doc_cci["evento_velox"]
        context_msisdn.evento_velox_tipo_evento = doc_cci["evento_velox_tipo_evento"]
        context_msisdn.evento_fixo_tipo_evento = doc_cci["evento_fixo_tipo_evento"]

        #TODO: refatorar
        #preenche prazo com data maior
        if context_msisdn.evento_fixo == 'Y' and context_msisdn.evento_velox == 'Y' and doc_cci["evento_fixo_datapromessa"] and doc_cci["evento_velox_datapromessa"]:
            prazo_fixo = datetime.strptime(doc_cci["evento_fixo_datapromessa"],'%d/%m/%Y %H:%M:%S')
            prazo_velox = datetime.strptime(doc_cci["evento_velox_datapromessa"],'%d/%m/%Y %H:%M:%S')            
            context_msisdn.evento_datapromessa = str(prazo_fixo.strftime('%d/%m/%Y %H:%M:%S')) if prazo_fixo > prazo_velox else str(prazo_velox.strftime('%d/%m/%Y %H:%M:%S'))
            context_msisdn.id_evento = doc_cci["evento_fixo_numero"] if prazo_fixo > prazo_velox else doc_cci["evento_velox_numero"]
            context_msisdn.evento_tipo =  'fixo' if prazo_fixo > prazo_velox else 'velox'
        elif (context_msisdn.evento_fixo == 'Y' and not doc_cci["evento_fixo_datapromessa"]) or (context_msisdn.evento_velox == 'Y' and not doc_cci["evento_velox_datapromessa"]):
            context_msisdn.evento_datapromessa = ""
        else:
            context_msisdn.id_evento = doc_cci["evento_fixo_numero"] if doc_cci["evento_fixo_numero"] else doc_cci["evento_velox_numero"]
            context_msisdn.evento_tipo = 'fixo' if doc_cci["evento_fixo_numero"] else 'velox'
            context_msisdn.evento_datapromessa = doc_cci["evento_fixo_datapromessa"] if doc_cci["evento_fixo_datapromessa"] else doc_cci["evento_velox_datapromessa"]
        
        self.deadline_expired(context_msisdn)
        self.missing_data(context_msisdn)
        self.over_48_hours(context_msisdn)
        self.update_context_msisdn(context_msisdn.msisdn_reclamado, context_msisdn)

    def update_context_msisdn(self, msisdn_reclamado, context_msisdn):
        #redis
        redis_class = RedisConnection()
        redis_con = redis_class.connect()
        redis_obj = redis_con.hgetall(msisdn_reclamado)
 
        context_msisdn_j = context_msisdn.get_json()
        
        if redis_con.exists(msisdn_reclamado):
            #id da chamada anterior com o mesmo número reclamado
            context_msisdn.id_chamada_anterior = redis_obj["id_chamada"]

            #repetida somente quando for sobre o mesmo evento
            if context_msisdn.id_chamada_anterior is not '' and redis_con.exists(context_msisdn.id_chamada_anterior) and self.compare(redis_obj, context_msisdn_j,"id_evento"):
                context_msisdn.repetida = 'Y'
            
            #data promessa mudou/evento igual/registrar atendimento chamada anterior Y
            if self.compare(redis_obj, context_msisdn_j,"evento_datapromessa") is False:
                if self.compare(redis_obj, context_msisdn_j,"id_evento") and str(redis_con.hmget(redis_obj["id_chamada"], 'registrar_atendimento')[0]) == 'Y':
                    context_msisdn.reaprazado = 'Y'
                    redis_con.hset(msisdn_reclamado,'reaprazado',context_msisdn.reaprazado)                
                
        redis_con.hmset(msisdn_reclamado,context_msisdn.get_json())
        redis_con.expire(msisdn_reclamado, 259200)

    def compare(self, doc_redis, doc_context, param):
        return doc_redis[param] if param in doc_redis else '' == doc_context[param] if param in doc_context else ''
    

    def deadline_expired(self, context_msisdn):
        today = str(datetime.today().strftime('%d/%m/%Y %H:%M:%S'))        
        prazo_reparo = get_config_on_redis('prazo-reparo', context_msisdn.evento_tipo)
        
        if context_msisdn.evento_datapromessa and (datetime.strptime(context_msisdn.evento_datapromessa,'%d/%m/%Y %H:%M:%S') < datetime.strptime(today,'%d/%m/%Y %H:%M:%S')):
            ddd = context_msisdn.msisdn_reclamado[0]+context_msisdn.msisdn_reclamado[1]
            horas = int(prazo_reparo[ddd]) if ddd in prazo_reparo else int(prazo_reparo["default"])
            context_msisdn.evento_datapromessa = (datetime.today() + timedelta(hours=horas)).strftime('%d/%m/%Y %H:%M:%S')

    def missing_data(self, context_msisdn):
        if (not context_msisdn.evento_fixo or not context_msisdn.evento_velox or not context_msisdn.evento_datapromessa or not context_msisdn.msisdn_reclamado) or (context_msisdn.evento_fixo == "N" and context_msisdn.evento_velox == "N"):
            context_msisdn.faltando_dados = "Y"
        
    
    def over_48_hours(self, context_msisdn):
        max_date = str((datetime.today() + timedelta(hours=48)).strftime('%d/%m/%Y %H:%M:%S'))
        if context_msisdn.evento_datapromessa and (datetime.strptime(context_msisdn.evento_datapromessa,'%d/%m/%Y %H:%M:%S') > datetime.strptime(max_date,'%d/%m/%Y %H:%M:%S')):
            context_msisdn.data_maior_48hrs = "Y"




        