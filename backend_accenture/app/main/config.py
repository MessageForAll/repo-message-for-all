import json
import sys
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig():
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    # TODO: Acertar db
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig():
    DEBUG = True
    TESTING = True
    # TODO: Acertar db
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig():
    # TODO: colocar debug false
    DEBUG = True
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


class Config:
    __flask_config__ = dict(
        dev=DevelopmentConfig,
        test=TestingConfig,
        prod=ProductionConfig
    )
    __value__ = None
    # TODO: Validar secret key - NÃO DEVE FICAR COMO VARIÁVEL DE AMBIENTE
    SECRET_KEY = os.getenv('SECRET_KEY', '')

    @staticmethod
    def value(force=False):
        # Se já tiver carregado as configurações, mantém o da memória
        if not force and Config.__value__ is not None:
            return Config.__value__

        # verifica se tem parâmetro de arquivo de configuração
        base_path = 'app/main/config/'
        config_file = base_path + Config.__get_arg__('-conf', 'general.json')

        # Carrega configurações dos arquivos
        with open(config_file) as data_file:
            data = json.load(data_file)
            new_config_value = data
        if new_config_value.__contains__('subfiles'):
            for file in new_config_value['subfiles']:
                with open(file) as data_file:
                    data = json.load(data_file)
                    new_config_value = {**new_config_value, **data}
        Config.__value__ = new_config_value

        return Config.__value__

    @staticmethod
    def find_in_dict(path: list, default=None):
        full_dic = Config.value()
        ret = Config.__find__(root=full_dic, path=path, default=default)
        return ret

    @staticmethod
    def get_flask_config(name: str):
        return Config.__flask_config__[name]

    @staticmethod
    def get_intents_default_utter(intent: str, default_utter: str):
        resp = Config.find_in_dict(['intent-confirmation', intent], default_utter)
        
        # faz uma segunda validação pois caso a intent exista mas esteja vazia ele não pega o default no passo anterior
        resp = resp if resp else default_utter

        return resp

    @staticmethod
    def __find__(root: dict, path: list, default=None):
        """
        Procura um valor no dicionário, se não existir o caminho, traz um valor padrão
        :param root: Raiz do dicionário
        :param path: Caminho
        :param default: Valor padrão
        :return:
        """
        rv = root
        try:
            for key in path:
                rv = rv[key]
        except:
            return default
        return rv

    @staticmethod
    def __get_arg__(arg: str, default: str = ""):
        """
        Busca valores de uma linha de comando. Se não existir, retorna padrão
        :param arg:
        :param default:
        :return:
        """
        try:
            argposition = sys.argv.index(arg)
            ret = sys.argv[argposition + 1]
        except BaseException:
            ret = default

        return ret

key = Config.SECRET_KEY
