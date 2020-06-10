from passlib.hash import sha256_crypt
import json

from flask_cors import CORS
from flask import Response
from flask import request
from flask import Flask
import requests

from models import User
from models import Scan
from models import Asset
from models import Software
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
        return {'status': 200, 'token': authentication.generate_token(user.id)}

    return {'status': 401}


@app.route('/register', methods=['POST'])
def register():
    json_request = request.json

    username = json_request.get('username')
    print(username)
    unsecure_password = json_request.get('password')
    email = json_request.get('email')

    if not username or not unsecure_password or not email:
        return {'status': 400}

    hashed_password = sha256_crypt.hash(unsecure_password)

    try:
        user = User(username=username, password=hashed_password, email=email)

        db.session.add(user)
        db.session.commit()

        return {'status': 200}
    except Exception as e:
        #logging.error(e)
        print(e)
        db.session.rollback()
        return {'status': 500}


@app.route('/users/emails', methods=['GET'])
def get_users_emails():
    json_request = request.json

    user = authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return Response('{"response": "Invalid User", "status": "False"}', status=401, mimetype='application/json')

    users = User.query.all()

    emails = []
    for user in users:
        emails.append(user.email)

    return {'status': 200, 'emails': emails}


@app.route('/assets/ips/public', methods=['GET'])
def get_public_ips():
    user = authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return Response('{"response": "Invalid User", "status": "False"}', status=401, mimetype='application/json')

    assets = Asset.query.all()

    ips = []

    for asset in assets:
        ips.append(asset.public_ip)

    return {'ips': ips}

@app.route('/assets', methods=['POST'])
def create_asset():
    json_request = request.json

    uuid = json_request.get('uuid')
    private_ip = json_request.get('private_ip')
    public_ip = json_request.get('public_ip')

    asset = Asset.query.filter_by(uuid=uuid).first()

    if asset:
        return Response('{"response": "Device already exists", "status": "False"}', status=200, mimetype='application/json')

    try:
        asset = Asset(
            uuid=uuid,
            private_ip=private_ip,
            public_ip=public_ip
        )

        db.session.add(asset)
        db.session.commit()

        return Response('{"response": "Added new device", "status": "True"}', status=201, mimetype='application/json')
    except:
        db.session.rollback()
        return Response('{"response": "Exception happened", "status": "False"}', status=500, mimetype='application/json')


@app.route('/assets/<uuid>', methods=['PUT'])
def update_asset(uuid):
    json_request = request.json
    software_list = json_request.get('software')

    asset = Asset.query.filter_by(uuid=uuid).first()

    print(asset)

    if not asset:
        return Response('{"response": "Invalid Device", "status": "False"}', status=404, mimetype='application/json')

    if not software_list:
        return Response('{"response": "Invalid data passed", "status": "False"}', status=400, mimetype='application/json')

    if not isinstance(software_list, list):
        return Response('{"response": "Invalid data passed", "status": "False"}', status=400, mimetype='application/json')

    try:
        for software in software_list:

            print(software)

            software_entry = Software(
                name=software['name'],
                version=software['version']
            )

            asset.software.append(software_entry)

        db.session.add(asset)
        db.session.commit()

        return Response('{"response": "Software inserted", "status": "True"}', status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(f'{"response": {e}, "status": "False"}', status=500, mimetype='application/json')


@app.route('/scans/<ip>', methods=['PUT'])
def add_scans(ip):
    json_request = request.json

    asset = Asset.query.filter_by(ip=ip).first()

    ports = request.json.get('ports')

    if not isinstance(ports, list):
        return {'status': 400}

    try:
        for port in ports:
            scan = Scan(
                port=port['id'],
                protocol=port['protocol'],
                service_name=port['service']['name'],
                state=port['state']['state'],
                state_reason=port['state']['reason']
            )

            asset.scans.append(scan)

        db.session.add(asset)
        db.session.commit()

        return Response('{"response": "Software inserted", "status": "True"}', status=200, mimetype='application/json')
    except:
        db.session.rollback()
        return Response('{"response": "Exception happened", "status": "False"}', status=500, mimetype='application/json')
