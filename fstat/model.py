from fstat import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))
    state = db.Column(db.Integer)
    signature = db.Column(db.String(1000), index=True)
    os = db.Column(db.Integer, index=True)
    node = db.Column(db.Integer, index=True)
    timestamp = db.Column(db.DateTime, index=True)
    db.UniqueConstraint('url', 'signature')
