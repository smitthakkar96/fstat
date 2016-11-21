from datetime import datetime, timedelta


def x_days_ago(x=1):
    '''
    Return timestamp for X days ago
    '''
    return datetime.today() - timedelta(days=x)
