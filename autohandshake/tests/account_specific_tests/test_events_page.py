import unittest

from autohandshake import EventsPage
from autohandshake.tests import TestSession
import csv


def csv_to_list_of_dicts(filepath):
    with open(filepath, encoding='utf-8') as file:
        return [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]


class TestEventsPage(unittest.TestCase):

    def test_load_saved_search(self):
        other_checkbox_xpath = '//input[@id="5_event_types"]'
        start_date_xpath = '//input[@id="start_date"]'
        end_date_xpath = '//input[@id="end_date"]'

        with TestSession() as browser:
            page = EventsPage(browser)
            self.assertEqual('', page._browser.get_element_attribute_by_xpath(start_date_xpath, 'value'))
            self.assertEqual('', page._browser.get_element_attribute_by_xpath(end_date_xpath, 'value'))

            # test valid search
            page.load_saved_search('Test Saved Search')
            self.assertEqual(True, page._browser.element_is_selected_by_xpath(other_checkbox_xpath))
            self.assertEqual('2017-08-29', page._browser.get_element_attribute_by_xpath(start_date_xpath, 'value'))
            self.assertEqual('2017-08-31', page._browser.get_element_attribute_by_xpath(end_date_xpath, 'value'))

            # test invalid search
            with self.assertRaises(ValueError):
                page.load_saved_search('This isnt a saved search')

    def test_download_event_data(self):
        with TestSession() as browser:
            page = EventsPage(browser)
            page.load_saved_search('Test Saved Search')
            filepath = page.download_event_data(TestSession.download_dir)
            actual = csv_to_list_of_dicts(filepath)
            self.assertEqual(2, len(actual))
            self.assertEqual('69611', actual[0]['Id'])
            self.assertEqual('78187', actual[1]['Id'])
