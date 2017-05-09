from collections import Counter
from flask import render_template, redirect, url_for, request
from fstat import app, db
from fstat.lib import x_weeks_ago
from model import Failure, FailureInstance
from datetime import datetime, timedelta


@app.route("/")
def index():
    return redirect(url_for('overall_summary'))


@app.route('/summary')
def overall_summary():
    ''' 
        Shows overall summary
        Params
            - start_day: date with format yy-mm-dd, if start date is none it is defaulted to the last monday
            - end_day: date with format yy-mmd-dd, if end date is none it is defaulted to today
    '''
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date:
        today = datetime.today().replace(hour=0, minute=0, second=0,
                                         microsecond=0)
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date = datetime.today().replace(hour=0, minute=0, second=0,
                                            microsecond=0)
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    failure_instances = FailureInstance.query.filter(FailureInstance.timestamp > start_date, 
                                                     FailureInstance.timestamp < end_date)
    failures = Counter([x.failure for x in failure_instances])
    return render_template('index.html',
                           num=(end_date - start_date).days,
                           failures=failures,
                           total=len(failures),
                           end_date=str(end_date.date()),
                           start_date=str(start_date.date()),
                           )    
    

@app.route('/failure/<int:fid>')
def instance_summary(fid=None):
    ''' 
        Shows instance summary for particular failure
        Params
            - start_day: date with format yy-mm-dd, if start date is none it is defaulted to the last monday
            - end_day: date with format yy-mmd-dd, if end date is none it is defaulted to today
    '''    
    fid = int(fid)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date:
        today = datetime.today().replace(hour=0, minute=0, second=0,
                                         microsecond=0)
        start_date = today - timedelta(days=today.weekday())
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date = datetime.today().replace(hour=0, minute=0, second=0,
                                            microsecond=0)
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    failure = Failure.query.filter_by(id=fid).first_or_404()
    failure_instances = FailureInstance.query.filter(
            db.and_(
                FailureInstance.timestamp > start_date,
                FailureInstance.timestamp < end_date,
                FailureInstance.failure == failure))
    return render_template('failure_instance.html',
                            num=(end_date - start_date).days,
                            failure=failure,
                            failure_instances=failure_instances,
                            end_date=str(end_date.date()),
                            start_date=str(start_date.date()),
                            title="Summary for " + failure.signature
                            )    



@app.route("/weeks/<int:num>")
def weekly_overall_summary(num=None):
    if num > 12:
        num = 12
    cut_off_date = (x_weeks_ago(num*7))
    failure_instances = FailureInstance.query.filter(
            FailureInstance.timestamp > cut_off_date)
    failures = Counter([x.failure for x in failure_instances])
    return render_template('index.html',
                           num=num,
                           failures=failures,
                           total=len(failures),
                           cut_off=cut_off_date.strftime('%Y-%m-%d'),
                           today=datetime.today().strftime('%Y-%m-%d'),
                           )


@app.route("/weeks/<int:num>/failure/<int:fid>")
def weekly_instance_summary(num=None, fid=None):
    if num > 4:
        num = 4
    fid = int(fid)
    cut_off_date = (x_weeks_ago(num*7))
    print cut_off_date
    failure = Failure.query.filter_by(id=fid).first_or_404()
    failure_instances = FailureInstance.query.filter(
            db.and_(
                FailureInstance.timestamp > cut_off_date,
                FailureInstance.failure == failure))
    return render_template('failure_instance.html',
                           num=num,
                           failure=failure,
                           failure_instances=failure_instances,
                           cut_off=cut_off_date.strftime('%Y-%m-%d'),
                           today=datetime.today().strftime('%Y-%m-%d'),
                           title="Summary for " + failure.signature,
                           )
