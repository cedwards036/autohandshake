import unittest
from autohandshake.src.Pages import AppointmentTypesListPage
from autohandshake.tests import TestSession


class TestAppointmentTypesListPage(unittest.TestCase):
    maxDiff = None

    def test_get_type_ids(self):
        with TestSession() as browser:
            types_page = AppointmentTypesListPage(browser)
            type_ids = types_page.get_type_ids()
            self.assertEqual(20930, type_ids[0])
            self.assertEqual(18406, type_ids[2])
            self.assertEqual(20932, type_ids[7])

    def test_get_type_settings(self):
        expected = [
            {
                'id': 20930,
                'name': 'Carey: Networking (30 Minutes)',
                'description': 'Strategize your approach to building your professional network and polish your networking skills.',
                'length': 30,
                'categories': ['Find Jobs/Internships/Opportunities'],
                'drop_in_enabled': True,
                'pre_message': 'Due to our staff size, we have a strict no-show policy for both in-person and virtual appointments. Please plan to arrive five minutes prior to your scheduled appointment.  If you cannot make your appointment, please cancel as soon as possible. You may cancel your appointment in Handshake up to 12 hours before your appointment date.  After 12 hours, you must contact our office at carey.careerdevelopment@jhu.edu or 410-234-9270 to cancel. For appointments at the Harbor East location, enter through the Carey Business School doors and go to the front desk. Explain that you have a coaching appointment and give the attendant the name of your Career Coach.  For appointments at the DC location, go to the Bernstein Offit Building (BOB) 1717 Massachusetts Ave, 8th floor.  We do not validate parking at the DC or Harbor East locations. In addition to the school\'s garage parking, local garages and street parking are available.',
                'pre_survey': 'Carey: Pre Appointment Survey',
                'post_message': 'To help us better assist you in the future, please take a moment to complete the attached brief survey.  We also want to celebrate your success and tailor career search strategies unique to your experience and needs. Please be sure to update us on your job interviews or offers by sending an email to carey.careerdevelopment@jhu.edu.',
                'post_survey': 'Carey: Post Appointment Survey',
                'staff_survey': None,
                'school_years': None,
                'cum_gpa_required': False,
                'cum_gpa': None,
                'major_groups': None,
                'colleges': None,
                'labels': ['system gen: dual degree cbs', 'temp label: dual degree cbs', 'system gen: cbs'],
                'career_clusters': None
            },
            {
                'id': 9022,
                'name': 'Homewood: Consulting - Internships (Paid & Unpaid) Search Strategies',
                'description': 'Devise a plan to search for your internship opportunities and use them to experience the professional world, build a network and expand your skills.',
                'length': 30,
                'categories': ['Find Jobs/Internships/Opportunities'],
                'drop_in_enabled': False,
                'pre_message': """Thank you for making an appointment with the Johns Hopkins Career Center.  

To make the most of your 30 minute appointment, be prepared to share your main goals for your appointment with your coach.

To learn more about the ethical standards (www.naceweb.org/career-development/organizational-structure/principles-for-ethical-professional-practice/) and professional principles (www.naceweb.org/career-development/organizational-structure/principles-for-professional-practice/#careerservices) that guide our career coaching practice, visit the websites listed. 

Please note where your appointment is happening (Career Center, virtually, etc.). If you are unable to attend your appointment or will be more than 10 minutes late, please call the Career Center 410/516-8056 to cancel your appointment.  

Appointment times are held for 10 minutes only. After that time, you will be labeled as a “no show” in Handshake. After 3 “no-shows” in one fiscal year (July 1-June 30), you will lose the ability to make another appointment for the remainder of the fiscal year. 

Feel free to contact the Career Center with any questions.

We look forward to speaking with you!

Johns Hopkins Career Center
Garland Hall, Suite 389
Tel: 410-516-8056
career@jhu.edu\n""",
                'pre_survey': None,
                'post_message': 'The Career Center is dedicated to improving the services it offers students including individual coaching sessions. Your input is very important to this process. Thank you for completing a short 4-question survey on your recent coaching session. Please contact the Career Center if you have any questions at career@jhu.edu.',
                'post_survey': 'Homewood: 2017 Internship Search post-appointment survey',
                'staff_survey': 'Homewood: Post-Appointment Staff Survey',
                'school_years': ['Sophomore', 'Junior', 'Senior'],
                'cum_gpa_required': False,
                'cum_gpa': None,
                'major_groups': None,
                'colleges': None,
                'labels': ['hwd: old appointment type'],
                'career_clusters': ['Homewood: Consulting']
            }
        ]

        with TestSession() as browser:
            types_page = AppointmentTypesListPage(browser)
            type_settings = types_page.get_type_settings(how_many=2)
            self.assertListEqual(expected, type_settings)
