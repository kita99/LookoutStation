from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

from app import app

db = SQLAlchemy(app)
db.create_all()


def serialize(obj, not_allowed_fields=False):
    data = {}

    for c in obj.__table__.columns:
        if not_allowed_fields == False:
            data[c.name] = getattr(obj, c.name) 
            continue

        if c.name not in not_allowed_fields:
            data[c.name] = getattr(obj, c.name) 

    return data


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def as_dict(self):
        return serialize(self, ['password'])

    def __repr__(self):
        return '<User %r>' % self.username


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(120), nullable=False)
    private_ip = db.Column(postgresql.INET, nullable=True)
    public_ip = db.Column(postgresql.INET, nullable=True)

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<Asset %r>' % self.uuid


class Software(db.Model):
    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(80), nullable=False)

    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    asset = db.relationship('Asset', backref=db.backref('software', lazy=True), cascade='all', passive_deletes = True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self, ['user_id'])

    def __repr__(self):
        return '<Software %r>' % self.name


class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    port = db.Column(db.Integer, nullable=False)
    protocol = db.Column(db.String(5), nullable=False)
    service_name = db.Column(db.String(10), nullable=False)
    state = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(10), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
