from flask import Blueprint

from lookoutstation.models import Software
from lookoutstation.models import Asset
from lookoutstation.models import CVEFeed
from lookoutstation.models import Port
from lookoutstation.models import CVE
from lookoutstation.models import CPE
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

        feed_count = CVEFeed.query.count()
        cve_count = CVE.query.count()
        cpe_count = CPE.query.count()

        for range in open_port_ranges:
            open_port_count += (range.upper - range.lower)

        return {
            'asset_count': asset_count,
            'vulnerability_count': vulnerability_count,
            'open_port_count': open_port_count,
            'feed_count': feed_count,
            'cve_count': cve_count,
            'cpe_count': cpe_count
        }
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
