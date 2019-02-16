# TODO: verificar sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from logging.config import fileConfig
import configparser
import os
import errno
import json

from .config import Config
from .model.redis_connection import RedisConnection

# TODO: BCrypt e db
# db = SQLAlchemy()
# flask_bcrypt = Bcrypt()

def create_app(config_name):
    check_config_file()

    flask_config = Config.get_flask_config(config_name)
    app = Flask(__name__)
    app.config.from_object(flask_config)
    # TODO: db -> db.init_app(app)
    # TODO: Configurar bcrypt
    # flask_bcrypt.init_app(app)

    return app

def check_config_file():
    env = os.getenv('PAV_OI_ENV') or 'dev'
    base_path = 'app/main/config/'
    #log_file_config = base_path + Config.find_in_dict(['log-config-file-' + env], 'log-config.ini')    
    #log_file_config = base_path + general_config['log-config-file-' + env]
    log_file_config = base_path+'log-config-'+env+'.ini'

    config = configparser.ConfigParser()
    config.read(log_file_config)
    log_file_name = config.get('handler_file_handler', 'args')
    log_file_name = log_file_name.split(',')[0][1:].replace("'", "")
    check_log_file(log_file_name)

    try:
        fileConfig(log_file_config)
    except:
        print("Invalid logging config file [" + log_file_config + "]")


def check_log_file(filename):
    if os.path.isfile(filename):
        return

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    open(filename, "w").close()