from datetime import datetime, timedelta

from fstat import db
from model import FailureInstance

def x_days_ago(x=1):
    '''
    Return timestamp for X days ago
    '''
    return (datetime.today().replace(hour=0, minute=0, second=0,
            microsecond=0) - timedelta(days=x))


def parse_start_date(start_date):
    if not start_date:
        today = datetime.today().replace(hour=0, minute=0, second=0,
                                         microsecond=0)
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    return start_date


def parse_end_date(end_date):
    if not end_date:
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    return end_date    


def get_branch_list(fid):
    return db.session.query(FailureInstance.branch).filter(FailureInstance.failure_id == fid).distinct()
