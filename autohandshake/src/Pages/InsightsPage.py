from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError, NoSuchElementError, \
    InsufficientPermissionsError
import re


class InsightsPage(Page):
    """The overview settings page listing all appointment types"""

    def __init__(self, url_string: str, browser: HandshakeBrowser):
        """
        Load the insights page specified by either the full URL or the query string

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
        self.download_dialogue_is_open = False

    def open_download_dialogue(self):
        """Open the insights report download dialogue box."""
        self._browser.click_element_by_xpath("//i[@class='lk-icon-gear']")
        self._browser.click_element_by_xpath("//a[@ng-click='openDownloadDialog()']")
        self._browser.wait_until_element_is_clickable_by_xpath("//div[contains(@class, 'query-download-modal-limit')]")
        # click modal body to bring it into focus, allowing additional actions
        self._browser.click_element_by_xpath("//div[@class='modal-body']")
        self.download_dialogue_is_open = True

    def validate_download_dialogue_is_open(self):
        """Throw an error if the download dialogue is not open."""
        if not self.download_dialogue_is_open:
            raise NoSuchElementError('Insights Download dialogue box must be open')

    def select_download_file_type(self, file_type: str):
        """
        If the download dialogue is open, select the file type to download.

        Valid file types include:
         - "txt," "text," or "tab-separated" for a tab-separated values file
         - "excel" for an excel file
         - "csv" for a comma-separated values file
         - "json" for a JSON file
         - "html" for an HTML file
         - "markdown" for a markdown file
         - "png" for a png image of the insights report

        :param file_type: the name of a valid file type to download from insights
        :type file_type: str
        """
        self.validate_download_dialogue_is_open()
        type_label_lookup = {
            'txt': 'TXT (tab-separated values)',
            'text': 'TXT (tab-separated values)',
            'tab-separated': 'TXT (tab-separated values)',
            'excel': 'Excel Spreadsheet (Excel 2007 or later)',
            'csv': 'CSV',
            'json': 'JSON',
            'html': 'HTML',
            'markdown': 'Markdown',
            'png': 'PNG (Image of Visualization)'
        }
        file_type = file_type.lower().strip()
        try:
            type_label = type_label_lookup[file_type]
            self._browser.click_element_by_xpath(f"//option[@label='{type_label}']")
        except KeyError:
            raise ValueError(f'Invalid file type: "{file_type}"')

    def set_limit_to_all_results(self, remove_sorts: bool = False):
        """
        If the download dialogue is open, set the download limit to "all results,"
        optionally removing sorts on the query for increased performance.

        :param remove_sorts: whether or not to remove sorts on the query
        :type remove_sorts: bool
        """
        self.validate_download_dialogue_is_open()
        all_results_radio_xpath = "//input[@name='qr-export-modal-limit' and @value='all']"
        remove_sorts_xpath = "//input[@ng-model='queryDownloadController.runUnsorted']"
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
        If the download dialogue is open, set the download limit to a custom number
        specified by "limit"

        :param limit: the custom download limit
        :type limit: int
        """
        self.validate_download_dialogue_is_open()
        custom_limit_radio_xpath = "//input[@name='qr-export-modal-limit' and @value='custom']"
        custom_limit_value_xpath = "//input[@name='customExportLimit']"
        self._browser.wait_until_element_is_clickable_by_xpath(custom_limit_radio_xpath)
        self._browser.click_element_by_xpath(custom_limit_radio_xpath)
        self._browser.send_text_to_element_by_xpath(custom_limit_value_xpath, str(limit))

    def set_file_name(self, file_name: str):
        """
        If the download dialogue is open, set the file name of the file to be
        downloaded.

        :param file_name: the name of the file to be downloaded
        :type file_name: str
        """
        self.validate_download_dialogue_is_open()
        file_name_xpath = "//input[@name='customExportFilename']"
        if not file_name:
            raise ValueError('File name cannot be null or ""')
        self._browser.wait_until_element_exists_by_xpath(file_name_xpath)
        self._browser.send_text_to_element_by_xpath(file_name_xpath, file_name)

    def validate_url(self, url):
        """
        Ensure that url string given is either a valid Insights URL or a valid
        Insights query string.

        :param url: the url to validate
        :type url: str
        """
        try:  # try full URL match
            re.match(fr'^{BASE_URL}/analytics/explore_embed\?insights_page=[a-zA-Z0-9_]+(==)?$', url) \
                .group(0)
        except AttributeError:
            try:  # try query parameter match
                re.match(r'^[a-zA-Z0-9_]+(==)?$', url) \
                    .group(0)
            except AttributeError:
                raise InvalidURLError()

    def wait_until_page_is_loaded(self):
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
