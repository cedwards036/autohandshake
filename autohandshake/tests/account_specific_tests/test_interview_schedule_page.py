import unittest
from autohandshake import InterviewSchedulePage
from autohandshake.tests import TestSession


class TestAppointmentTypePage(unittest.TestCase):

    def test_get_schedule_contact_info_with_multiple_contacts(self):
        TEST_SCHEDULE_ID = 61382  # Bloomberg SWE Interviews, Fall 2018

        expected = [{'name': 'Bloomberg Engineering Campus Recruitment', 'email': 'fsdrecruitment@bloomberg.com'},
                    {'name': 'Catherine Malatack', 'email': 'cmalatack@bloomberg.net'},
                    {'name': 'Katie Golub', 'email': 'kgolub@bloomberg.com'}]

        with TestSession() as browser:
            schedule_page = InterviewSchedulePage(TEST_SCHEDULE_ID, browser)
            self.assertEqual(expected, schedule_page.get_contact_info())

    def test_get_schedule_contact_info_with_no_contacts(self):
        TEST_SCHEDULE_ID = 41258  # Fake Hop-Pop schedule with no contacts

        expected = []

        with TestSession() as browser:
            schedule_page = InterviewSchedulePage(TEST_SCHEDULE_ID, browser)
            self.assertEqual(expected, schedule_page.get_contact_info())

    def test_get_reserved_rooms(self):
        TEST_SCHEDULE_ID = 61382  # Bloomberg SWE Interviews, Fall 2018

        expected = 7

        with TestSession() as browser:
            schedule_page = InterviewSchedulePage(TEST_SCHEDULE_ID, browser)
            self.assertEqual(expected, schedule_page.get_reserved_rooms())
