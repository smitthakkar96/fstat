from fstat.parser import get_summary
from fstat import app, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

with app.app_context():
    db.create_all()
    get_summary('centos6-regression', 5)
