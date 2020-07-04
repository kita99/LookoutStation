from passlib.hash import sha256_crypt
from flask import Blueprint
from flask import request

from lookoutstation.helpers import authentication
from lookoutstation.models import User
from lookoutstation.app import db


users = Blueprint('users', __name__)


@users.route('/login', methods=['POST'])
def login():
    json_request = request.json

    username = json_request.get('username')
    unsecure_password = json_request.get('password')

    user = authentication.authenticate(username, unsecure_password)

    if user:
        return {'token': authentication.generate_token(user.id)}

    return {'message': 'Authentication failure'}, 401


@users.route('/register', methods=['POST'])
def register():
    json_request = request.json

    username = json_request.get('username')
    email = json_request.get('email')
    unsecure_password = json_request.get('password')

    if not username or not unsecure_password or not email:
        return {'message': 'Authentication failure'}, 401

    hashed_password = sha256_crypt.hash(unsecure_password)

    try:
        user = User(username=username, password=hashed_password, email=email)

        db.session.add(user)
        db.session.commit()

        return {'message': 'Registration successful'}, 201
    except Exception as e:
        # logging.error(e)
        print(e)
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@users.route('/users/emails', methods=['GET'])
def get_users_emails():
    json_request = request.json

    user = authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure'}, 401

    users = User.query.all()

    emails = []
    for user in users:
        emails.append(user.email)

    return {'emails': emails}
