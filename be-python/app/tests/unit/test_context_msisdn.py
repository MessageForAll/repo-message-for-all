import unittest

from app.main.model.context_msisdn import ContextMsisdn

class TestContextMsisdn(unittest.TestCase):
    context = ContextMsisdn()

    def setUp(self):
        self.context.repetida = 'Y'
        self.context.reaprazado = 'Y'
        self.context.prazo_vencido = 'Y'
        self.context.msisdn_reclamado = '1198909877'
        self.context.id_chamada = '001'
        self.context.protocolo = '1111111'
        self.context.cpf = '12334566578'

        self.context.id_evento = '0909090'
        self.context.evento_fixo = 'N'
        self.context.evento_velox = 'S'
        self.context.evento_velox_numero = '2020202020'
        self.context.evento_datapromessa = '18/08/2018 08:14:00'

    def test_get_json(self):
        self.assertEqual(self.context.get_json(), {'repetida': 'Y', 'reaprazado': 'Y', 'prazo_vencido': 'Y', 
                                                    'msisdn_reclamado': '1198909877', 'id_chamada': '001', 
                                                    'protocolo': '1111111', 'cpf': '12334566578', 'evento_fixo': 'N', 
                                                    'id_evento': '0909090', 'evento_velox': 'S', 'evento_datapromessa': '18/08/2018 08:14:00'})

