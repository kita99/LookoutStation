from flask import Blueprint
from flask import request

from lookoutstation.models import Scan
from lookoutstation.models import Port
from lookoutstation.app import db


statistics = Blueprint('statistics', __name__)


@statistics.route('/overview', methods=['GET'])
def get_overview_statistics():
    try:
        asset_count = 1
        vulnerability_count = 'IMPLEMENT_ME'
        open_port_count = Port.query.filter_by(state='open').filter(Port.port_range is None).count()
        open_port_ranges = Port.query.filter_by(state='open').filter(Port.port is None).all()

        for range in open_port_ranges:
            open_port_count += (range.upper - range.lower)

        return {
            'asset_count': asset_count,
            'vulnerability_count': vulnerability_count,
            'open_port_count': open_port_count
        }
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
