from datetime import datetime

class InboundMessage(object):
    #TODO: deletar tres próximos e suas referencias
    user_message: str
    confidence_verbio: str
    watson_conversation_id: str

    session_verbio: str
    datetime_inicio: str
    datetime_final: str
    tempo_total: int
    ultima_etapa: str    
    msisdn_reclamado: str
    retida: str
    nome_arquivo: str
    msisdn_binado: str

    # { "request": {"session": "atma00", "transcript":"ola", "confidence":0.7, "datetime_inicio": "2018-09-21-16:25:48",
    #                                                     "datetime_final": "2018-31-09:18:15", "msisdn-reclamado":"011998765432" } }
    def __init__(self, request:dict = None):
        """
        Cria o InboundMessage baseado no request
        """
        if not request:
            return

        try:
            self.session_verbio = request["request"]["session"]
            self.user_message = request["request"]["transcript"]
            self.confidence_verbio = request["request"]["confidence"]

            self.session_verbio = request["request"]["session"]
            self.msisdn_reclamado = request["request"]["msisdn-reclamado"]
            self.nome_arquivo = ''
            self.msisdn_binado = request["request"]["msisdn-reclamado"]
            #request["request"]["nome_arquivo"] if request["request"]["nome_arquivo"] else ''

            # TODO: default true, implementar mudança when false
            self.retida = 'true'

        except BaseException:
            raise KeyError('''Chamada inválida

            Os seguintes parâmetros são necessários para o método POST:
            session, transcript, confidence''')


