#!/usr/bin/python

import blessings
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import argparse
from collections import defaultdict
from datetime import timedelta, datetime
from pystache import render

# This tool goes though the Gluster regression links and checks for failures

BASE = 'https://build.gluster.org'
TERM = blessings.Terminal()
MAX_BUILDS = 1000
summary = defaultdict(list)
VERBOSE = None

def process_abortion(url):
    '''
    Process the aborted job
    '''
    log = requests.get(url, verify=False)
    print log.text.split('\n')[-7:][:3]

def get_summary(cut_off_date, reg_link):
    '''
    Get links to the failed jobs
    '''
    for page in xrange(0, MAX_BUILDS, 100):
        build_info = requests.get(''.join([
                BASE,
                reg_link,
                'api/json?depth=1&tree=allBuilds'
                '[url,result,timestamp,builtOn]',
                '{{{0},{1}}}'.format(page, page+100)
        ]), verify=False).json()
        for build in build_info.get('allBuilds'):
            if datetime.fromtimestamp(build['timestamp']/1000) < cut_off_date:
                # stop when timestamp older than cut off date
                return
            if build['result'] == 'ABORTED':
                url = ''.join([build['url'], 'consoleText'])
                print ''.join([
                    TERM.red,
                    'FAILURE on {0}'.format(url),
                    TERM.normal
                ])
                print build['builtOn']
                process_abortion(url)


def main(num_days, regression_link, html_report):
    cut_off_date = datetime.today() - timedelta(days=num_days)
    for reg in regression_link:
        if reg == 'centos':
            reg_link = '/job/centos6-regression/'
        elif reg == 'netbsd':
            reg_link = '/job/netbsd7-regression/'
        else:
            reg_link = reg
        get_summary(cut_off_date, reg_link)


if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    parser = argparse.ArgumentParser()
    parser.add_argument("get-summary")
    parser.add_argument(
            "last_no_of_days",
            default=1,
            type=int,
            help="Regression summary of last number of days"
    )
    parser.add_argument(
            "regression_link",
            default="centos",
            nargs='+',
            help="\"centos\" | \"netbsd\" | any other regression link"
    )
    parser.add_argument(
            "--verbose",
            default=False,
            action="store_true",
            help="Print a detailed report of each test case that is failed"
    )
    parser.add_argument(
            "--html-report",
            default=False,
            action="store_true",
            help="Print a brief report of failed regressions in html format"
    )
    args = parser.parse_args()
    VERBOSE = args.verbose
    main(
        num_days=args.last_no_of_days,
        regression_link=args.regression_link,
        html_report=args.html_report
    )
