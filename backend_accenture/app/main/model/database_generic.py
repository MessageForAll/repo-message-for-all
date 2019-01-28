import pymongo
import os
import logging
from app.main.config import Config
from app.main.model.outbound_message import OutboundMessage
from app.main.model.config_on_redis import get_config_on_redis


class DatabaseGeneric(object):    
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    env : str
    logger : logging.Logger

    def __init__(self):
        self.logger = logging.getLogger('mongo')
        self.env = os.getenv('PAV_OI_ENV') or 'dev'
        # Mongo connection
        self.db_host = Config.find_in_dict(['mongo-'+self.env, 'host'])
        self.db_port = Config.find_in_dict(['mongo-'+self.env, 'port'])
        self.db_user = Config.find_in_dict(['mongo-'+self.env, 'user'])
        self.db_name = Config.find_in_dict(['mongo-'+self.env, 'dbname'])
        self.db_password = Config.find_in_dict(['mongo-'+self.env, 'password'])               

    def connect(self,collection):
                                      
        try:
            connection = pymongo.MongoClient(self.db_host, username=self.db_user, password=self.db_password)
            db = connection[self.db_name]
            collection = db[collection]                                                                              

        except BaseException:            
            raise KeyError(get_config_on_redis('mensage-category', 'error_connect'))

        return collection

      
    