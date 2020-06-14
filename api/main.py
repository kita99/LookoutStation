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


@app.route('/login', methods=['POST'])
def login():
    json_request = request.json

    username = json_request.get('username')
    unsecure_password = json_request.get('password')

    user = authentication.authenticate(username, unsecure_password)

    if user:
        return {'token': authentication.generate_token(user.id)}

    return {'message': 'Authentication failure'}, 401


@app.route('/register', methods=['POST'])
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
        #logging.error(e)
        print(e)
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@app.route('/users/emails', methods=['GET'])
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


@app.route('/assets', methods=['GET'])
def get_all_assets():
    user = authentication.validate_token(request.headers.get('Authorization'))
    asset_list = []

    if not user:
        return {'message': 'Authentication failure'}, 401

    assets = Asset.query.all()

    for asset in assets:
        asset_list.append(asset.as_dict())

    return {'assets': asset_list}


@app.route('/assets/<uuid>', methods=['GET'])
def get_single_asset(uuid):
    user = authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure'}, 401

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    software = [software.as_dict() for software in asset.software] if asset.software else None

    return {'asset': {'software': software, **asset.as_dict()}}


@app.route('/assets/<uuid>/software', methods=['GET'])
def get_single_asset_software(uuid):
    user = authentication.validate_token(request.headers.get('Authorization'))
    software = []

    if not user:
        return {'message': 'Authentication failure'}, 401

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    if not asset.software:
        return {'message': 'This asset does not have any software associated'}, 404

    return {'software': [software.as_dict() for software in asset.software]}


@app.route('/assets/ips/public', methods=['GET'])
def get_all_assets_public_ips():
    user = authentication.validate_token(request.headers.get('Authorization'))
    ips = []

    if not user:
        return {'message': 'Authentication failure' }, 401

    assets = Asset.query.all()

    for asset in assets:
        ips.append(asset.public_ip)

    return {'ips': ips}


@app.route('/assets/<uuid>/ips/public', methods=['GET'])
def get_single_public_ip(uuid):
    user = authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure' }, 401

    asset = Asset.query.filter_by(uuid=device).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    return {'ip': asset.public_ip}


@app.route('/assets', methods=['POST'])
def create_asset():
    json_request = request.json

    uuid = json_request.get('uuid')
    hostname = json_request.get('hostname')
    operating_system = json_request.get('operating_system')
    private_ip = json_request.get('private_ip')
    public_ip = json_request.get('public_ip')

    asset = Asset.query.filter_by(uuid=uuid).first()

    if asset:
        return {'message': 'UUID already exists'}

    try:
        asset = Asset(
            uuid=uuid,
            hostname=hostname,
            private_ip=private_ip,
            public_ip=public_ip
        )

        db.session.add(asset)
        db.session.commit()

        return {'message': 'Asset registered successfully'}, 201
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@app.route('/assets/<uuid>', methods=['PUT'])
def update_asset(uuid):
    json_request = request.json
    software_list = json_request.get('software')

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    if not software_list:
        return {'message': 'One or more parameters missing'}, 400

    if not isinstance(software_list, list):
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        for software in software_list:
            software_entry = Software(
                name=software['name'],
                version=software['version']
            )

            asset.software.append(software_entry)

        db.session.add(asset)
        db.session.commit()

        return {'message': 'Asset updated successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@app.route('/scans/<public_ip>', methods=['PUT'])
def add_scans(public_ip):
    json_request = request.json
    ports = json_request.get('ports')

    if not isinstance(ports, list):
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        for port in ports:
            scan = Scan(
                public_ip=public_ip,
                port=port['id'],
                protocol=port['protocol'],
                service_name=port['service']['name'],
                state=port['state']['state'],
                state_reason=port['state']['reason']
            )

            db.session.add(scan)

        db.session.commit()

        return {'message': 'Scan data inserted successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
