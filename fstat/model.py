from fstat import db
from datetime import datetime


STATE = (
    None,
    'SUCCESS',
    'FAILURE',
    'ABORTED',
)


class Failure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signature = db.Column(db.String(1000), index=True)
    failures = db.relationship('FailureInstance', backref='failure', lazy='dynamic')

class FailureInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    state = db.Column(db.Integer)
    job_name  = db.Column(db.String(100), index=True)
    node = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'))
    __table__args = (db.UniqueConstraint(url, failure_id))

    def process_build_info(self, build):
        self.state = STATE.index(build['result'])
        self.node = build['builtOn']
        self.timestamp = datetime.fromtimestamp(build['timestamp']/1000)

