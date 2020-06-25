from flask import Blueprint
from flask import request

from lookoutstation import helpers
from lookoutstation.models import Software
from lookoutstation.models import Asset
from lookoutstation.models import CPE
from lookoutstation.app import db


assets = Blueprint('assets', __name__)


@assets.route('', methods=['GET'])
def get_all_assets():
    user = helpers.authentication.validate_token(request.headers.get('Authorization'))
    asset_list = []

    if not user:
        return {'message': 'Authentication failure'}, 401

    assets = Asset.query.all()

    for asset in assets:
        asset_list.append(asset.as_dict())

    return {'assets': asset_list}


@assets.route('/<uuid>', methods=['GET'])
def get_single_asset(uuid):
    user = helpers.authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure'}, 401

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    software = [software.as_dict() for software in asset.software] if asset.software else None

    return {'asset': {'software': software, **asset.as_dict()}}


@assets.route('/<uuid>/software', methods=['GET'])
def get_single_asset_software(uuid):
    user = helpers.authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure'}, 401

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    if not asset.software:
        return {'message': 'This asset does not have any software associated'}, 404

    return {'software': [software.as_dict() for software in asset.software]}


@assets.route('/ips/public', methods=['GET'])
def get_all_assets_public_ips():
    user = helpers.uthentication.validate_token(request.headers.get('Authorization'))
    ips = []

    if not user:
        return {'message': 'Authentication failure'}, 401

    assets = Asset.query.all()

    for asset in assets:
        ips.append(asset.public_ip)

    return {'ips': ips}


@assets.route('/<uuid>/ips/public', methods=['GET'])
def get_single_public_ip(uuid):
    user = helpers.authentication.validate_token(request.headers.get('Authorization'))

    if not user:
        return {'message': 'Authentication failure'}, 401

    asset = Asset.query.filter_by(uuid=uuid).first()

    if not asset:
        return {'message': 'Asset with specified UUID does not exist'}, 404

    return {'ip': asset.public_ip}


@assets.route('/', methods=['POST'])
def create_asset():
    json_request = request.json

    uuid = json_request.get('uuid')
    hostname = json_request.get('hostname')
    operating_system = json_request.get('operating_system')
    kernel_version = json_request.get('kernel_version')
    private_ip = json_request.get('private_ip')
    public_ip = json_request.get('public_ip')

    asset = Asset.query.filter_by(uuid=uuid).first()

    if asset:
        return {'message': 'UUID already exists'}

    try:
        asset = Asset(
            uuid=uuid,
            hostname=hostname,
            operating_system=operating_system,
            kernel_version=kernel_version,
            private_ip=private_ip,
            public_ip=public_ip
        )

        db.session.add(asset)
        db.session.commit()

        return {'message': 'Asset registered successfully'}, 201
    except Exception as e:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@assets.route('/<uuid>', methods=['PUT'])
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
        for current in software_list:
            result, software = helpers.software.check_for_match(asset.software, current)

            if not software:
                software = Software(
                    name=current['name'],
                    version=current['version']
                )

            if result == 'update':
                software.version = current['version']

            cpes = CPE.query.filter_by(product=current['name'], version=current['version'])

            for cpe in cpes:
                for cve in cpes.cves:
                    software.matched_cves.append(cve)

            if result == 'no_match':
                asset.software.append(software)
                continue

            db.session.add(software)

        db.session.add(asset)
        db.session.commit()

        return {'message': 'Asset updated successfully'}, 201
    except Exception as e:
        print(e)
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
