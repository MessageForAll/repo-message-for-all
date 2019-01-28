from flask_restplus import Api
from flask import Blueprint
from flask_restplus import Resource, Api

from .main.controller.dialog_controller import api as dialog_ns

def create_blueprint():
    blueprint = Blueprint('api', __name__)

    api = Api(blueprint,
            title='PA Virtual Dialogs',
            version='1.0',
            description='Oi - PA Virtual client dialogs'
            )

    # TODO: Verificar se vamos manter esse path /client/dialog
    api.add_namespace(dialog_ns, path='/client')

    return blueprint
