from passlib.hash import sha256_crypt
from flask import Blueprint
import click
import requests

import getpass
import json

from lookoutstation.models import CVEImpactMetric
from lookoutstation.models import CVEFeedTask
from lookoutstation.models import CVEFeed
from lookoutstation.models import Software
from lookoutstation.models import Asset
from lookoutstation.models import CVE
from lookoutstation.models import CPE
from lookoutstation.models import User
from lookoutstation.models import Scan
from lookoutstation.models import Port
from lookoutstation.models import db

commands = Blueprint('commands', __name__)


def dot_print(left, right):
    dot_len = 35 
    l_len = len(left)
    dots = (dot_len - l_len) * '.'

    click.echo(f'{left}{dots}{right}')


@commands.cli.command('create-user', help='Create an administrator account')
def create_user():
    username = input('Username (admin): ')

    if not username:
        username = 'admin'

    email = input('Email (admin@admin.com):')

    if not email:
        email = 'admin@admin.com'

    while True:
        password = getpass.getpass('Password (min. 8 chars): ')

        if len(password) > 7:
            break

        click.echo('Please insert a valid password')

    try:
        user = User(username=username, password=sha256_crypt.hash(password), email=email)

        db.session.add(user)
        db.session.commit()

        click.echo(f'User "{username}" created successfully!')
    except Exception as e:
        click.echo(e)
        click.echo(f'Could not create user "{username}"')


@commands.cli.command('tasks', help='Basic task utilities for workers')
@click.argument('command')
@click.argument('subcommand', required=False)
@click.argument('payload', required=False)
def tasks(command, subcommand, payload):
    if command == 'publish':
        if subcommand and payload:
            res = requests.post(
                url='http://lookoutstation-worker-master/publish',
                json={
                    'queue': subcommand,
                    'message': payload
                }
            )

            if res.status_code != 200:
                click.echo(f'Could not publish {payload} to queue {subcommand}. Code: {res.status_code}')

            click.echo('Message published to redis successfully!')

            return


    if command == 'trigger':
        if subcommand == 'scheduler':
            res = requests.get('http://lookoutstation-worker-scheduler/trigger')

            if res.status_code != 200:
                click.echo(f'Could not trigger scheduler. Code: {res.status_code}')

            click.echo('Scheduler triggered successfully!')

            return


    if command == 'queues':
        res = requests.get('http://lookoutstation-worker-master/queues')

        if res.status_code != 200:
            click.echo(f'Could not trigger scheduler. Code: {res.status_code}')

            return

        click.echo(json.dumps(res.json(), indent=4))

        return


    if command == 'clear':
        res = requests.get('http://lookoutstation-worker-master/cleanup')

        if res.status_code != 200:
            click.echo(f'Could not trigger scheduler. Code: {res.status_code}')

            return

        click.echo(json.dumps(res.json(), indent=4))

        return


    if not subcommand:
        click.echo(f'Task command "{command}" not recognized')
        return


    click.echo(f'Task command "{command} {subcommand}" not recognized')


@commands.cli.command('seed', help='Jumpstart the app with crucial data')
@click.argument('entity')
def seeds(entity):
    if entity == 'feeds':
        feeds = []
        description = '''  Each vulnerability in the feed includes a description and associated reference links
                           from the CVE® dictionary feed, as well as CVSS base scores, vulnerable product configuration,
                           and weakness categorization. '''

        try:
            for year in range(2002, 2021):
                feeds.append(CVEFeed(
                    name=f'CVE-{year}',
                    description=description,
                    organization='NIST',
                    url=f'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.json.gz',
                    meta_url=f'https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-{year}.meta',
                    data_type='json'
                ))

            db.session.bulk_save_objects(feeds)
            db.session.commit()

            click.echo('Successfully seeded CVEFeeds with feeds from NIST')
            return
        except Exception as e:
            click.echo(e)
            click.echo('Whoops, something went wrong (no changes made)')
            db.session.rollback()

    click.echo(f'{entity} is not recognized as a seedable entity')


@commands.cli.command('db', help='Visualize or recreate the database')
@click.argument('action')
def database_actions(action):
    if action == 'recreate':
        try:
            db.drop_all()
            db.create_all()

            click.echo('Database recreated successfully!')

            return
        except:
            click.echo('Could not recreate database: ')

    if action == 'overview':
        dot_print('Total Users', User.query.count())
        dot_print('Total Assets', Asset.query.count())
        dot_print('Total Software', Software.query.count())
        dot_print('Total Scans', Scan.query.count())
        dot_print('Total Ports', Port.query.count())
        dot_print('Total CVEs', CVE.query.count())
        dot_print('Total CPEs', CPE.query.count())
        dot_print('Total CVE Feeds', CVEFeed.query.count())
        dot_print('Total CVE Feed Tasks', CVEFeedTask.query.count())
        dot_print('Total CVE Impact Metrics', CVEImpactMetric.query.count())

        return

    click.echo(f'{action} is not recognized as a valid action')
