import os
from os import listdir
import redis

from app.main.model.config_on_redis import set_config_on_redis
from app.main.model.redis_connection import RedisConnection

# Redis connection
redis_config = RedisConnection()
redis_cache = redis_config.connect()

config_path = 'app/main/config/cache/'
config_files = [f for f in listdir(config_path) if f.endswith('.json')]

set_config_on_redis(config_files)