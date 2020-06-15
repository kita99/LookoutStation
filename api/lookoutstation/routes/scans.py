from flask import Blueprint
from flask import request

from lookoutstation.helpers import authentication
from lookoutstation.models import db


scans = Blueprint('scans', __name__)


@scans.route('/<public_ip>', methods=['PUT'])
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
