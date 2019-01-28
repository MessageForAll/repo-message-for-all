
class ContextChamada():

    conversation_id: str
    registrar_atendimento: str
    context_watson: dict
    flag_anatel: str
    etapa: str
    datetime_inicio: str
    datetime_final: str
    tempo_total : str
    
    def __init__(self):
        self.conversation_id = ""
        self.registrar_atendimento = ""
        self.context_watson = ""
        self.flag_anatel = ""
        self.etapa = ""        
        self.datetime_inicio = ""
        self.datetime_final = ""
        self.tempo_total = ""

    def get_json(self):
        context_chamada_j = {}
        context_chamada_j["conversation_id"] = self.conversation_id
        context_chamada_j["registrar_atendimento"] = self.registrar_atendimento
        context_chamada_j["context_watson"] = self.context_watson
        context_chamada_j["flag_anatel"] = self.flag_anatel
        context_chamada_j["etapa"] = self.etapa
        context_chamada_j["datetime_inicio"] = self.datetime_inicio
        context_chamada_j["datetime_final"] = self.datetime_final
        context_chamada_j["tempo_total"] = self.tempo_total

        return context_chamada_j