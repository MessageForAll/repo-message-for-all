import json
import logging
from .model.redis_connection import RedisConnection

class Config_redis:       
    logger: logging.Logger

    @staticmethod
    def find_in_dict(self, path, key, default='Não entendi.'):
        redis = RedisConnection()
        redis_con = redis.connect()
        objeto = redis_con.hgetall(key)
        self.logger.debug(key)
        self.logger.debug(objeto)

        return objeto if objeto else default

    def find_repetida(self,msisdnreclamado):
        redis = RedisConnection()
        redis_con = redis.connect()
        
        reclamado = redis_con.scan_iter(match=msisdnreclamado)
        if not reclamado:
            return False
        else:
            print(reclamado)
            return True