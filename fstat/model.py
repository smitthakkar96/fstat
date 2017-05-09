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
    failures = db.relationship('FailureInstance',
                               backref='failure',
                               lazy='dynamic')


class FailureInstance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    state = db.Column(db.Integer)
    job_name = db.Column(db.String(100), index=True)
    node = db.Column(db.String(100), index=True)
    timestamp = db.Column(db.DateTime, index=True)
    review = db.Column(db.Integer, index=True)
    patchset = db.Column(db.Integer)
    branch = db.Column(db.String(100), index=True)
    failure_id = db.Column(db.Integer, db.ForeignKey('failure.id'))
    __table__args = (db.UniqueConstraint(url, failure_id))

    def process_build_info(self, build):
        self.state = STATE.index(build['result'])
        self.node = build['builtOn']
        self.timestamp = datetime.fromtimestamp(build['timestamp']/1000)
        try:
            self.review = build['actions'][5]['parameters'][4]['value']
        except KeyError:
            pass
        try:
            self.patchset = build['actions'][5]['parameters'][6]['value']
        except KeyError:
            pass
        try:
            self.branch = build['actions'][5]['parameters'][2]['value']
        except KeyError:
            self.branch = 'master'
