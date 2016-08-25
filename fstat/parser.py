import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
from datetime import timedelta, datetime
from fstat import app, db, Job


def process_failure(url, build_info):
    text = requests.get(url, verify=False).text
    accum = []
    for t in text.split('\n'):
        if t.find("Result: FAIL") != -1:
            for t2 in accum:
                if t2.find("Wstat") != -1:
                    test_case = re.search('\./tests/.*\.t', t2)
                    if test_case:
                        failure = Job()
                        failure.url = url
                        failure.state = build_info['result']
                        failure.signature = test_case.group()
                        failure.node = build_info['builtOn']
                        failure.timestamp = datetime.fromtimestamp(build_info['timestamp']/1000)
                        db.session.add(failure)
                        db.session.commit()
            accum = []
        else:
            accum.append(t)


def get_summary(job_name, num_days):
    '''
    Get links to the failed jobs
    '''
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    cut_off_date = datetime.today() - timedelta(days=num_days)
    for page in xrange(0, app.config['JENKINS_MAX'], 100):
        print ''.join([
                app.config['JENKINS_URL'],
                '/job/',
                job_name,
                '/'
                'api/json?depth=1&tree=allBuilds'
                '[url,result,timestamp,builtOn]',
                '{{{0},{1}}}'.format(page, page+100)
        ])
        build_info = requests.get(''.join([
                app.config['JENKINS_URL'],
                '/job/',
                job_name,
                '/'
                'api/json?depth=1&tree=allBuilds'
                '[url,result,timestamp,builtOn]',
                '{{{0},{1}}}'.format(page, page+100)
        ]), verify=False).json()
        for build in build_info.get('allBuilds'):
            if datetime.fromtimestamp(build['timestamp']/1000) < cut_off_date:
                # stop when timestamp older than cut off date
                return
            if build['result'] not in [None, 'SUCCESS']:
                url = ''.join([build['url'], 'consoleText'])
                process_failure(url, build)
