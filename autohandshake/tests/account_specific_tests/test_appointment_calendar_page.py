import unittest
from autohandshake import AppointmentCalendarPage
from autohandshake.tests import TestSession
from datetime import datetime

LOCATION_VARIES = 'In-Person (Location: Varies- Coach will contact you with location)'
IN_PERSON = 'In-Person (Location: Career Center--Garland Hall 389)'
VIRTUAL = 'Virtual Appointment (Coach will Contact You)'


class TestAppointmentCalendarPage(unittest.TestCase):

    def test_go_to_date(self):
        test_date_1 = datetime(2018, 9, 13).date()
        test_date_2 = datetime(2019, 10, 30).date()

        with TestSession() as browser:
            calendar = AppointmentCalendarPage(browser)
            calendar.go_to_date(test_date_1)
            self.assertTrue(browser.element_exists_by_xpath("//span[text()='Thursday, September 13th']"))
            calendar.go_to_date(test_date_2)
            self.assertTrue(browser.element_exists_by_xpath("//span[text()='Wednesday, October 30th']"))

    def test_get_one_day_of_unfilled(self):
        with TestSession() as browser:
            calendar = AppointmentCalendarPage(browser)
            expected = [
                {
                    'start_time': datetime(2017, 11, 8, 15, 0),
                    'end_time': datetime(2017, 11, 8, 16, 0),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Justin Lorts',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 8, 14, 0),
                    'end_time': datetime(2017, 11, 8, 14, 30),
                    'length': 30,
                    'status': 'unfilled',
                    'staff_name': 'Nadine Goldberg',
                    'mediums': [IN_PERSON, VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 8, 11, 0),
                    'end_time': datetime(2017, 11, 8, 12, 0),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 8, 13, 0),
                    'end_time': datetime(2017, 11, 8, 15, 0),
                    'length': 120,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                }
            ]
            actual = calendar.get_unfilled_blocks(datetime(2017, 11, 8).date(), include_mediums=True)
            self.assertEqual(expected, actual)

    def test_multi_day(self):
        with TestSession(30) as browser:
            calendar = AppointmentCalendarPage(browser)
            expected = [
                {
                    'start_time': datetime(2017, 11, 10, 9, 30),
                    'end_time': datetime(2017, 11, 10, 10, 0),
                    'length': 30,
                    'status': 'unfilled',
                    'staff_name': 'Caroline Kelly',
                    'mediums': [VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 10, 11, 0),
                    'end_time': datetime(2017, 11, 10, 11, 30),
                    'length': 30,
                    'status': 'unfilled',
                    'staff_name': 'Caroline Kelly',
                    'mediums': [VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 10, 13, 0),
                    'end_time': datetime(2017, 11, 10, 14, 0),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Lauren Barrett',
                    'mediums': [VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 10, 10, 0),
                    'end_time': datetime(2017, 11, 10, 12, 0),
                    'length': 120,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 10, 14, 0),
                    'end_time': datetime(2017, 11, 10, 15, 30),
                    'length': 90,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 13, 9, 0),
                    'end_time': datetime(2017, 11, 13, 10, 0),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Andrea Wiseman',
                    'mediums': [IN_PERSON, VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 13, 10, 30),
                    'end_time': datetime(2017, 11, 13, 11, 30),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Caroline Kelly',
                    'mediums': [IN_PERSON, VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 13, 10, 30),
                    'end_time': datetime(2017, 11, 13, 12, 0),
                    'length': 90,
                    'status': 'unfilled',
                    'staff_name': 'Justin Lorts',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 13, 14, 30),
                    'end_time': datetime(2017, 11, 13, 15, 0),
                    'length': 30,
                    'status': 'unfilled',
                    'staff_name': 'Lauren Barrett',
                    'mediums': [IN_PERSON, VIRTUAL]
                },
                {
                    'start_time': datetime(2017, 11, 13, 13, 0),
                    'end_time': datetime(2017, 11, 13, 16, 0),
                    'length': 180,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 13, 10, 0),
                    'end_time': datetime(2017, 11, 13, 11, 0),
                    'length': 60,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                },
                {
                    'start_time': datetime(2017, 11, 13, 11, 30),
                    'end_time': datetime(2017, 11, 13, 12, 0),
                    'length': 30,
                    'status': 'unfilled',
                    'staff_name': 'Sonjala Williams',
                    'mediums': [LOCATION_VARIES]
                }
            ]
            actual = calendar.get_unfilled_blocks(datetime(2017, 11, 10).date(), datetime(2017, 11, 14).date(),
                                                  include_mediums=True)
            self.assertEqual(expected, actual)


