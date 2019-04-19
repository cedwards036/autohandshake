import unittest
from autohandshake.src.Pages import MajorSettingsPage
from autohandshake.tests import TestSession


class TestMajorSettingsPage(unittest.TestCase):

    def test_get_major_mapping(self):
        with TestSession() as browser:
            major_settings_page = MajorSettingsPage(browser)
            mapping = major_settings_page.get_major_mapping()
            self.assertEqual(
                {
                    'major': 'AD: Piano',
                    'groups': ['Music & Music Education', 'Visual & Performing Arts']
                }, mapping[3])
            self.assertEqual(
                {
                    'major': 'Applied Physics',
                    'groups': ['General Engineering', 'Aerospace Engineering', 'Physics']
                }, mapping[12])
            self.assertEqual(
                {
                    'major': 'Bachelors: Film & Media Studies',
                    'groups': ['Documentary/Film', 'Public Relations', 'Radio, Television, Media']
                }, mapping[30])
