import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re
from datetime import timedelta, datetime
from fstat import app


def process_failure(url, node):
    text = requests.get(url, verify=False).text
    accum = []
    for t in text.split('\n'):
        if t.find("Result: FAIL") != -1:
            for t2 in accum:
                if t2.find("Wstat") != -1:
                    test_case = re.search('\./tests/.*\.t', t2)
                    if test_case:
                        summary[test_case.group()].append((url, node))
            accum = []
        else:
            accum.append(t)


def get_summary(cut_off_date, reg_link):
    '''
    Get links to the failed jobs
    '''
    for page in xrange(0, app.config['MAX_BUILDS'], 100):
        build_info = requests.get(''.join([
                app.config['JENKINS_URL'],
                reg_link,
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
                process_failure(url, build['builtOn'])


def main(num_days, regression_link):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    cut_off_date = datetime.today() - timedelta(days=num_days)
    for reg in regression_link:
        if reg == 'centos':
            reg_link = '/job/centos6-regression/'
        elif reg == 'netbsd':
            reg_link = '/job/netbsd7-regression/'
        else:
            reg_link = reg
        get_summary(cut_off_date, reg_link)
