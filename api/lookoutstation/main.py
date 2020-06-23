from flask_cors import CORS

from lookoutstation.routes.statistics import statistics
from lookoutstation.routes.assets import assets
from lookoutstation.routes.scans import scans
from lookoutstation.routes.users import users
from lookoutstation.routes.feeds import feeds
from lookoutstation.cli import commands
from lookoutstation.app import app

CORS(app)

app.register_blueprint(users)
app.register_blueprint(assets, url_prefix='/assets')
app.register_blueprint(scans, url_prefix='/scans')
app.register_blueprint(feeds, url_prefix='/feeds')
app.register_blueprint(statistics, url_prefix='/statistics')

app.register_blueprint(commands, cli_group=None)
