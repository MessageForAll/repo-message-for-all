import os
from os import listdir
import unittest
import json
import threading

# TODO: Acretar migration, db, model
# from flask_migrate import Migrate, MigrateCommand
# from app.main.model import user, blacklist
from flask_script import Manager
from app import create_blueprint
from app.main import create_app  # , db
from app.main.config import Config
from app.main.model.config_on_redis import set_config_on_redis

app = create_app(os.getenv('PAV_OI_ENV') or 'dev')
blueprint = create_blueprint()
app.register_blueprint(blueprint)
app.app_context().push()
manager = Manager(app)

# TODO: Acretar migration, db, model
# migrate = Migrate(app, db)
#
# manager.add_command('db', MigrateCommand)

@manager.command
def run():
    port = Config.find_in_dict(["server", "port"])
    host = Config.find_in_dict(["server", "host"])
    env = os.getenv('PAV_OI_ENV') or 'dev'    
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":    
        load_cache()
    app.run(host=host, port=port)

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/tests/unit', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@app.before_first_request
def load_cache():
    # Subindo os arquivos de config para o Redis
    redis_cache = threading.Thread(target=set_config_on_redis,args=())
    redis_cache.start()    
    
if __name__ == '__main__':
    manager.run()
