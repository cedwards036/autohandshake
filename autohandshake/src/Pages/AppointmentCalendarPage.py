from autohandshake.src.Pages import Page
from autohandshake.src.exceptions import NoSuchElementError
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from dateutil.parser import parse
from bs4 import BeautifulSoup
from typing import List, Generator
import datetime
import re


class AppointmentCalendarPage(Page):
    """
    The calendar view of staff appointments.

    Can only be accessed with a career services/admin-type account.
    """

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/appointments/calendar', browser)

    @Page.require_user_type(UserType.STAFF)
    def go_to_date(self, date: datetime.date):
        """Using the calendar's datepicker, navigate to the specified date

        :param date: the date to which to navigate on the calendar
        :type date: date
        """
        OPEN_DATEPICKER_XPATH = "//span[@id='date-button']"
        DATEPICKER_CALENDAR_XPATH = "//div[@class='datetimepicker datetimepicker-inline']"
        DAYS_TO_MONTHS_SWITCH_XPATH = "//div[@class='datetimepicker-days']//th[@class='switch']"
        MONTHS_TO_YEARS_SWITCH_XPATH = "//div[@class='datetimepicker-months']//th[@class='switch']"
        YEAR_XPATH = f"//span[text()='{date.year}']"
        MONTH_XPATH = f"//span[text()='{date.strftime('%b')}']"
        DAY_XPATH = f"//td[text()='{date.day}' and @class='day']"
        LOADING_SPINNER_XPATH = '//span[@class="ladda-spinner"]/div'

        # open datepicker and prepare to select date
        self._browser.wait_then_click_element_by_xpath(OPEN_DATEPICKER_XPATH)
        self._browser.wait_until_element_exists_by_xpath(DATEPICKER_CALENDAR_XPATH)
        self._browser.wait_then_click_element_by_xpath(DAYS_TO_MONTHS_SWITCH_XPATH)
        self._browser.wait_then_click_element_by_xpath(MONTHS_TO_YEARS_SWITCH_XPATH)

        # select year, month, and day, in that order
        self._browser.click_element_by_xpath(YEAR_XPATH)
        self._browser.click_element_by_xpath(MONTH_XPATH)
        self._browser.click_element_by_xpath(DAY_XPATH)

        # wait for new calendar date to finish loading
        self._browser.wait_until_element_does_not_exist_by_xpath(LOADING_SPINNER_XPATH)

    @Page.require_user_type(UserType.STAFF)
    def get_unfilled_blocks(self, start_date: datetime.date, end_date: datetime.date = None,
                            include_mediums: bool = False) -> List[dict]:
        """
        Get a list of unfilled appointment block data for the days from
        start_date up to (but not including) end_date.

        The method returns a list of appointment block dicts of the form:
        ::

            {
                'start_time': datetime.datetime(2019, 3, 7, 9, 30), # block start time
                'end_time': datetime.datetime(2019, 3, 7, 10, 30), # block end time
                'length': 60, # difference in minutes between start time and end time
                'status': 'unfilled', # status of the appointment
                'staff_name': 'Jane Coach', # the name of the staff member associated with the block
                'mediums': ['in-person', 'virtual'] # [OPTIONAL] the list of possible mediums for the open block
            }

        :param start_date: the start date of the date range from which to pull the data
        :type start_date: date
        :param end_date: the end date of the date range from which to pull the data.
                         If no end date is specified, only pull data for start_date
        :type end_date: date
        :param include_mediums: whether or not to include the appointment block mediums
                                in the data. Including the medium significantly
                                increases the time required to pull the data.
        :type include_mediums: bool
        :return: a list of appointment block dicts
        :rtype: list
        """
        if end_date:
            results = []
            for date in self._daterange(start_date, end_date):
                results += self._get_unfilled_on_one_date(date, include_mediums=include_mediums)
        else:
            results = self._get_unfilled_on_one_date(start_date, include_mediums=include_mediums)

        return results

    def _validate_url(self, url):
        """
        Ensure that the given URL is a valid URL.

        Since the URL is not entered by the user, it is always valid.

        :param url: the url to validate
        :type url: str
        """
        return

    def _wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""

        # altering the window size is necessary because the calendar's responsive
        # design only triggers upon resizing, not on initial load
        self._browser.maximize_window()
        self._browser.wait_until_element_exists_by_xpath("//div[@class='appointment-calendar-staff-container']")

    def _get_unfilled_on_one_date(self, date: datetime.date, include_mediums: bool = False) -> List[dict]:
        """
        Get unfilled block data for a single date.

        :param date: the date for which to get data
        :type date: date
        :param include_mediums: bool
        :type include_mediums: whether or not to include appointment mediums in the data
        :return: a list of unfilled appointment block data dicts
        :rtype: list
        """

        # the height of a calendar block increases by 3 pixels for each additional
        # minute of length
        PIXELS_PER_MINUTE = 3
        DATE_STR = date.strftime("%m/%d/%y")

        self.go_to_date(date)

        staff_header = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            "//div[@class='appointment-calendar-staff-container']", "innerHTML"),
            'html.parser')

        appt_grid = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            "//div[@class='appointment-calendar-grid-container']", "innerHTML"),
            'html.parser')

        # Populate ordered list with staff as they appear in the header
        staff = []
        for link in staff_header.findAll('a'):
            staff.append({
                'name': link.text,
                'blocks': {
                    'available': [],
                    'appointments': [],
                    'blocked': [],
                }
            })

        # for each staff column in the calendar...
        for column_index, column in enumerate(appt_grid.findAll(
                'div', 'appointment-calendar-advisor-data')):

            # capture all available, appointment, and unavailable blocks
            available_blocks = column.findAll(lambda x:
                                              x.name == 'div' and
                                              'appointment-block' in x.get('class', []) and
                                              not 'unavailable' in x['class'])

            appointment_blocks = column.findAll('div', 'appointment')
            unavailable_blocks = column.findAll('div', 'unavailable')

            # Capture "Available" blocks
            for block_index, block in enumerate(available_blocks):
                block_start_time = parse(block['data-time'][:-6])
                block_height = int(re.search("height: (\d+)px", block['style']).group(1))
                block_length = block_height / PIXELS_PER_MINUTE
                block_end_time = block_start_time + datetime.timedelta(minutes=block_length)
                staff[column_index]['blocks']['available'].append({
                    'start_time': block_start_time,
                    'end_time': block_end_time,
                    'x_idx': column_index + 1,
                    'y_idx': block_index + 1
                })

            # Capture "Appointment" blocks
            for appt_block in appointment_blocks:
                appt_time_text = appt_block.find('div', 'timing-information').text
                appt_start_time = parse(DATE_STR + ' ' + re.search('^(\d+:\d+ [a-z]+)', appt_time_text).group(1))
                appt_end_time = parse(DATE_STR + ' ' + re.search('(\d+:\d+ [a-z]+)$', appt_time_text).group(1))

                staff[column_index]['blocks']['appointments'].append({
                    'start_time': appt_start_time,
                    'end_time': appt_end_time,
                })

            # Capture "Unavailable" blocks
            for unavail_block in unavailable_blocks:
                block_start_time = parse(unavail_block['data-time'][:-6])
                block_height = int(re.search("height: (\d+)px", unavail_block['style']).group(1))
                block_length = block_height / PIXELS_PER_MINUTE
                block_end_time = block_start_time + datetime.timedelta(minutes=block_length)

                staff[column_index]['blocks']['blocked'].append({
                    'start_time': block_start_time,
                    'end_time': block_end_time
                })

        # cross reference available, unavailable, and appointment blocks to
        # determine unfilled time ranges
        unfilled_appt_list = []

        for staff_member in staff:
            all_conflicts = staff_member['blocks']['appointments'] + staff_member['blocks']['blocked']
            all_open = staff_member['blocks']['available'][:]
            for open_block in all_open:

                # break each open block up into its constituent open segments that are not covered by unavailable or appt blocks
                open_segments = self._get_open_block_segments(open_block, all_conflicts)
                for open_segment in open_segments:
                    unfilled_block = {
                        'start_time': open_segment['start_time'],
                        'end_time': open_segment['end_time'],
                        'length': int((open_segment['end_time'] - open_segment['start_time']).total_seconds() / 60),
                        'status': 'unfilled',
                        'staff_name': staff_member['name'],
                    }
                    if include_mediums:
                        unfilled_block['mediums'] = self._get_appt_mediums(open_block['x_idx'],
                                                                           open_block['y_idx'])
                    unfilled_appt_list.append(unfilled_block)

        return unfilled_appt_list

    @staticmethod
    def _get_open_block_segments(open_block: dict, conflict_blocks: list) -> List[dict]:
        """
        Compare the given block with all possible conflict blocks and return the
        truly open segments of the original block.

        For example, if the open block stretches from 10 - 12, and there are conflicts
        from 9:50 - 10:10, 10:30 - 11:00, and 11:30-12:30, then this method would
        return a list of two open blocks: from 10:10 to 10:30 and from 11:00 to 11:30.

        :param open_block: an available calendar block
        :type open_block: dict
        :param conflict_blocks: a list of all unavailable calendar blocks
        :type conflict_blocks: list
        :return: a list of all remaining available segments of the open_block
        :rtype: list
        """
        open_segments = [open_block]
        for conflict in conflict_blocks:
            for segment in open_segments:
                # case where availability block is completely consumed by conflict block
                if conflict['start_time'] <= segment['start_time'] and \
                        conflict['end_time'] >= segment['end_time']:
                    open_segments.remove(segment)

                if conflict['start_time'] <= segment['start_time'] and \
                        conflict['end_time'] > segment['start_time'] and \
                        conflict['end_time'] < segment['end_time']:
                    segment['start_time'] = conflict['end_time']

                if conflict['start_time'] > segment['start_time'] and \
                        conflict['start_time'] < segment['end_time'] and \
                        conflict['end_time'] >= segment['end_time']:
                    segment['end_time'] = conflict['start_time']

                if conflict['start_time'] > segment['start_time'] and \
                        conflict['end_time'] < segment['end_time']:
                    open_segments.remove(segment)

                    first_half = dict(segment)
                    first_half['end_time'] = conflict['start_time']
                    open_segments.append(first_half)

                    second_half = dict(segment)
                    second_half['start_time'] = conflict['end_time']
                    second_half['end_time'] = segment['end_time']
                    open_segments.append(second_half)

        return open_segments

    def _get_appt_mediums(self, col_num: int, block_num: int) -> List[str]:
        """
        Get the appointment mediums for a single available block

        :param col_num: the block's calendar column number
        :type col_num: int
        :param block_num: the block's index within the column
        :type block_num: int
        :return: a list of the block's mediums
        :rtype: list
        """
        BLOCK_XPATH = f'//div[@class="appointment-calendar-advisor-data"]' \
            f'[{col_num}]/div[@class="appointment-block clickable"][{block_num}]'
        EDIT_ICON_XPATH = f"{BLOCK_XPATH}//*[contains(@class,'edit-icon')]"
        MEDIUMS_XPATH = '//div[@id="s2id_appointment-medium"]/ul/li/div'
        MODAL_XPATH = "//div[contains(@class, 'edit-appointment-block-popover')]"
        CLOSE_MODAL_XPATH = f'{MODAL_XPATH}//*[contains(@class, "btn-primary")]'
        LOADING_SPINNER_XPATH = '//span[@class="ladda-spinner"]/div'

        try:
            try:
                self._browser.click_element_by_xpath(EDIT_ICON_XPATH)
            except:
                # open modal using javascript to account for "element not clickable at (x, y)" error
                self._browser.execute_script_on_element_by_xpath('arguments[0].click()',
                                                                 EDIT_ICON_XPATH)
            self._browser.wait_until_element_exists_by_xpath(MODAL_XPATH)
            # capture the appointment mediums
            mediums = self._browser.get_elements_attribute_by_xpath(MEDIUMS_XPATH,
                                                                    'innerHTML')
        except NoSuchElementError:
            mediums = []

        # close the modal
        self._browser.wait_then_click_element_by_xpath(CLOSE_MODAL_XPATH)

        self._browser.wait_until_element_does_not_exist_by_xpath(
            MODAL_XPATH)
        self._browser.wait_until_element_does_not_exist_by_xpath(
            LOADING_SPINNER_XPATH)

        return mediums

    @staticmethod
    def _daterange(start_date: datetime.date,
                   end_date: datetime.date) -> Generator[datetime.date, None, None]:
        """
        Create a generator that yeilds dates from the start date up to (but not
        including) the end date.

        :param start_date: the start date of the range
        :type start_date: datetime.date
        :param end_date: the end date of the range
        :type end_date: datetime.date
        :return: the dates in between start_date and end_date
        :rtype: datetime.date
        """
        for n in range(int(((end_date - start_date).days))):
            yield start_date + datetime.timedelta(n)
