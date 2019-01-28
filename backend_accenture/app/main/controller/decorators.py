from functools import wraps

from flask import request, Response

# TODO:
# from app.main.service.auth_helper import Auth

def check_headers(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        known_headers = ["msisdn-reclamado", "client-name", "protocolo"]
        if not all(header in request.headers for header in known_headers):
            response_object = {
                'status': 'fail',
                'message': 'missing headers'
            }

            return response_object, 400

        return f(*args, **kwargs)

    return decorated
        

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        # TODO: Validar Token
        # data, status = Auth.get_logged_in_user(request)
        # token = data.get('data')
        # 
        # if not token:
        #     return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        # TODO: Validar Token Admin
        # data, status = Auth.get_logged_in_user(request)
        # token = data.get('data')
        # 
        # if not token:
        #     return data, status
        # 
        # admin = token.get('admin')
        # if not admin:
        #     response_object = {
        #         'status': 'fail',
        #         'message': 'admin token required'
        #     }
        #     return response_object, 401

        return f(*args, **kwargs)

    return decorated
