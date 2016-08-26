from flask import render_template
from fstat import app
from model import Job

@app.route("/")
def index():
    failures = Job.query.all()
    print failures
    return render_template('index.html', failures=failures)
