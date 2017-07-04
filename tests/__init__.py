import os

from fstat.parser import get_summary

os.system("flask db upgrade")
get_summary('centos6-regression', 5)
