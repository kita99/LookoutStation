import datetime
from passlib.hash import sha256_crypt

import jwt

from models import User
import settings


def generate_token(user_id):
    return jwt.encode(
        {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
        },
        settings.JWT_SECRET,
        algorithm='HS256').decode('utf-8')


def validate_token(encoded_jwt):
    try:
        decoded = jwt.decode(encoded_jwt, settings.JWT_SECRET, algorithms=['HS256'])

        return User.query.get(decoded.get('user_id'))
    except:
        return False


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()

    if sha256_crypt.verify(password, user.password):
        return user

    return False
