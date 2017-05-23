from functools import wraps
from datetime import datetime, timedelta

from flask import jsonify

from fstat import db, github
from model import FailureInstance


def x_days_ago(x=1):
    '''
    Return timestamp for X days ago
    '''
    return (datetime.today().replace(hour=0, minute=0, second=0,
            microsecond=0) - timedelta(days=x))

def parse_start_date(start_date=None):
    if not start_date:
        today = datetime.today().replace(hour=0, minute=0, second=0,
                                         microsecond=0)
        start_date = today - timedelta(days=today.weekday())

        if (datetime.today() - start_date).days == 0:
            start_date = start_date - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    return start_date


def parse_end_date(end_date=None):
    if not end_date:
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return end_date


def get_teams():
    organizations = github.get('user/orgs')
    return organizations


def organization_access_required(org):
    """ Decorator that can be used to validate the presence of user in a particular organization. """  # noqa: E501
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            teams = get_teams()
            for team in teams:
                if team['login'] == org:
                    return None
            return jsonify({"response": "You must be the memeber of \
                                        gluster to associate the bug."}), 401
        return wrap
    return decorator


def get_branch_list(fid=None):
    if not fid:
        return db.session.query(FailureInstance.branch) \
                .filter(FailureInstance.branch.isnot(None)) \
                .order_by(FailureInstance.branch) \
                .distinct()
    else:
        return db.session.query(FailureInstance.branch) \
                .filter(FailureInstance.failure_id == fid,
                        FailureInstance.branch.isnot(None)) \
                .order_by(FailureInstance.branch) \
                .distinct()
