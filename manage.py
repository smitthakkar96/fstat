#!/usr/bin/env python

from flask_script import Server, Manager
from fstat import app, db

manager = Manager(app)
manager.add_command('runserver', Server())

@manager.command
def db_init():
    db.create_all()


if __name__ == '__main__':
    manager.run()
