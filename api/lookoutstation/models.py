from sqlalchemy.dialects import postgresql

from lookoutstation.app import db


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
    hostname = db.Column(db.String(50), nullable=False)
    operating_system = db.Column(db.String(50), nullable=False)
    kernel_version = db.Column(db.String(50), nullable=False)
    private_ip = db.Column(postgresql.INET, nullable=True)
    public_ip = db.Column(postgresql.INET, nullable=True)

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<Asset %r>' % self.uuid


class Software(db.Model):
    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id', ondelete='CASCADE'))
    asset = db.relationship('Asset', backref=db.backref('software', lazy=True), cascade='all')

    name = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(80), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self, ['user_id'])

    def __repr__(self):
        return '<Software %r>' % self.name


class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True)
    public_ip = db.Column(postgresql.INET, nullable=False)
    worker_code = db.Column(db.String(12), nullable=False)
    payload = db.Column(db.String(120), nullable=False)
    progress = db.Column(db.Integer, nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<Scan %r:%r>' % (self.public_ip, self.worker_code)


class Port(db.Model):
    __tablename__ = 'ports'

    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey('scans.id', ondelete='CASCADE'))
    scan = db.relationship('Scan', backref=db.backref('ports', lazy=True), cascade='all')

    port = db.Column(db.Integer, nullable=True)
    port_range = db.Column(postgresql.INT4RANGE, nullable=True)
    protocol = db.Column(db.String(5), nullable=True)
    service_name = db.Column(db.String(10), nullable=True)
    state = db.Column(db.String(10), nullable=False)
    reason = db.Column(db.String(10), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<Port %r:%r>' % (self.port, self.port_range)


class CVEFeed(db.Model):
    __tablename__ = 'cve_feeds'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    organization = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    meta_url = db.Column(db.String(255), nullable=False)
    data_type = db.Column(db.String(10), nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<CVEFeed %r>' % self.name
    

class CVEFeedTask(db.Model):
    __tablename__ = 'cve_feed_tasks'

    id = db.Column(db.Integer, primary_key=True)
    cve_feed_id = db.Column(db.Integer, db.ForeignKey('cve_feeds.id', ondelete='CASCADE'))
    cve_feed = db.relationship('CVEFeed', backref=db.backref('tasks', lazy=True), cascade='all')

    byte_size = db.Column(db.Integer, nullable=False)
    cve_amount = db.Column(db.Integer, nullable=False)
    sha256 = db.Column(db.String(255), nullable=False)
    raw_json = db.Column(postgresql.JSONB, nullable=False)

    feed_modification_date = db.Column(db.DateTime, nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<CVEFeedTask %r>' % self.sha256
    
    
class CVE(db.Model):
    __tablename__ = 'cves'

    id = db.Column(db.Integer, primary_key=True)
    created_by_feed_task_id = db.Column(db.Integer, db.ForeignKey('cve_feed_tasks.id', ondelete='CASCADE'))
    created_by_feed_task = db.relationship('CVEFeedTask', backref=db.backref('cves_created', lazy=True), cascade='all')
    updated_by_feed_task_id = db.Column(db.Integer, db.ForeignKey('cve_feed_tasks.id', ondelete='CASCADE'))
    updated_by_feed_task = db.relationship('CVEFeedTask', backref=db.backref('cves_updated', lazy=True), cascade='all')

    assigner = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    cve_modification_date = db.Column(db.DateTime, nullable=False)
    cve_publication_date = db.Column(db.DateTime, nullable=False)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<CVE %r>' % self.name
    

class CPE(db.Model):
    __tablename__ = 'cpes'

    id = db.Column(db.Integer, primary_key=True)
    cve_name = db.Column(db.String(50), db.ForeignKey('cves.name', ondelete='CASCADE'))
    cve = db.relationship('CVE', backref=db.backref('cves', lazy=True), cascade='all')

    part = db.Column(db.String(255), nullable=False)
    vendor = db.Column(db.String(255), nullable=False)
    product = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(255), nullable=True)
    update = db.Column(db.String(255), nullable=True)
    edition = db.Column(db.String(255), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<CPE %r:%r>' % (self.vendor, self.product)


class CVEImpactMetric(db.Model):
    __tablename__ = 'cve_impact_metrics'

    id = db.Column(db.Integer, primary_key=True)
    cve_name = db.Column(db.Integer, db.ForeignKey('cves.name', ondelete='CASCADE'))
    cve = db.relationship('CVE', backref=db.backref('impact_metrics', lazy=True), cascade='all')

    cvss_version = db.Column(db.String(10), nullable=False)
    vector_string = db.Column(db.String(255), nullable=False)
    attack_vector = db.Column(db.String(50), nullable=False)
    attack_complexity = db.Column(db.String(50), nullable=True)
    privileges_required = db.Column(db.String(50), nullable=True)
    user_interaction = db.Column(db.String(50), nullable=True)
    scope = db.Column(db.String(255), nullable=True)
    confidentiality_impact = db.Column(db.String(50), nullable=True)
    integrity_impact = db.Column(db.String(50), nullable=True)
    availability_impact = db.Column(db.String(50), nullable=True)
    base_score = db.Column(db.String(10), nullable=True)
    base_severity = db.Column(db.String(10), nullable=True)
    exploitability_score = db.Column(db.String(10), nullable=True)
    impact_score = db.Column(db.String(10), nullable=True)

    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def as_dict(self):
        return serialize(self)

    def __repr__(self):
        return '<CVEImpactMetric %r>' % self.vector_string
