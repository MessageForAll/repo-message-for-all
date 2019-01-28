import unittest

from app.main.model.context_chamada import ContextChamada

class TestContextChamada(unittest.TestCase):
    context = ContextChamada()    

    def setUp(self):
        self.context.conversation_id = '001'
        self.context.registrar_atendimento = 'Y'
        self.context.context_watson = {}
        self.context.flag_anatel = 'Y'
        self.context.etapa = 'teste'       

    def test_get_json(self):
        self.assertEqual(self.context.get_json(), {'conversation_id': '001', 'registrar_atendimento': 'Y', 
                                                            'context_watson': {}, 'flag_anatel': 'Y', 'etapa': 'teste'})
        self.context.conversation_id = '002'
        self.context.registrar_atendimento = 'Y'
        self.context.context_watson = {"chave_teste": "texto_teste"}
        self.context.flag_anatel = 'Y'
        self.context.etapa = 'teste2'         

        self.assertEqual(self.context.get_json(), {'conversation_id': '002', 'registrar_atendimento': 'Y', 
        'context_watson': {'chave_teste': 'texto_teste'}, 'flag_anatel': 'Y', 'etapa': 'teste2'})
    

