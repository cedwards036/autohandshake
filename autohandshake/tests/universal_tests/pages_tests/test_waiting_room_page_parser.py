import unittest
import datetime
from autohandshake import WaitingRoomPage
from bs4 import BeautifulSoup


class TestWaitingRoomPageParser(unittest.TestCase):

    def test_parse_entry_with_office_location_not_being_created(self):
        check_in_soup = BeautifulSoup("""
        <div class="list-group-item clearfix">
            <div class="pull-right">
                <div>
                    <a class="btn btn-primary"
                        data-bind="click: $parent.check_drop_in_status_and_act, css: { 'btn-primary': status() == 'pending', 'btn-warning': status() != 'pending' }, text: status() == 'pending' ? 'Start Appointment' : 'Being Created'"
                        href="#">Start Appointment</a>
                </div>
                <div class="margin-top center">
                    <a class="text-danger" data-bind="click: $parent.remove_drop_in" href="#">Cancel Drop-in</a>
                </div>
            </div>
            <h3 class="no-margin-top">
                <a data-bind="text: fancy_title, attr: { href: '/users/' + user_id() }" target="_blank"
                    href="/users/8766322">Rachael Gamlin</a>
            </h3>
            <h4 data-bind="text: 'Checked In: ' + Handshake.Helpers.fullStraightDateTime(created_at())">Checked In: Saturday,
                September 22nd 2018 12:24 pm</h4>
            <h4 data-bind="visible: office_location_name(), text: 'Office Location: ' + office_location_name()">Office Location: Homewood AMS Career Connections - 100 Whitehead Hall</h4>
        </div>
        """, 'html.parser')
        expected = {
            'being_created': False,
            'student_id': 8766322,
            'student_name': 'Rachael Gamlin',
            'datetime': datetime.datetime(2018, 9, 22, 12, 24),
            'office_location': 'Homewood AMS Career Connections - 100 Whitehead Hall'
        }

        self.assertEqual(expected, WaitingRoomPage._parse_checkin(check_in_soup))

    def test_parse_entry_with_office_location_being_created(self):
        check_in_soup = BeautifulSoup("""
        <div class="list-group-item clearfix">
            <div class="pull-right">
                <div>
                    <a class="btn btn-warning"
                        data-bind="click: $parent.check_drop_in_status_and_act, css: { 'btn-primary': status() == 'pending', 'btn-warning': status() != 'pending' }, text: status() == 'pending' ? 'Start Appointment' : 'Being Created'"
                        href="#">Being Created</a>
                </div>
                <div class="margin-top center">
                    <a class="text-danger" data-bind="click: $parent.remove_drop_in" href="#">Cancel Drop-in</a>
                </div>
            </div>
            <h3 class="no-margin-top">
                <a data-bind="text: fancy_title, attr: { href: '/users/' + user_id() }" target="_blank"
                    href="/users/1468803">Jon Silveira</a>
            </h3>
            <h4 data-bind="text: 'Checked In: ' + Handshake.Helpers.fullStraightDateTime(created_at())">Checked In: Wednesday,
                October 31st 2018 2:33 pm</h4>
            <h4 data-bind="visible: office_location_name(), text: 'Office Location: ' + office_location_name()"
                style="display: none;">Office Location: null</h4>
        </div>
        """, 'html.parser')
        expected = {
            'being_created': True,
            'student_id': 1468803,
            'student_name': 'Jon Silveira',
            'datetime': datetime.datetime(2018, 10, 31, 14, 33),
            'office_location': None
        }

        self.assertEqual(expected, WaitingRoomPage._parse_checkin(check_in_soup))
