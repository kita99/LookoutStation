from passlib.hash import sha256_crypt
import json

from flask_cors import CORS
from flask import Response
from flask import request
from flask import Flask
import requests

from models import FeedEntry
from models import User
from models import Feed
import authentication
from models import db
from app import app

CORS(app)


@app.route('/test', methods=['GET'])
def test():
    auth = request.headers.get('Authorization')
    user = authentication.validate_token(auth)

    print(user.as_dict())
    return {'status': 200}


@app.route('/login', methods=['POST'])
def login():
    json_request = request.json

    username = json_request.get('username')
    unsecure_password = json_request.get('password')

    user = authentication.authenticate(username, unsecure_password)

    if user:
        return {'status': '200', 'token': authentication.generate_token(user.id)}

    return {'status': '401'}


@app.route('/register', methods=['POST'])
def register():
    json_request = request.json

    username = json_request.get('username')
    unsecure_password = json_request.get('password')

    if not username or not unsecure_password:
        return {'status': '400'}

    hashed_password = sha256_crypt.hash(unsecure_password)

    try:
        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        return {'status': '200'}
    except:
        db.session.rollback()
        return {'status': '500'}