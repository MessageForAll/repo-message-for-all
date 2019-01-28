import logging
import re
import json
import os
from datetime import datetime, timedelta

from ..config import Config
from ..config_redis import Config_redis
from app.main.model.config_on_redis import get_config_on_redis, hget_config_on_redis

    
class VerbioResponse(object):
    logger: logging.Logger
    transfer_to: str
    response_audio: list

    def __init__(self):
        self.logger = logging.getLogger('funcional')
        self.transfer_to = "10331"
        self.response_audio = []


    def construct_response(self, outbound_message, msisdn_reclamado):
        text_output = outbound_message.output_text[len(outbound_message.output_text) - 1]
        watson_transcript_audios = text_output.split("|")
        transcript = watson_transcript_audios[0]
        split_audios = watson_transcript_audios[1:]

        if hget_config_on_redis(msisdn_reclamado, "faltando_dados") == "Y" or hget_config_on_redis(msisdn_reclamado, "data_maior_48hrs") == "Y":
            self.response_audio = [{"type": "tts", "transcript": "Tive dificuldade em encontrar seus dados, vou transferir para outro atendente para que ele possa te atender melhor.", "id": "ID_11_1"}]
            self.logger.info("[%s] Ligação transferida para atendente, não achamos as informações de terminal reclamado, data promessa ou tipo de evento ou o prazo de normalização é maior que 48 horas.", outbound_message.conversation_id)
            return self.response_audio, transcript

        if len(watson_transcript_audios) == 1:
            self.logger.info("[%s] Os IDs dos áudios não foram informados, a resposta será passada em tts", outbound_message.conversation_id) 
            transcript = self.replace_variables_transcript(transcript, msisdn_reclamado, outbound_message)
            self.response_audio = [{"type": "tts", "transcript": transcript, "id": "ID_11_1"}] 
        else:
            i = 0
            while i < len(split_audios):
                audio_id = split_audios[i]
                i += 1

                if audio_id not in ['telefone', 'protocolo', 'data_normalizacao', 'hora_normalizacao']:                
                    self.response_audio.append({"type": "recording", "transcript": "", "id": audio_id})         

                elif audio_id in ['telefone', 'protocolo', 'data_normalizacao', 'hora_normalizacao']:
                    self.replace_variables(audio_id, msisdn_reclamado)

                else:
                    transcript = self.replace_variables_transcript(transcript, msisdn_reclamado, outbound_message)
                    self.response_audio = [{"type": "tts", "transcript": transcript, "id": "ID_11_1"}] 
                    self.logger.info("[%s] VERBIO RESPONSE: A variável informada não pôde ser encontrada.", outbound_message.conversation_id)
                    break

        return self.response_audio, transcript
    
