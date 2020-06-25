from psycopg2.extras import NumericRange
from sqlalchemy import desc
from flask import Blueprint
from flask import request

from lookoutstation.helpers import authentication
from lookoutstation.models import Scan
from lookoutstation.models import Port
from lookoutstation import helpers
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


@scans.route('/completed', methods=['GET'])
def get_completed_scans():
    try:
        completed_scans = Scan.query.filter_by(progress=100).all()

        return {'completed_scans': [scan.as_dict() for scan in completed_scans]}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@scans.route('/<public_ip>', methods=['GET'])
def get_scan_ports(public_ip):
    result = []

    try:
        scans = Scan.query.filter_by(public_ip=public_ip, progress=100).all()

        for scan in scans:
            if scan.progress != 100:
                continue

            current = scan.as_dict()
            current['open_ports'] = []
            current['closed_ports'] = []

            for port in scan.ports:
                if port.state == 'open':
                    current['open_ports'].append(port.as_dict())

                if port.state == 'closed':
                    current['closed_ports'].append(port.as_dict())

            result.append(current)

        return {'scans': scans}
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
    except:
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
        compact_ports = helpers.scan.compact(host)

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
                protocol=port['protocol'],
                service_name=port['service']['name'],
                state=port['state']['state'],
                reason=port['state']['reason']
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


@scans.route('/<public_ip>', methods=['DELETE'])
def delete_scan(public_ip):
    json_request = request.json

    worker_code = json_request.get('worker_code')

    if not worker_code:
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        Scan.query.filter_by(public_ip=public_ip, worker_code=worker_code).delete()

        return {'message': 'Scan deleted successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
