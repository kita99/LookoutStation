from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate

from lookoutstation import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DB_CONN
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