### FUNÇÕES PARA TRATAR AS VARIÁVEIS

    def replace_variables(self, audio_id, msisdn_reclamado):
        data = hget_config_on_redis(msisdn_reclamado, 'evento_datapromessa')
        entire_date = data.split()[0]
        entire_date = datetime.strptime(entire_date,'%d/%m/%Y')
        tomorrow = datetime.today() + timedelta(days=1)
        if audio_id == 'telefone':
            telefone = hget_config_on_redis(msisdn_reclamado, 'msisdn_reclamado') 
            self.phone_audios(telefone)
            
        elif audio_id == 'protocolo':
            protocolo = hget_config_on_redis(msisdn_reclamado, 'protocolo') 
            self.protocolo_audios(protocolo)
            
        elif audio_id == 'data_normalizacao':
            if entire_date > tomorrow:
                return self.response_audio
            else:
                self.date_audios(data)
        
        elif audio_id == 'hora_normalizacao':
            if entire_date > tomorrow:
                return self.date_audios(data)
            else:
                self.hour_audios(data)
                
        return self.response_audio

    def replace_variables_transcript(self, transcript, msisdn_reclamado, outbound_message):
        #TODO: adicionar variáveis conforme forem identificadas
        data_evento = hget_config_on_redis(msisdn_reclamado, 'evento_datapromessa').split()
        data_normalizacao = data_evento[0]
        hora_evento = data_evento[1][:5]
        transcript = transcript.replace("<telefone>", hget_config_on_redis(msisdn_reclamado, 'msisdn_reclamado'))
        transcript = transcript.replace("<protocolo>", hget_config_on_redis(msisdn_reclamado, 'protocolo'))
        transcript = transcript.replace("<data_normalizacao>", data_normalizacao)
        transcript = transcript.replace("<hora_normalizacao>", hora_evento)
        if ('<' or '>') in transcript:
            self.logger.info("[%s] VERBIO RESPONSE: O input:'"+transcript+"' retornou variáveis que não foram identificadas.", outbound_message.conversation_id) 
            transcript = 'Não entendi, você pode repetir?|EntendParcial_Excecao_PodeRepetir' #TODO: verificar como tratar
        return transcript
    

    def phone_audios(self, phone):
        phone = list(map(int, phone))
        phone_size = len(phone)
        ddd_phone = str(phone[0])+str(phone[1])
        if phone_size == 10:
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": ddd_phone, "id": ddd_phone+"_NF"})
            self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[2]), "id": str(phone[2])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[3]), "id": str(phone[3])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[4]), "id": str(phone[4])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[5]), "id": str(phone[5])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[6]), "id": str(phone[6])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[7]), "id": str(phone[7])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[8]), "id": str(phone[8])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[9]), "id": str(phone[9])+"_F" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
        else:
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": ddd_phone, "id": ddd_phone+"_NF"})
            self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[2]), "id": str(phone[2])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[3]), "id": str(phone[3])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[4]), "id": str(phone[4])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[5]), "id": str(phone[5])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[6]), "id": str(phone[6])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[7]), "id": str(phone[7])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[8]), "id": str(phone[8])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            self.response_audio.append({"type": "recording", "transcript": str(phone[9]), "id": str(phone[9])+"_NF" })
            self.response_audio.append({"type": "recording", "transcript": str(phone[10]), "id": str(phone[10])+"_F" })
            self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})    

        return self.response_audio

    def protocolo_audios(self, protocolo):
        protocolo_size = len(protocolo)
        year = protocolo[:4]
        self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
        self.response_audio.append({"type": "recording", "transcript": year, "id": "P_"+year+"_NF"})
        i = 4
        numbers = []
        while i < protocolo_size:
            number = protocolo[i]+protocolo[i+1]
            numbers.append(number)
            i += 2

        index = 0
        while index < len(numbers):
            if index == int(len(numbers)) - 1:
                self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
                self.response_audio.append({"type": "recording", "transcript": numbers[index], "id": "P_"+numbers[index]+"_F"})
                self.response_audio.append({"type": "recording", "transcript": "250_Milissegundos", "id": '250_Milissegundos'})
            else:
                self.response_audio.append({"type": "recording", "transcript": "500_Milissegundos", "id": '500_Milissegundos'})
                self.response_audio.append({"type": "recording", "transcript": numbers[index], "id": "P_"+numbers[index]+"_NF"})
            index += 1

        return self.response_audio

    def date_audios(self, date):
        entire_date = date.split()[0]
        split_date = entire_date.split("/")
        day_month = split_date[0]+split_date[1]
        year = split_date[2][2:]
        today = str(datetime.today().strftime('%d/%m/%Y'))
        tomorrow = str((datetime.today() + timedelta(days=1)).strftime('%d/%m/%Y'))

        if entire_date == today:
            self.response_audio.append({"type": "recording", "trancript": "hoje", "id": "Hoje_F"}) 
        elif entire_date == tomorrow:
            self.response_audio.append({"type": "recording", "trancript": "amanhã", "id": "Amanha_F"}) 
        else:
            self.response_audio.append({"type": "recording", "trancript": "48 horas", "id": "48_Horas_F"}) 
    
        return self.response_audio

    def hour_audios(self, date):
        entire_hour = date.strip().split()[1]
        split_hour = entire_hour.split(":")
        hour = split_hour[0]
        minuts = split_hour[1]

        if minuts == '00':
            self.response_audio.append({"type": "recording", "transcript": hour, "id": "Hora_"+minuts+hour+"_F"})
        else:
            if '00' < hour < '12':
                self.response_audio.append({"type": "recording", "transcript": hour, "id": "Hora_"+hour+"_NF"})
                self.response_audio.append({"type": "recording", "transcript": minuts, "id": "Minuto_"+minuts+"_F"})
                self.response_audio.append({"type": "recording", "transcript": "da manhã", "id": "Da_Manha_F"})
            else:
                self.response_audio.append({"type": "recording", "transcript": hour, "id": "Hora_"+hour+"_NF"})
                self.response_audio.append({"type": "recording", "transcript": minuts, "id": "Minuto_"+minuts+"_F"})

        return self.response_audio

### REGRAS DE TRANSFERÊNCIA
    def get_region(self, phone):
        phone_region = phone[0]+phone[1]
        region = get_config_on_redis('regiao-cliente', phone_region)
        return region
    
    def transfer_sector(self, outbound_message, phone_number):
        region = self.get_region(phone_number)
        region_transfer = get_config_on_redis('setor-transferencia', region)
        if outbound_message.intent == "CancelarLinhaOuProduto":
            transfer_sector = region_transfer['CancelarLinhaOuProduto']
        elif outbound_message.intent == "QuestionarConta": #TODO: verificar como identificar questionarconta
            transfer_sector = region_transfer['QuestionarConta']
        else:
            transfer_sector = region_transfer['Default']
        return transfer_sector

    def next_step(self, outbound_message, msisdn_reclamado):
        #TODO: ajustar esse if
        if outbound_message.etapa == 'transferir_atendente' or (outbound_message.intent == 'SolicitarProtocolo' and not hget_config_on_redis(msisdn_reclamado, 'protocolo')) or hget_config_on_redis(msisdn_reclamado, "faltando_dados") == "Y" or hget_config_on_redis(msisdn_reclamado, "data_maior_48hrs") == "Y":
            action = 'transfer' 
        elif outbound_message.etapa == 'hang-up': 
            action = 'hangup'
        else:
            action = 'ask'
        return action