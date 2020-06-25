from flask import Blueprint

from lookoutstation.models import Software
from lookoutstation.models import Asset
from lookoutstation.models import Port
from lookoutstation.app import db


statistics = Blueprint('statistics', __name__)


@statistics.route('/overview', methods=['GET'])
def get_overview_statistics():
    vulnerability_count = 0

    try:
        asset_count = Asset.query.count()

        global_software = Software.query.all()

        for software in global_software:
            if software.matched_cves:
                vulnerability_count += len(software.matched_cves)

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
