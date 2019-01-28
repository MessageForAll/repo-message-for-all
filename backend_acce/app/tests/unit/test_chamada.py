import unittest

from app.main.model.chamada import Chamada

class TestChamada(unittest.TestCase):
    
    
    def setUp(self):
        class InboundMessage(object):
            session_verbio = 'teste_chamada'
            datetime_inicio = '2018-09-21-16:25:48'
            datetime_final = '201809201733'
            msisdn_reclamado = 'msisdnteste'
            retida = 'N'
            tempo_total = '007'
            msisdn_binado = 'binadoteste'
            nome_arquivo = 'arquivo_teste'

        class OutboundMessage(object):
            etapa = 'etapa_teste'
        
        self.inbound_message = InboundMessage()
        self.outbound_message = OutboundMessage()
        self.context_manager = ''
        self.chamada = Chamada(self.inbound_message, self.outbound_message, self.context_manager)


    def test_get_header(self):
        self.assertEqual(self.chamada.get_header(), {"session": "teste_chamada", "datetime-inicio": "2018-09-21-16:25:48",
                        "datetime-final": "201809201733", "msisdn-reclamado": "msisdnteste", "retida": "N", 
                        "tempo-total": "007", "ultima-etapa": "etapa_teste", "repetida": None, "reaprazada": None, 
                        "msisdn_binado": "binadoteste", "nome_arquivo": "arquivo_teste", "protocolo": None, "cpf": None})
    
    def test_save_chamada(self):
        self.assertEqual(self.chamada.save_chamada(), None)