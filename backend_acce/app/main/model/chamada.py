import json
from .database_generic import DatabaseGeneric
from app.main.model.elastic_connection import ElasticConnection
from app.main.model.config_on_redis import hget_config_on_redis

class Chamada(object):    
    session: str
    datetime_inicio: str
    datetime_final: str
    retida: str
    tempo_total: int
    ultima_etapa: str
    nome_arquivo: str
    repetida: str
    reaprazada: str
    msisdn_reclamado: str
    msisdn_binado: str
    protocolo: str
    cpf: str
    nome_reclamante: str
    timestamp: str

    def __init__(self, inbound_message, outbound_message, context_manager):                   
        self.session = inbound_message.session_verbio
        self.datetime_inicio = context_manager.datetime_inicio
        self.datetime_final = context_manager.datetime_final
        self.msisdn_reclamado = inbound_message.msisdn_reclamado
        self.retida = inbound_message.retida
        self.tempo_total = context_manager.tempo_total
        self.ultima_etapa = outbound_message.etapa
        self.repetida = hget_config_on_redis(self.msisdn_reclamado, "repetida")
        self.msisdn_binado = inbound_message.msisdn_binado
        self.nome_arquivo = inbound_message.nome_arquivo
        self.reaprazada = hget_config_on_redis(self.msisdn_reclamado, "reaprazada")
        self.protocolo = hget_config_on_redis(self.msisdn_reclamado, "protocolo")
        self.cpf = hget_config_on_redis(self.msisdn_reclamado, "cpf")
        self.nome_reclamante = hget_config_on_redis(self.session, "nome_reclamante")
        self.timestamp = self.datetime_inicio
        
        self.save_chamada()
    
    def save_chamada(self):
        #Grava db
        db = DatabaseGeneric()                
        collection = db.connect('chamada')
        collection.update({'session':self.session},{'$set': self.get_header()}, upsert = True)        
        
        #Grava elastic
        ElasticConnection().save_chamada({'chamada' : self.get_header()}, self.session)

    def get_header(self):
        data = {}
        data['session'] = self.session
        data['datetime-inicio'] = self.datetime_inicio
        data['datetime-final'] = self.datetime_final
        data['msisdn-reclamado'] = self.msisdn_reclamado
        data['retida'] = self.retida
        data['tempo-total'] = self.tempo_total
        data['ultima-etapa'] = self.ultima_etapa
        data['repetida'] = self.repetida
        data['reaprazada'] = self.reaprazada
        data['msisdn_binado'] = self.msisdn_binado
        data['nome_arquivo'] = self.nome_arquivo
        data['protocolo'] = self.protocolo
        data['cpf'] = self.cpf
        data['nome_reclamante'] = self.nome_reclamante
        data['timestamp'] = self.timestamp

        return data