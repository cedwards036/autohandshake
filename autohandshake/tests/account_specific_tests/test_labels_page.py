import unittest
from autohandshake import LabelSettingsPage
from autohandshake.tests import TestSession


class TestLabelSettingsPage(unittest.TestCase):

    def test_get_label_data_scrapes_webpage_correctly(self):
        with TestSession() as browser:
            label_settings_page = LabelSettingsPage(browser)
            labels = label_settings_page.get_label_data()
            self.assertEqual(['label_name', 'usage_counts', 'used_for', 'created_by_first_name', 'created_by_last_name',
                              'label_type'],
                             list(labels[0].keys()))

            # Warning: test data may change at any time, causing the test to fail!
            amm_expected = {
                'label_name': 'hwd: arts, media, and marketing academy',
                'usage_counts': {
                    'InterviewSchedule': 1,
                    'Job': 1,
                    'Event': 43
                },
                'used_for': 'All',
                'created_by_first_name': 'Krystle',
                'created_by_last_name': 'Wagemann',
                'label_type': 'normal',
            }
            ferpa_expected = {
                'label_name': 'ferpa',
                'usage_counts': {
                    'User': 842
                },
                'used_for': 'All',
                'created_by_first_name': None,
                'created_by_last_name': None,
                'label_type': 'system',
            }
            self.assertEqual(amm_expected, labels[34])
            self.assertEqual(ferpa_expected, labels[30])
