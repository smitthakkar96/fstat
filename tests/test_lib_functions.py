""" Unit tests for the utility functions present in lib.py """

import unittest
from datetime import datetime
from mock import Mock, patch

from fstat import lib


class TestDateFunctions(unittest.TestCase):
    """ Test cases for datetime releated functions in lib.py"""

    @patch('fstat.lib.datetime')
    def test_parse_start_date_without_params(self, datetime_mock):
        """ Test parse start date function without start_date """
        datetime_mock.today = Mock(return_value=datetime.strptime('May 11 2017', '%b %d %Y'))
        assert lib.parse_start_date().day == 8

    def test_parse_start_date_with_params(self):
        """ Test parse start date function with start_date """
        assert lib.parse_start_date("2017-01-01").day == 1

    @patch('fstat.lib.datetime')
    def test_parse_end_date_without_params(self, datetime_mock):
        """ Test parse start date function without end_date """
        datetime_mock.today = Mock(return_value=datetime.strptime('May 11 2017', '%b %d %Y'))
        assert lib.parse_end_date() == datetime.strptime('May 11 2017', '%b %d %Y')

    def test_parse_end_date_with_params(self):
        """ Test parse start date function with end_date """
        assert lib.parse_end_date("2017-05-11") == datetime.strptime('May 11 2017', '%b %d %Y')
