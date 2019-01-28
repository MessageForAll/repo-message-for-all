import json

class ContextMsisdn():

    repetida: str
    reaprazado: str
    prazo_vencido: str
    msisdn_reclamado: str
    id_chamada: str
    id_chamada_anterior: str
    protocolo: str
    cpf: str

    evento_fixo: str
    evento_fixo_numero: str
    evento_fixo_datapromessa: str
    evento_fixo_tipo_evento: str
    evento_velox: str
    evento_velox_numero: str
    evento_velox_datapromessa: str
    evento_velox_tipo_evento: str
    evento_tipo: str
    data_maior_48hrs: str
    faltando_dados: str
    
    def __init__(self):
        self.repetida = 'N'
        self.reaprazado = 'N'
        self.prazo_vencido = 'N'
        self.msisdn_reclamado = ''
        self.id_chamada = ''
        self.id_chamada_anterior = ''
        self.protocolo = ''
        self.cpf = ''

        self.id_evento = ''        
        self.evento_fixo = 'N'
        self.evento_fixo_tipo_evento = ''
        self.evento_velox = 'N'
        self.evento_velox_numero = ''
        self.evento_velox_tipo_evento = ''
        self.evento_datapromessa = ''
        self.evento_tipo = ''
        self.data_maior_48hrs = 'N'
        self.faltando_dados = ''
        
    def get_json(self):
        context_msisdn_j = {}
        context_msisdn_j["repetida"] = str(self.repetida)
        context_msisdn_j["reaprazado"] = str(self.reaprazado)
        context_msisdn_j["prazo_vencido"] = str(self.prazo_vencido)
        context_msisdn_j["msisdn_reclamado"] = str(self.msisdn_reclamado)
        context_msisdn_j["id_chamada"] = str(self.id_chamada)
        context_msisdn_j["id_chamada_anterior"] = str(self.id_chamada_anterior)
        context_msisdn_j["protocolo"] = str(self.protocolo)
        context_msisdn_j["cpf"] = str(self.cpf)

        context_msisdn_j["evento_fixo"] = str(self.evento_fixo)
        context_msisdn_j["id_evento"] = str(self.id_evento)
        context_msisdn_j["evento_fixo_tipo_evento"] = str(self.evento_fixo_tipo_evento)
        context_msisdn_j["evento_velox"] = str(self.evento_velox)
        context_msisdn_j["evento_datapromessa"] = str(self.evento_datapromessa)
        context_msisdn_j["evento_velox_tipo_evento"] = str(self.evento_velox_tipo_evento)
        context_msisdn_j["evento_tipo"] = str(self.evento_tipo)
        context_msisdn_j["data_maior_48hrs"] = str(self.data_maior_48hrs) 
        context_msisdn_j["faltando_dados"] = str(self.faltando_dados)      

        return context_msisdn_j