import unittest
from autohandshake.src.Pages.SchoolSettings import MajorSettingsPage
from autohandshake.tests import TestSession


class TestMajorSettingsPage(unittest.TestCase):

    def test_get_major_mapping(self):
        with TestSession() as browser:
            major_settings_page = MajorSettingsPage(browser)
            mapping = major_settings_page.get_major_mapping()
            self.assertEqual(
                {
                    'major': 'AD: Piano',
                    'groups': ['Visual & Performing Arts', 'Music & Music Education']
                }, mapping[3])
            self.assertEqual(
                {
                    'major': 'Applied Physics',
                    'groups': ['Physics', 'General Engineering', 'Aerospace Engineering']
                }, mapping[12])
            self.assertEqual(
                {
                    'major': 'Bachelors: Film & Media Studies',
                    'groups': ['Public Relations', 'Documentary/Film', 'Radio, Television, Media']
                }, mapping[30])
