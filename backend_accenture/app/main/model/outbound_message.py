from datetime import datetime

class OutboundMessage(object):
    datetime_interacao: str
    request: str
    intent: str
    watson_confidence: str
    verbio_confidence: str
    intervalo_confianca: str    
    watson_response: str    
    etapa: str
    context: dict
    output_text: str
    conversation_id: str
    registrar_atendimento: str
    watson_times_response: dict
    flag_anatel: str

    def __init__(self):
        self.datetime_interacao = datetime.now().__format__("%Y-%m-%d %H:%M:%S")
        self.request = ''
        self.intent = ''
        self.watson_confidence = ''
        self.watson_times_response = ''
        self.verbio_confidence = ''
        self.intervalo_confianca = ''        
        self.watson_response = ''         
        self.etapa = ''
        self.output_text = ''
        self.conversation_id = ''
        self.registrar_atendimento = ''
        self.flag_anatel = ''        
    