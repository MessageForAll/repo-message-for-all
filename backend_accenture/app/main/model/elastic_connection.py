import os
import logging
import requests
import json
from requests.auth import HTTPBasicAuth
from ..config import Config

class ElasticConnection(object):
    elastic_host: str
    elastic_port: int
    elastic_user: str
    elastic_password: str
    elastic_index : str
    env : str 
    logger : logging.Logger
    
    def __init__(self):
        self.env = os.getenv('PAV_OI_ENV') or 'dev'
        #elastic    
        self.elastic_host = Config.find_in_dict(['elastic-'+self.env, 'host'])
        self.elastic_port = Config.find_in_dict(['elastic-'+self.env, 'port'])
        self.elastic_user = Config.find_in_dict(['elastic-'+self.env, 'user'])
        self.elastic_password = Config.find_in_dict(['elastic-'+self.env, 'password'])
        self.elastic_index = Config.find_in_dict(['elastic-'+self.env, 'index'])

    def save_interacao(self,dados):   
        url = "http://" + self.elastic_host+':'+self.elastic_port+'/'+self.elastic_index+'/_doc/'
        user = self.elastic_user
        password = self.elastic_password
        
        auth_values = (user, password)
        headers = {'content-type': 'application/json'}

        requests.post(url, data=json.dumps(dados), auth=auth_values, headers=headers)

    def save_chamada(self,dados,session):
        url = "http://" + self.elastic_host+':'+self.elastic_port+'/'+self.elastic_index+'/_doc/'+session
        user = self.elastic_user
        password = self.elastic_password
        
        auth_values = (user, password)
        headers = {'content-type': 'application/json'}

        requests.post(url, data=json.dumps(dados), auth=auth_values, headers=headers)