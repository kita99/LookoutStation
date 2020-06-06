from flask_sqlalchemy import SQLAlchemy

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

    def as_dict(self):
        return serialize(self, ['password'])

    def __repr__(self):
        return '<User %r>' % self.username


class Software(db.Model):
    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('software', lazy=True), cascade='all', passive_deletes = True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self, ['user_id'])

    def __repr__(self):
        return '<Feed %r>' % self.title
