from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def ops_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get('is_ops_user', False):
            return jsonify({'message': 'Ops user only'}), 403
        return fn(*args, **kwargs)
    return wrapper

def client_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get('is_ops_user', False):
            return jsonify({'message': 'Client user only'}), 403
        return fn(*args, **kwargs)
    return wrapper