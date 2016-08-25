from fstat import db

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100))

