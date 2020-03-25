import unittest

from autohandshake import SurveyPage
from autohandshake.tests import TestSession
import csv

TEST_SURVEY = 33726


def csv_to_list_of_dicts(filepath):
    with open(filepath) as file:
        return [{k: v for k, v in row.items()} for row in csv.DictReader(file, skipinitialspace=True)]


class TestSurveyPage(unittest.TestCase):

    def test_get_survey_data(self):
        expected = [
            {
                'Name': 'Christopher Edwards',
                'Date': '2019-08-07 17:58:01 UTC',
                'Email Address': 'cedwar42@jhu.edu',
                'What is your name?': 'John',
                'What is your quest?': 'Option B',
                'Describe your dog:': 'She is small and cute.',
                'Which of the following?': 'a, c',
                'How likely are you?': '3'
            },
            {
                'Name': 'Jasmine Miller',
                'Date': '2019-08-07 17:59:25 UTC',
                'Email Address': 'rshille1@jhu.edu',
                'What is your name?': 'Becca',
                'What is your quest?': 'Option Three',
                'Describe your dog:': 'I have a cat',
                'Which of the following?': 'e',
                'How likely are you?': '9'
            },
            {
                'Name': 'Aleanairis Nunez',
                'Date': '2019-08-07 18:00:50 UTC',
                'Email Address': 'anunez5@jhu.edu',
                'What is your name?': 'Aly',
                'What is your quest?': 'Option 1',
                'Describe your dog:': 'I might have a dog?',
                'Which of the following?': 'a, b, c, d, e',
                'How likely are you?': '5'
            },
        ]

        with TestSession() as browser:
            page = SurveyPage(TEST_SURVEY, browser)
            filepath = page.download_responses(TestSession.download_dir)
            actual = csv_to_list_of_dicts(filepath)
            self.assertEqual(expected, actual)