class TestAppointmentCalendarPageOpenBlockAlgorithm(unittest.TestCase):
    def test_degernerate_cases(self):
        open_block = {
            'start_time': datetime(2018, 11, 2, 10, 0),
            'end_time': datetime(2018, 11, 2, 14, 0)
        }

        consuming_conflicts = [
            {
                'start_time': datetime(2018, 11, 2, 9, 30),
                'end_time': datetime(2018, 11, 2, 16, 10)
            }
        ]

        consuming_actual = AppointmentCalendarPage._get_open_block_segments(open_block, consuming_conflicts)
        no_conflict_actual = AppointmentCalendarPage._get_open_block_segments(open_block, [])
        self.assertEqual([], consuming_actual)
        self.assertEqual([open_block], no_conflict_actual)

    def test_bookends_only_case(self):
        open_block = {
            'start_time': datetime(2018, 11, 2, 10, 0),
            'end_time': datetime(2018, 11, 2, 14, 0)
        }

        bookends_conflicts = [
            {
                'start_time': datetime(2018, 11, 2, 9, 30),
                'end_time': datetime(2018, 11, 2, 10, 10)
            },
            {
                'start_time': datetime(2018, 11, 2, 13, 55),
                'end_time': datetime(2018, 11, 2, 14, 30)
            }
        ]

        expected = [
            {
                'start_time': datetime(2018, 11, 2, 10, 10),
                'end_time': datetime(2018, 11, 2, 13, 55)
            }
        ]

        actual = AppointmentCalendarPage._get_open_block_segments(open_block, bookends_conflicts)
        self.assertEqual(expected, actual)

    def test_bookends_with_middle_conflict_case(self):
        open_block = {
            'start_time': datetime(2018, 11, 2, 10, 0),
            'end_time': datetime(2018, 11, 2, 14, 0)
        }

        one_middle_conflicts = [
            {
                'start_time': datetime(2018, 11, 2, 8, 30),
                'end_time': datetime(2018, 11, 2, 9, 10)
            },
            {
                'start_time': datetime(2018, 11, 2, 9, 30),
                'end_time': datetime(2018, 11, 2, 10, 10)
            },
            {
                'start_time': datetime(2018, 11, 2, 11, 15),
                'end_time': datetime(2018, 11, 2, 12, 30)
            },
            {
                'start_time': datetime(2018, 11, 2, 13, 55),
                'end_time': datetime(2018, 11, 2, 14, 30)
            },
            {
                'start_time': datetime(2018, 11, 2, 14, 30),
                'end_time': datetime(2018, 11, 2, 15, 30)
            }
        ]

        expected = [
            {
                'start_time': datetime(2018, 11, 2, 10, 10),
                'end_time': datetime(2018, 11, 2, 11, 15)
            },
            {
                'start_time': datetime(2018, 11, 2, 12, 30),
                'end_time': datetime(2018, 11, 2, 13, 55)
            }
        ]

        actual = AppointmentCalendarPage._get_open_block_segments(open_block, one_middle_conflicts)
        self.assertEqual(expected, actual)

    def test_bookends_with_mutiple_middle_conflicts(self):
        open_block = {
            'start_time': datetime(2018, 11, 2, 10, 0),
            'end_time': datetime(2018, 11, 2, 14, 0)
        }

        one_middle_conflicts = [
            {
                'start_time': datetime(2018, 11, 2, 8, 30),
                'end_time': datetime(2018, 11, 2, 9, 10)
            },
            {
                'start_time': datetime(2018, 11, 2, 9, 30),
                'end_time': datetime(2018, 11, 2, 10, 10)
            },
            {
                'start_time': datetime(2018, 11, 2, 11, 15),
                'end_time': datetime(2018, 11, 2, 12, 30)
            },
            {
                'start_time': datetime(2018, 11, 2, 12, 45),
                'end_time': datetime(2018, 11, 2, 13, 0)
            },
            {
                'start_time': datetime(2018, 11, 2, 13, 30),
                'end_time': datetime(2018, 11, 2, 13, 50)
            }
        ]

        expected = [
            {
                'start_time': datetime(2018, 11, 2, 10, 10),
                'end_time': datetime(2018, 11, 2, 11, 15)
            },
            {
                'start_time': datetime(2018, 11, 2, 12, 30),
                'end_time': datetime(2018, 11, 2, 12, 45)
            },
            {
                'start_time': datetime(2018, 11, 2, 13, 00),
                'end_time': datetime(2018, 11, 2, 13, 30)
            },
            {
                'start_time': datetime(2018, 11, 2, 13, 50),
                'end_time': datetime(2018, 11, 2, 14, 00)
            }
        ]

        actual = AppointmentCalendarPage._get_open_block_segments(open_block, one_middle_conflicts)
        self.assertEqual(expected, actual)
