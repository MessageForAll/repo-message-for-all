import json
from .chamada import Chamada
from .database_generic import DatabaseGeneric
from app.main.model.elastic_connection import ElasticConnection

class Interacao(Chamada):
    session: str
    datetime_interacao: str
    request: str
    intent: str
    watson_confidence: str    
    watson_response: str
    response: str    
    etapa: str
    intervalo_confianca: str
    datetime_interacao: str
    confidence_verbio: str
    output_text: str
    msisdn_binado: str
    timestamp: str

    def __init__(self, inbound_message, outbound_message, context):
        Chamada.__init__(self, inbound_message, outbound_message, context)      
        self.session = inbound_message.session_verbio
        self.request = inbound_message.user_message
        self.intent = outbound_message.intent
        self.etapa = outbound_message.etapa
        self.watson_response = outbound_message.watson_response
        self.output_text = outbound_message.output_text[len(outbound_message.output_text) - 1]        
        self.watson_confidence = outbound_message.watson_confidence
        self.confidence_verbio = inbound_message.confidence_verbio
        self.datetime_interacao = outbound_message.datetime_interacao
        self.intervalo_confianca = outbound_message.intervalo_confianca
        self.msisdn_binado = inbound_message.msisdn_binado
        self.timestamp = outbound_message.datetime_interacao

    def save(self):
        db = DatabaseGeneric()                
        collection = db.connect('chamada')

        interacao = {}
        interacao['session'] = str(self.session)
        interacao['datetime_interacao'] = str(self.datetime_interacao)
        interacao['request'] = str(self.request)
        interacao['intent'] = str(self.intent)
        interacao['etapa'] = str(self.etapa)        
        interacao['watson_response'] = str(self.watson_response)
        interacao['watson_confidence'] = str(self.watson_confidence)
        interacao['confidence_verbio'] = str(self.confidence_verbio)
        interacao['output_text'] = str(self.output_text)
        interacao['intervalo_confianca'] = str(self.intervalo_confianca)
        interacao['msisdn_binado'] = str(self.msisdn_binado)
        interacao['timestamp'] = str(self.timestamp)

        
        #Grava db
        collection.update({'session' : self.session},{'$push': {'interacoes': interacao}}, upsert = True)
                
        #Grava elastic
        ElasticConnection().save_interacao({'interacoes' : interacao})
