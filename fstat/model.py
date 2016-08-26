from fstat import db
from datetime import datetime

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    state = db.Column(db.Integer)
    signature = db.Column(db.String(1000), index=True)
    job_name  = db.Column(db.String(100), index=True)
    node = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True)
    __table__args = (db.UniqueConstraint(url, signature))

    def process_build_info(self, build):
        self.state = build['result']
        self.node = build['builtOn']
        self.timestamp = datetime.fromtimestamp(build['timestamp']/1000)
