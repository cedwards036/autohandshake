import unittest
from autohandshake.src.Pages import MajorSettingsPage
from autohandshake.tests import TestSession


class TestMajorSettingsPage(unittest.TestCase):

    def test_get_major_mapping(self):
        with TestSession() as browser:
            major_settings_page = MajorSettingsPage(browser)
            mapping = major_settings_page.get_major_mapping()
            self.assertEqual('AD: Piano', mapping[4]['major'])
            self.assertEqual(['Music & Music Education', 'Visual & Performing Arts'], sorted(mapping[4]['groups']))

            self.assertEqual('Applied Physics', mapping[13]['major'])
            self.assertEqual(['Aerospace Engineering', 'General Engineering', 'Physics'], sorted(mapping[13]['groups']))

            self.assertEqual('Bachelors: Film & Media Studies', mapping[33]['major'])
            self.assertEqual(['Documentary/Film', 'Public Relations', 'Radio, Television, Media'],
                             sorted(mapping[33]['groups']))
