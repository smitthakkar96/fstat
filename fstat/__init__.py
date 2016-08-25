from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
Bootstrap(app)
db = SQLAlchemy(app)

from controller import index
