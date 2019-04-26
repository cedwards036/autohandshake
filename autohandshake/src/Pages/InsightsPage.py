from autohandshake.src.Pages import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.constants import BASE_URL
from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError, \
    InsufficientPermissionsError
import re
import os
import time
from typing import List
import json
from enum import Enum
from datetime import date

DEFAULT_WAIT_TIME = 300


class FileType(Enum):
    """
    The possible download file types in Insights

            * EXCEL - an excel file with a .xlsx extension
            * TXT - a tab-separated .txt file
            * JSON - a json file with a .json extension
            * HTML - a .html file that can render the data table in a browser
            * MARKDOWN - a .md file that renders the table in markdown
            * PNG - a .png image of the data table
            * CSV - a comma-separated .csv file
    """
    EXCEL = 'xlsx'
    TXT = 'txt'
    JSON = 'json'
    HTML = 'html'
    MARKDOWN = 'md'
    PNG = 'png'
    CSV = 'csv'


class _DownloadModal:
    """An interface to the pop-up modal for downloading Insights files"""

    def __init__(self, browser: HandshakeBrowser):
        """
        Open the download modal on the Insights page

        :param browser: a logged-in HandshakeBrowser on the Insights Page
        :type browser: HandshakeBrowser
        """
        self._browser = browser
        self.is_open = False

    def open(self):
        """Open the insights report download modal box."""
        if not self.is_open:
            self._browser.wait_then_click_element_by_xpath("//i[@class='lk-icon-gear']")
            self._browser.wait_then_click_element_by_xpath("//a[@ng-click='openDownloadDialog()']")
            self._browser.wait_until_element_is_clickable_by_xpath(
                "//div[contains(@class, 'query-download-modal-limit')]")
            # click modal body to bring it into focus, allowing additional actions
            self._browser.click_element_by_xpath("//div[@class='modal-body']")
            self.is_open = True

    def validate_download_modal_is_open(self):
        """Throw an error if the download modal is not open."""
        if not self.is_open:
            raise NoSuchElementError('Insights Download modal box must be open')

    def get_download_file_type(self) -> FileType:
        """
        Get the name of the file type currently selected.

        :return: the name of the file type currently selected
        :rtype: FileType
        """
        self.validate_download_modal_is_open()
        value = self._browser.get_element_attribute_by_xpath(
            "//select[@id='qr-export-modal-format']", "value")
        # values are formatted "string:[value name]." we must remove the first 7 chars
        return FileType(value[7:])

    def set_download_file_type(self, file_type: FileType):
        """
        If the download modal is open, select the file type to download.

        :param file_type: the name of a valid file type to download from insights
        :type file_type: FileType
        """
        self.validate_download_modal_is_open()
        type_label_lookup = {
            FileType.TXT: 'TXT (tab-separated values)',
            FileType.EXCEL: 'Excel Spreadsheet (Excel 2007 or later)',
            FileType.CSV: 'CSV',
            FileType.JSON: 'JSON',
            FileType.HTML: 'HTML',
            FileType.MARKDOWN: 'Markdown',
            FileType.PNG: 'PNG (Image of Visualization)'
        }
        try:
            type_label = type_label_lookup[file_type]
            self._browser.click_element_by_xpath(f"//option[@label='{type_label}']")
        except KeyError:
            raise ValueError(f'Invalid file type: "{file_type}"')

    def set_limit_to_all_results(self, remove_sorts: bool = False):
        """
        If the download modal is open, set the download limit to "all results,"
        optionally removing sorts on the query for increased performance.

        :param remove_sorts: whether or not to remove sorts on the query
        :type remove_sorts: bool
        """
        self.validate_download_modal_is_open()
        all_results_radio_xpath = "//input[@name='qr-export-modal-limit' and @value='all']"
        remove_sorts_xpath = "//input[@ng-model='queryDownloadController.runUnsorted']"
        time.sleep(0.1)  # account for unknown, inconsistent timing error that prevents clicking
        try:
            self._browser.wait_until_element_is_clickable_by_xpath(all_results_radio_xpath)
            self._browser.click_element_by_xpath(all_results_radio_xpath)
            if remove_sorts:
                self._browser.wait_until_element_is_clickable_by_xpath(remove_sorts_xpath)
                self._browser.click_element_by_xpath(remove_sorts_xpath)
        except NoSuchElementError:
            raise InsufficientPermissionsError('You do not have permission '
                                               'to download all results')

    def set_custom_limit(self, limit: int):
        """
        If the download modal is open, set the download limit to a custom number
        specified by "limit"

        :param limit: the custom download limit
        :type limit: int
        """
        self.validate_download_modal_is_open()
        custom_limit_radio_xpath = "//input[@name='qr-export-modal-limit' and @value='custom']"
        custom_limit_value_xpath = "//input[@name='customExportLimit']"
        time.sleep(0.1)  # account for unknown, inconsistent timing error that prevents clicking
        self._browser.wait_until_element_is_clickable_by_xpath(custom_limit_radio_xpath)
        self._browser.click_element_by_xpath(custom_limit_radio_xpath)
        self._browser.wait_until_element_is_clickable_by_xpath(custom_limit_value_xpath)
        self._browser.send_text_to_element_by_xpath(custom_limit_value_xpath, str(limit))

    def get_file_name(self) -> str:
        """
        If the download modal is open, get the file name of the file to be
        downloaded.

        :returns: the name of the file to be downloaded
        :rtype: str
        """
        self.validate_download_modal_is_open()
        file_name_xpath = "//input[@name='customExportFilename']"
        self._browser.wait_until_element_exists_by_xpath(file_name_xpath)
        return self._browser.get_element_attribute_by_xpath(file_name_xpath, 'value')

    def set_file_name(self, file_name: str):
        """
        If the download modal is open, set the file name of the file to be
        downloaded.

        :param file_name: the name of the file to be downloaded
        :type file_name: str
        """
        self.validate_download_modal_is_open()
        file_name_xpath = "//input[@name='customExportFilename']"
        if not file_name:
            raise ValueError('File name cannot be null or ""')
        self._browser.wait_until_element_exists_by_xpath(file_name_xpath)
        file_name = self.ensure_file_name_has_correct_extension(file_name)
        self._browser.send_text_to_element_by_xpath(file_name_xpath, file_name)

    def click_download_button(self, download_dir: str, max_wait_time: int = DEFAULT_WAIT_TIME) -> str:
        """
        If the download modal is open, download the Insights report

        :param download_dir: the directory into which Insights will download the
                             file. This is used to confirm that the file
                             downloaded successfully, *not* to tell Insights
                             where to download the file (Insights has no power
                             over that).
        :type download_dir: str
        :param max_wait_time: the maximum amount of time to wait for the file to
                              download without throwing an error
        :type max_wait_time: int
        :return: the full file path of the downloaded file
        :rtype: str
        """
        self.validate_download_modal_is_open()
        file_name = self.get_file_name()
        file_path = os.path.join(download_dir, file_name)
        self._browser.click_element_by_xpath("//button[@id='qr-export-modal-download']")
        self._confirm_file_downloaded(file_path, max_wait_time)
        self.is_open = False
        return file_path

    def click_open_in_browser(self) -> List[dict]:
        """
        If the download modal is open, open the data report in the browser in a
        new tab.

        :returns: a python list of dicts representing the data generated by Insights
        :rtype: list
        """
        valid_file_types = [FileType.JSON]
        if not self.get_download_file_type() in valid_file_types:
            raise RuntimeError("Getting data in browser is only available for the JSON file type at this time")
        self.validate_download_modal_is_open()
        self._browser.click_element_by_xpath("//button[@id='qr-export-modal-open']")
        self._browser.switch_to_new_tab()
        self._browser.wait_until_element_exists_by_xpath("//pre")
        raw_text = self._browser.get_element_attribute_by_xpath("//pre", "text")
        self._browser.return_to_main_tab()
        self.is_open = False
        return json.loads(raw_text)

    @staticmethod
    def _confirm_file_downloaded(file_path, wait_time):
        """
        Confirm that the file at the given file path has downloaded successfully.

        Throw an error if the file still does not exists when the given wait time
        is up

        :param file_path: the expected file path of the downloading file
        :type file_path: str
        :param wait_time: the maximum time to wait for the file to download
        :type wait_time: integer
        """
        start_time = time.time()
        time_to_stop = start_time + wait_time
        while time.time() <= time_to_stop:
            time.sleep(0.5)
            if os.path.exists(file_path):
                return

        raise RuntimeError('File did not download in time')

    def ensure_file_name_has_correct_extension(self, file_name) -> str:
        """Make sure the file name has the correct extension for the selected file type"""
        file_type = self.get_download_file_type()
        if file_name[(-1) * len(str(file_type.value)):] != file_type.value:
            file_name = file_name + '.' + file_type.value
        return file_name


