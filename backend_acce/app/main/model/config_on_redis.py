import os
from os import listdir
from os.path import isfile, join
import redis
import json
from .redis_connection import RedisConnection

# Redis connection
redis_config = RedisConnection()
redis_cache = redis_config.connect()

def set_config_on_redis(config_files = None):
    if config_files is None:
        config_path = 'app/main/config/cache/'
        config_files = [f for f in listdir(config_path) if f.endswith('.json')]        
    
    if config_files:
        for file in config_files:
            config_file = file
            config_file_name = os.path.splitext(config_file)[0]
            with open(config_path+config_file) as data_file:
                file_with_config = json.dumps(json.load((data_file)))
                redis_cache.set(config_file_name, file_with_config)

def update_config_on_redis(config_file_name):
    update_path = 'app/main/config/cache/'
    update_file = config_file_name
    update_file_name = os.path.splitext(config_file_name)[0]
    with open(update_path+update_file) as data_file:
        update_config = json.dumps(json.load((data_file)))
        redis_cache.set(update_file_name, update_config)

#_list = Nome da lista, Key = Chave a ser localizada, Retorna valor da chave.
def get_config_on_redis(key,field,default = None):    
       _list = json.loads(redis_cache.get(key)) if redis_cache.get(key) else {}             
       return _list[str(field)] if str(field) in _list else default

#_list = Nome da lista, Key = Chave a ser localizada, Retorna valor da chave.
def hget_config_on_redis(key,field,default = None):    
       _list = redis_cache.hgetall(key) if redis_cache.hgetall(key) else {}             
       return _list[str(field)] if str(field) in _list else default

# Retorna uma lista baseado na chave
def get_list_on_redis(key,default = None):
    _list = json.loads(redis_cache.get(key)) if redis_cache.get(key) else {}
    return _list

def set_list_on_redis(key,_list):
    res = redis_cache.hmset(key,_list)
    return res