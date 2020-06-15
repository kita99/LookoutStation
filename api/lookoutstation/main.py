from flask_cors import CORS

from routes.assets import assets
from routes.scans import scans
from routes.users import users
from app import app

CORS(app)

app.register_blueprint(users)
app.register_blueprint(assets, url_prefix='/assets')
app.register_blueprint(assets, url_prefix='/scans')
