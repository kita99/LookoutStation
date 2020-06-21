from sqlalchemy import desc
from flask import Blueprint
from flask import request

from lookoutstation.models import CVEImpactMetric
from lookoutstation.models import CVEFeedTask
from lookoutstation.models import CVEFeed
from lookoutstation.models import CVE
from lookoutstation.models import CPE
from lookoutstation import helpers
from lookoutstation.app import db


feeds = Blueprint('feeds', __name__)


@feeds.route('', methods=['GET'])
def get_all_feeds():
    response = []

    try:
        feeds = CVEFeed.query.all()

        for feed in feeds:
            response.append(feed.as_dict())

        return {'feeds': response}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>', methods=['GET'])
def get_single_feed(id):
    try:
        feed = CVEFeed.query.filter_by(id=id).first()

        return {'feed_tasks': feed.as_dict()}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>/tasks', methods=['GET'])
def get_all_feeds_tasks(id):
    response = []

    try:
        feed_tasks = CVEFeedTask.query.filter_by(cve_feed_id=id).all()

        for feed_task in feed_tasks:
            response.append(feed_task.as_dict())

        return {'feed_tasks': response}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>/tasks', methods=['POST'])
def create_feed_task(id):
    json_request = request.json

    byte_size = json_request.get('byte_size')
    cve_amount = json_request.get('cve_amount')
    sha256 = json_request.get('sha256')
    feed_modification_date = json_request.get('feed_modification_date')
    raw_json = json_request.get('raw_json')

    try:
        feed_task = CVEFeedTask(
            cve_feed_id=id,
            byte_size=byte_size,
            cve_amount=cve_amount,
            sha256=sha256,
            feed_modification_date=feed_modification_date,
            raw_json=raw_json
        )

        db.session.add(feed_task)
        db.session.commit()

        return {'message': 'Feed task created successfully', 'id': feed_task.id}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>/tasks/<task_id>/cves', methods=['POST'])
def create_cve(id, task_id):
    json_request = request.json

    cves = json_request.get('cves')

    if not isinstance(cves, list):
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        primary_bulk = []
        secondary_bulk = []

        # NOTE: Some assumptions are being made on the data that should
        #       be fixed in the future (from the worker side)

        for cve in cves:
            primary_bulk.append(CVE(
                created_by_feed_task_id=task_id,
                name=cve['CVE_data_meta']['ID'],
                assigner=cve['CVE_data_meta']['ASSIGNER'],
                description=cve['description']['description_data'][0]['value'],
                cve_modification_date=cve['lastModifiedDate'],
                cve_publication_date=cve['publishedDate']
            ))

            impact_metrics = helpers.extract_and_prepare(cve, cve['CVE_data_meta']['ID'])
            cpes = helpers.cpe.find_and_parse(cve['configurations']['nodes'], cve['CVE_data_meta']['ID'])

            if impact_metrics:
                secondary_bulk.append(impact_metrics)

            if cpes:
                secondary_bulk.append(cpes)

        db.session.bulk_save_objects(primary_bulk)
        db.session.commit()

        db.session.bulk_save_objects(secondary_bulk)
        db.session.commit()

        return {'message': 'CVE data inserted successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>/tasks/<task_id>/cves', methods=['PUT'])
def update_cve(id, task_id):
    json_request = request.json

    cves = json_request.get('cves')

    if not isinstance(cves, list):
        return {'message': 'One or more parameters is malformed'}, 400

    try:
        # NOTE: In the future instead of deletes and updates
        #       maybe inserts with versioning for a timeline?

        for cve in cves:
            bulk = []

            existing = CVE.query.filter_by(cve_name=cve['CVE_data_meta']['ID'])

            existing.updated_by_feed_task_id = task_id
            existing.description = cve['description']['description_data'][0]['value']
            existing.cve_modification_date = cve['lastModifiedDate']

            CVEImpactMetric.query.filter_by(cve_name=cve['CVE_data_meta']['ID']).delete()
            CPE.query.filter_by(cve_name=cve['CVE_data_meta']['ID']).delete()

            impact_metrics = helpers.extract_and_prepare(cve, cve['CVE_data_meta']['ID'])
            cpes = helpers.cpe.find_and_parse(cve['configurations']['nodes'], cve['CVE_data_meta']['ID'])

            if impact_metrics:
                bulk.append(impact_metrics)

            if cpes:
                bulk.append(cpes)

            db.session.bulk_save_objects(bulk)
            db.session.commit()


        return {'message': 'CVEs updated successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500


@feeds.route('/<id>/tasks/latest', methods=['GET'])
def get_latest_feeds_task(id):
    try:
        feed_task = CVEFeedTask.query.filter_by(cve_feed_id=id).order_by(desc(CVEFeedTask.created_on)).first()

        return {'feed_task': feed_task.as_dict()}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
