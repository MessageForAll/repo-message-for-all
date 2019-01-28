import unittest

import app.main.model.config_on_redis as config_redis

class TesteConfigOnRedis(unittest.TestCase):


    def test_get_config_on_redis(self):
        chave = 'contador'
        field = 'silencio'
        self.assertEqual(config_redis.get_config_on_redis(chave, field), 2)
        chave = 'etapa-valida'
        field = 'evento'
        self.assertEqual(config_redis.get_config_on_redis(chave, field), 'Y')
        chave = 'regiao-cliente'
        field = '89'
        self.assertEqual(config_redis.get_config_on_redis(chave, field), 'R1')
        chave = 'teste4'
        field = 'teste4'
        self.assertEqual(config_redis.get_config_on_redis(chave, field), None)

    def test_get_list_on_redis(self):
        chave = 'contador'
        self.assertEqual(config_redis.get_list_on_redis(chave), {"silencio":2,"improperio":2,"pede-repetir":2,
                                                                "repetir":2,"chamada-repetida":24,"descricao-evento":2})
        chave = 'intent-confidence'
        self.assertEqual(config_redis.get_list_on_redis(chave), {"ask-confirmation": 0.6,"misunderstood": 0.4})
        chave = 'tipo-registro-prazo-dentro'
        self.assertEqual(config_redis.get_list_on_redis(chave), {"Somente Fixo":"BDE","Somente Velox":"BTE",
                                                            "Fixo e Velox":"BDE", "Fixo com impacto no Velox":"BDE"})
        chave = 'teste3'
        self.assertEqual(config_redis.get_list_on_redis(chave), {})

    def test_set_list_on_redis(self):
        chave = "teste 1"
        lista = {"msg": "hello", "msg2": "world"}
        self.assertEqual(config_redis.set_list_on_redis(chave, lista), True)
        #TODO: ver como testar um caso que vai dar errado

    def test_hget_config_on_redis(self):
        chave = 'teste1'
        field = 'teste1'
        self.assertEqual(config_redis.hget_config_on_redis(chave, field), None)
        chave = 'teste2'
        field = 'teste2'
        self.assertEqual(config_redis.hget_config_on_redis(chave, field), None)

    def test_set_config_on_redis(self):
        config_redis.set_config_on_redis()
        self.assertEqual(config_redis.redis_cache.get('contador'), '{"silencio": 2, "improperio": 2, "pede-repetir": 2, "repetir": 2, "chamada-repetida": 24, "descricao-evento": 2}')

    def test_update_config_on_redis(self):
        config_redis.update_config_on_redis('etapa-valida.json')
        self.assertEqual(config_redis.redis_cache.get('etapa-valida'), '{"evento": "Y", "instrucoes_finais": "Y", "hang-up": "Y", "transferir_atendente": "Y"}')


    


        
