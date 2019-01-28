import unittest

from app.main.service.oi.registro_chamada import OutputData
from app.main.model.redis_connection import RedisConnection

class TestRegistroChamada(unittest.TestCase):
    register = OutputData()
    redis = RedisConnection()
    redis_con = redis.connect()

    def setUp(self):
        class OutboundMessage(object):
            intent = 'teste'
        
        self.outbound_message = OutboundMessage()

    def test_create_intent_note(self):
        self.assertEqual(self.register.create_intent_note(self.outbound_message),'')
        self.outbound_message.intent = 'AmeacarAnatel'
        self.assertEqual(self.register.create_intent_note(self.outbound_message),"Cliente ameaÃ§ou recorrer juridicamente")

    def test_register_note(self):
        self.redis_con.hset("test_register_note", "etapa", "resultado teste 1")
        self.assertEqual(self.register.create_register_note("test_register_note", self.outbound_message), '')
        self.redis_con.hset("test_register_note", "etapa", "motivo_contato")
        self.assertEqual(self.register.create_register_note("test_register_note", self.outbound_message), "Aberto por Mari, atendente virtual. Cliente identificado, evento nÃ£o vocalizado.\n")

    def test_set_evento(self):
        self.redis_con.hset("test_registro_chamada", "evento_fixo", "Y")
        self.redis_con.hset("test_registro_chamada", "evento_velox", "N")
        self.assertEqual(self.register.set_evento("test_registro_chamada"), "Somente Fixo")
        self.redis_con.hset("test_registro_chamada", "evento_fixo", "N")
        self.redis_con.hset("test_registro_chamada", "evento_velox", "Y")
        self.assertEqual(self.register.set_evento("test_registro_chamada"), "Somente Velox")
        self.redis_con.hset("test_registro_chamada", "evento_fixo", "Y")
        self.redis_con.hset("test_registro_chamada", "evento_velox", "Y")
        self.assertEqual(self.register.set_evento("test_registro_chamada"), "Fixo e Velox")

    def test_set_prazo(self):
        self.redis_con.hset("test_registro_chamada", "prazo_vencido", "Y")
        self.assertEqual(self.register.set_prazo("test_registro_chamada"), "tipo-registro-prazo-fora")
        self.redis_con.hset("test_registro_chamada", "prazo_vencido", "")
        self.assertEqual(self.register.set_prazo("test_registro_chamada"), "tipo-registro-prazo-dentro")

    def test_set_tipo_registro(self):
        self.assertEqual(self.register.set_tipo_registro("test_registro_chamada"), "BDE")
        self.redis_con.hset("test_registro_chamada", "prazo_vencido", "Y")
        self.redis_con.hset("test_registro_chamada", "evento_fixo", "N")
        self.assertEqual(self.register.set_tipo_registro("test_registro_chamada"), "BD")

    

