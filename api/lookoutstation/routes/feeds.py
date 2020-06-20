from sqlalchemy import desc
from flask import Blueprint
from flask import request

from lookoutstation.helpers import authentication
from lookoutstation.models import CVEFeed
from lookoutstation.models import CVEFeedTask
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

    try:
        feed_task = CVEFeedTask(
            cve_feed_id=id,
            byte_size=byte_size,
            cve_amount=cve_amount,
            sha256=sha256
        )

        db.session.add(feed_task)
        db.session.commit()

        return {'message': 'Feed task created successfully'}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500

    pass


@feeds.route('/<id>/tasks/latest', methods=['GET'])
def get_latest_feeds_task(id):
    try:
        feed_task = CVEFeedTask.query.filter_by(cve_feed_id=id).order_by(desc(CVEFeedTask.created_on)).first()

        return {'feed_task': feed_task.as_dict()}
    except:
        db.session.rollback()
        return {'message': 'Internal server error'}, 500
