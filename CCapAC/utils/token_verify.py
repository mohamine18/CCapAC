from flask import session, jsonify, request, app
from functools import wraps
import jwt
from CCapAC.admin import app


def token_verify(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'message': 'Missing authentication'}), 403
        token = session['username']
        if not token:
            return jsonify({'message': 'Missing token'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return wrapped