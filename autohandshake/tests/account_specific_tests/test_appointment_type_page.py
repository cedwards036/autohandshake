import unittest
from autohandshake.src.Pages.SchoolSettings import AppointmentTypePage
from autohandshake.tests import TestSession

TEST_TYPE_ID = 16097

class TestAppointmentTypePage(unittest.TestCase):

    def test_get_appt_settings(self):

        expected_settings = {
            'id': TEST_TYPE_ID,
            'name': 'Homewood: TEST appointment type',
            'description': 'a malleable appointment type for testing purposes',
            'length': 30,
            'categories': ['Create Documents', 'Find Jobs/Internships/Opportunities'],
            'drop_in_enabled': True,
            'pre_message': 'This is a pre-appointment message',
            'pre_survey': 'Homewood: Pre- Appointment Survey',
            'post_message': 'This is the post-appointment message',
            'post_survey': 'Homewood: 2017 Mock Interview post-appointment survey',
            'staff_survey': 'Homewood: Post-Appointment Staff Survey',
            'school_years': ['Sophomore', 'Senior', 'Doctorate'],
            'cum_gpa_required': True,
            'cum_gpa': 3.5,
            'major_groups': ['major_group: Law', 'major_group: Public Policy',
                             'major_group: Individual Studies', 'indv_major: Applied Economics',
                             'indv_major: Applied Biomedical Engineering',
                             'indv_major: Applied and Computational Mathematics'],
            'colleges': ['Krieger School of Arts & Sciences', 'Whiting School of Engineering'],
            'labels': ['shared: appointments allowed', 'hwd: old appointment type'],
            'career_clusters': ['Homewood: STEM & Innovation', 'Carey Network: Finance']
        }

        with TestSession() as browser:
            type_page = AppointmentTypePage(TEST_TYPE_ID, browser)
            self.assertEqual(expected_settings, type_page.get_settings())