class InsightsPage(Page):
    """Handshake's custom data reporting page (powered by Looker)"""

    def __init__(self, url_string: str, browser: HandshakeBrowser):
        """
        :param url_string: either a full insights URL or just the alphanumeric
                           query string specifying the exact report
        :type url_string: str
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(url_string, browser)
        if self._browser.element_exists_by_xpath(
                "//span[text()='Select some dimensions or measures.' and @aria-hidden='false']"):
            raise InvalidURLError('Insights URL has no dimensions or measures selected')
        self.modal = _DownloadModal(self._browser)

    def get_data(self) -> List[dict]:
        """Get a JSON-like list of dict representation of the Insights report's data

        :returns: the Insight report's data in list-of-dict/JSON-like format
        :rtype: list
        """
        self.modal.open()
        self.modal.set_download_file_type(FileType.JSON)
        try:
            self.modal.set_limit_to_all_results(remove_sorts=True)
        except InsufficientPermissionsError:
            pass
            # keep limit at "Results in Table" if "All Results" is not available
        return self.modal.click_open_in_browser()

    def download_file(self, download_dir: str, file_name: str = None, file_type: FileType = FileType.CSV,
                      max_wait_time: int = DEFAULT_WAIT_TIME) -> str:
        """Download the Insights report's data in a file of the specified type

        :param file_type: the type of file to download
        :type file_type: FileType
        :param download_dir: the directory into which Insights will download the
                             file. This is used to confirm that the file
                             downloaded successfully, *not* to tell Insights
                             where to download the file (Insights has no power
                             over that).
        :type download_dir: str
        :param file_name: the name of the file to download. If None, default to
                          Handshake's standard naming of Insights files
        :type file_name: str
        :param max_wait_time: the maximum amount of time to wait for the file to
                              download without throwing an error
        :type max_wait_time: int
        :returns: the filepath of the newly-downloaded file
        :rtype: str
        """
        self.modal.open()
        self.modal.set_download_file_type(file_type)
        if file_name:
            self.modal.set_file_name(file_name)
        try:
            self.modal.set_limit_to_all_results(remove_sorts=True)
        except InsufficientPermissionsError:
            pass
            # keep limit at "Results in Table" if "All Results" is not available
        return self.modal.click_download_button(download_dir, max_wait_time)

    def set_date_range_filter(self, field_category: str, field_title: str,
                              start_date: date, end_date: date):
        """
        Set a date range filter on the Insights report to the given start and end date.

        Insights date filters are identified by a two-part name: the first part
        indicates the "category" or subject matter the date refers to, and the
        second part indicates the specific date field on that category.

        For example: the filter for the start date of an appointment is called
        "Appointments Start Date Date." In the Insights filter box, this title
        appears with the "Start Date Date" part in bold and the "Appointments"
        part in regular type. In this case "Appointments" is the field_category,
        and "Start Date Date" is the field_title. This methods requires both
        parts of the name in order to apply the given start and end dates to the
        correct filter.

        IMPORTANT: at this time, this method only works on date range filters
        that follow the form "[Category] [Title] is in range [start] until (before) [end]."
        The method does not work on month or time filters, or on filters that do
        not represent a range between two time-less dates. Also, the filter must
        already exist in the Insights page; this method will not create a filter,
        merely modify the dates of an existing one.

        :param field_category: the date filter's category name (see method description)
        :type field_category: str
        :param field_title: the date filter's title (see method description)
        :type field_title: str
        :param start_date: the start date to use in the filter
        :type start_date: date
        :param end_date: the end date to use in the filter. IMPORTANT: Handshake
                         date ranges go *up to but not including* the end date,
                         so a filter from 1/15/19 to 1/30/19 will NOT include any
                         data from 1/30/19, for example.
        :type end_date: date
        """
        ENTER_KEY = u'\ue007'
        BACKSPACE_KEY = u'\u0008'
        start_date_str = self._format_date(start_date)
        end_date_str = self._format_date(end_date)

        date_inputs_xpath = '//tr[@class="filter ng-scope"][.//span[@class="' \
                            'ng-binding" and text()="{}"][../' \
                            'strong/text()="{}"]]//span[{}]/span/input'
        start_xpath = date_inputs_xpath.format(field_category, field_title, 2)
        end_xpath = date_inputs_xpath.format(field_category, field_title, 3)
        self._browser.send_text_to_element_by_xpath(start_xpath, (BACKSPACE_KEY * 10) + start_date_str + ENTER_KEY * 2)
        self._browser.send_text_to_element_by_xpath(end_xpath, (BACKSPACE_KEY * 10) + end_date_str + ENTER_KEY * 2)

    def _validate_url(self, url):
        """
        Ensure that url string given is either a valid Insights URL or a valid
        Insights query string.

        :param url: the url to validate
        :type url: str
        """
        try:  # try full URL match
            re.match(f'^{BASE_URL}' + r'/analytics/explore_embed\?insights_page=[a-zA-Z0-9_]+(=){0,2}$', url) \
                .group(0)
        except AttributeError:
            try:  # try query parameter match
                re.match(r'^[a-zA-Z0-9_]+(=){0,2}$', url) \
                    .group(0)
            except AttributeError:
                raise InvalidURLError()

    def _wait_until_page_is_loaded(self):
        """Wait until the page has finished loading."""
        self._switch_to_looker_iframe()

    def _switch_to_looker_iframe(self):
        """Bring the Looker iframe into focus on the insights page"""
        exists_once_iframe_in_focus = "//i[@class='lk-icon-gear']"
        if not self._browser.element_exists_by_xpath(exists_once_iframe_in_focus):
            if self._browser.element_exists_by_xpath("//div[@style='display: none']"):
                raise InvalidURLError("Insights query string is malformed")

            iframe_xpath = "//iframe[@id='insights-iframe']"
            self._browser.wait_until_element_exists_by_xpath(iframe_xpath)
            self._browser.switch_to_frame_by_xpath(iframe_xpath)

            if self._browser.element_exists_by_xpath("//div[@class='error-http-status-code']"):
                raise InvalidURLError("Insights query string is malformed")

            self._browser.wait_until_element_exists_by_xpath(exists_once_iframe_in_focus)

    @staticmethod
    def _format_date(date: date) -> str:
        """
        Format the given date as a string of the form yyyy-mm-dd.

        :param date: the date to format
        :type date: date
        :return: a date string in the form yyyy-mm-dd
        :rtype: str
        """
        return date.strftime('%Y-%m-%d')
