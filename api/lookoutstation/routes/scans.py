from psycopg2.extras import NumericRange
from sqlalchemy import desc
from flask import Blueprint
from flask import request

from lookoutstation.helpers import authentication
from lookoutstation.helpers import scans
from lookoutstation.models import Scan
from lookoutstation.models import Port
from lookoutstation.app import db


scans = Blueprint('scans', __name__)


@scans.route('/ongoing', methods=['GET'])
def get_ongoing_scans():

    try:
        ongoing_scans = Scan.query.filter(Scan.progress != 100).all()

        return {'ongoing_scans': [scan.as_dict() for scan in ongoing_scans]}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@scans.route('/<public_ip>', methods=['POST'])
def create_scan(public_ip):
    json_request = request.json

    worker_code = json_request.get('worker_code')
    payload = json_request.get('payload')

    if not worker_code or not payload:
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        scan = Scan(
            worker_code=worker_code,
            public_ip=public_ip,
            payload=payload,
            progress=0
        )

        db.session.add(scan)
        db.session.commit()

        return {'message': 'Scan created successfully'}
    except Exception as e:
        print(e)
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@scans.route('/<public_ip>', methods=['PUT'])
def update_scan(public_ip):
    is_port_range = False
    json_request = request.json

    worker_code = json_request.get('worker_code')
    progress = json_request.get('progress')
    ports = json_request.get('ports')
    hosts = json_request.get('hosts')

    if not isinstance(hosts, list):
        return {'message': 'One or more parameters is malformed'}, 400

    host = hosts[0]

    if not worker_code or not progress or not ports:
        return {'message': 'One or more parameters is malformed'}, 400

    scan = Scan.query.filter_by(worker_code=worker_code).order_by(desc(Scan.updated_on)).first()

    if not scan:
        return {'message': 'This worker does not have any recently initiated scans'}, 404


    if '-' in ports:
        range_start, range_end = ports.split('-')
        is_port_range = True


    if host['ports'] and not host['extra_ports']:
        compact_ports = scans.compact(host)

        for port in compact_ports:
            is_port_range = False

            if 'range_end' in port:
                is_port_range = port['range_start'] != port['range_end']

            scan.ports.append(Port(
                port=port['range_start'] if not is_port_range else None,
                port_range=NumericRange(port['range_start'], port['range_end']) if is_port_range else None,
                protocol=port['protocol'],
                service_name=port['service_name'],
                state=port['state'],
                reason=port['reason']
            ))


    if not host['ports'] and host['extra_ports']:
        scan.ports.append(Port(
            port=ports if not is_port_range else None,
            port_range=NumericRange(int(range_start), int(range_end)) if is_port_range else None,
            protocol='tcp',
            service_name=None,
            state=host['extra_ports'][0]['state'],
            reason=host['extra_ports'][0]['reasons'][0]['reason']
        ))


    if host['ports'] and host['extra_ports']:
        for i, port in enumerate(host['ports']):
            if i != 0:
                range_start = int(host['ports'][i-1]['id']) + 1

            scan.ports.append(Port(
                port_range=NumericRange(int(range_start), int(port['id']) - 1),
                protocol='tcp',
                service_name=None,
                state=host['extra_ports'][0]['state'],
                reason=host['extra_ports'][0]['reasons'][0]['reason']
            ))

            scan.ports.append(Port(
                port=port['id'],
                protocol='tcp',
                service_name=None,
                state=host['extra_ports'][0]['state'],
                reason=host['extra_ports'][0]['reasons'][0]['reason']
            ))

    try:
        scan.progress = progress
        scan.state = host['status']['state']
        scan.reason = host['status']['reason']

        db.session.add(scan)
        db.session.commit()

        return {'message': 'Scan data inserted successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500

