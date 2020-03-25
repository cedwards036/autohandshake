import unittest
from autohandshake.src.Pages import AccessRequestPage, RequestStatus
from autohandshake.tests import TestSession
from datetime import datetime


class TestAccessRequestPage(unittest.TestCase):

    def test_get_request_data_with_single_page_data(self):
        with TestSession() as browser:
            expected_failed = [
                {
                    'user': 'Diunase Nso Keshu',
                    'user_id': '16052363',
                    'email': 'dnsokes1@jh.edu',
                    'request_date': datetime.strptime('2018-09-20', '%Y-%m-%d').date(),
                    'request': 'Student Access',
                    'status': 'failed'
                },
                {
                    'user': 'Songnan Wang',
                    'user_id': '374064',
                    'email': 'swang140@jhu.edu',
                    'request_date': datetime.strptime('2018-09-05', '%Y-%m-%d').date(),
                    'request': 'Student Reactivation',
                    'status': 'failed'
                },
                {
                    'user': 'Krista Grubb',
                    'user_id': '369508',
                    'email': 'krista.grubb@jhu.edu',
                    'request_date': datetime.strptime('2018-08-15', '%Y-%m-%d').date(),
                    'request': 'Student Reactivation',
                    'status': 'failed'
                }
            ]
            access_page = AccessRequestPage(browser)
            actual_failed = access_page.get_request_data(RequestStatus.FAILED)
            self.assertEqual(expected_failed, actual_failed[-3:])

    # This test should only be uncomment and run manually to visually confirm the
    # code works. The actual results of this method call vary from day to day, and
    # a true, consistent test of this functionality is not possible.

    # def test_get_request_data_with_multi_page_data(self):
    #
    #     with TestSession(10) as browser:
    #         access_page = AccessRequestPage(browser)
    #
    #         print(access_page.get_request_data())
