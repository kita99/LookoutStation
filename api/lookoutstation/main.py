from flask_cors import CORS

from routes.statistics import statistics
from routes.assets import assets
from routes.scans import scans
from routes.users import users
from routes.feeds import feeds
from cli import commands
from app import app

CORS(app)

app.register_blueprint(users)
app.register_blueprint(assets, url_prefix='/assets')
app.register_blueprint(scans, url_prefix='/scans')
app.register_blueprint(feeds, url_prefix='/feeds')
app.register_blueprint(statistics, url_prefix='/statistics')

app.register_blueprint(commands, cli_group=None)
