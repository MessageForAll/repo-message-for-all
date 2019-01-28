import os
import redis
import logging
from ..config import Config

class RedisConnection(object):
    redis_host: str
    redis_port: int
    redis_password: str
    env : str
    logger : logging.Logger

    def __init__(self):
        self.logger = logging.getLogger('redis')
        self.env = os.getenv('PAV_OI_ENV') or 'dev'

        self.redis_host = Config.find_in_dict(['redis-'+ self.env, 'host'])
        self.redis_port = Config.find_in_dict(['redis-'+ self.env, 'port'])
        self.redis_password = Config.find_in_dict(['redis-'+ self.env, 'password'])
        
    def connect(self):
        connection = redis.StrictRedis(host=self.redis_host, port=self.redis_port, 
                      password=self.redis_password, decode_responses=True)
        return connection