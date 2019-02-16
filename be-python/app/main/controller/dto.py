from flask_restplus import Namespace, fields

# TODO: Acertar api.model
class DialogDto:
    api = Namespace('dialog', description='dialog operations', path="/dialog")
    # TODO: Mapear resposta por aqui
    dialog = api.model('dialog', {})
