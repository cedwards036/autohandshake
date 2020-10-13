import unittest

from autohandshake import EventPage
from autohandshake.tests import TestSession


class TestEventPage(unittest.TestCase):

    def test_get_invited_schools(self):
        multischool_event_id = 592834
        with TestSession() as browser:
            page = EventPage(multischool_event_id, browser)
            schools = page.get_invited_schools()
            self.assertEqual(len(schools), 210)
            self.assertEqual(schools[0], 'Central Michigan University')
            self.assertEqual(schools[209], 'University of Illinois at Chicago')
