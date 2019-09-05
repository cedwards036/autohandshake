from autohandshake.src.Pages import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL
from autohandshake.src.exceptions import NoSuchElementError
from typing import List
from bs4 import BeautifulSoup


class LabelModal:
    _MODAL_XPATH = '//div[@data-bind="with: selectedLabel"]'

    def __init__(self, browser: HandshakeBrowser, row_idx: int):
        self._browser = browser
        self._row_idx = row_idx

    def __enter__(self):
        ROW_XPATH = f'//tbody[@data-bind="foreach: institution_labels"]/tr[{self._row_idx + 1}]'
        self._browser.click_element_by_xpath(ROW_XPATH)
        self._browser.wait_until_element_is_clickable_by_xpath(self._MODAL_XPATH)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        CLOSE_BTN_XPATH = f'{self._MODAL_XPATH}//button[@class="btn btn-default"]'
        self._browser.click_element_by_xpath(CLOSE_BTN_XPATH)
        self._browser.wait_until_element_does_not_exist_by_xpath(self._MODAL_XPATH)

    def get_usage_counts(self):
        usage_counts = {}
        try:
            table_rows = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
                '//tbody[@data-bind="foreach: type_details"]', 'innerHTML'),
                'html.parser').find_all('tr', recursive=False)
            for row in table_rows:
                usage_counts = self._parse_row(row, usage_counts)
        except NoSuchElementError:
            usage_counts = {'All': 0}
        return usage_counts

    def _parse_row(self, row: BeautifulSoup, usage_counts: dict) -> dict:
        usage_type = row.find('a', {'data-bind': 'text: labellable_type'}).text
        usage_count = int(row.find('a', {'data-bind': 'text: count'}).text)
        usage_counts[usage_type] = usage_count
        return usage_counts


class LabelSettingsPage(Page):

    def __init__(self, browser: HandshakeBrowser):
        """
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        labels_base_url = f'{BASE_URL}/schools/{browser.school_id}/institution_labels'
        url_query = '?ajax=true&query=&category=ManageLabels&page=1&per_page=1000&sort_direction=asc&sort_column=default&followed_only=false&qualified_only=&core_schools_only=false&including_all_facets_in_searches=false'
        super().__init__(labels_base_url + url_query,
                         browser)

    @Page.require_user_type(UserType.STAFF)
    def get_label_data(self) -> List[dict]:
        """
        Get a list of all the school's labels and their usage data.

        :return: a list of label data dicts, of the form:
        ::

            {
                'label_name': 'preferred employer', # the name of the label
                'usage_counts': { # how many times the label has been used in different system modules
                    'Job': 43,
                    'Event': 55,
                    'InterviewSchedule': 23
                },
                'used_for': 'All', # the primary module this label is used for. Labels used for multiple modules are marked 'All'
                'created_by_first_name': 'John', # the first name of the user who created the label
                'created_by_last_name': 'Staffmember', # the last name of the user who created the label
                'label_type': 'normal' # the label type. One of 'normal', 'system' or 'public'
            }
        :rtype: list
        """
        table_rows = BeautifulSoup(self._browser.get_element_attribute_by_xpath(
            '//tbody', 'innerHTML'),
            'html.parser').find_all('tr', recursive=False)
        return self._parse_table(table_rows)

    def _parse_table(self, table_rows: List[BeautifulSoup]) -> List[dict]:
        label_data = []
        for idx, row in enumerate(table_rows):
            label_data.append(self._parse_table_row(row, idx))
        return label_data

    def _parse_table_row(self, row: BeautifulSoup, row_idx: int) -> dict:
        used_for = row.find('a', {'data-bind': 'text: labellable_type_text, click: $parent.searchByLabels'}).text
        return {
            'label_name': row.find('a', {'data-bind': 'text: name, click: $parent.searchByLabels'}).text,
            'usage_counts': self._get_usage_counts(row, row_idx, used_for),
            'used_for': used_for,
            'created_by_first_name': self._get_first_name(row),
            'created_by_last_name': self._get_last_name(row),
            'label_type': row.find('div', {
                'data-bind': 'text: label_type, css: label_type_css, click: $parent.searchByLabels'}).text
        }

    def _get_usage_counts(self, row: BeautifulSoup, row_idx: int, used_for: str) -> dict:
        usage_count = int(row.find('a', {'data-bind': 'text: total_labelled, click: $parent.searchByLabels'}).text)
        if used_for == 'All' and usage_count != 0:
            return self._get_all_usage_counts(row_idx)
        else:
            return {
                used_for: usage_count
            }

    def _get_all_usage_counts(self, row_idx: int) -> dict:
        with LabelModal(self._browser, row_idx) as label_modal:
            return label_modal.get_usage_counts()

    def _get_first_name(self, row: BeautifulSoup):
        first_name = row.find('a', {'data-bind': 'text: first_name, click: $parent.searchByLabels'}).text
        if not first_name:
            return None
        else:
            return first_name

    def _get_last_name(self, row: BeautifulSoup):
        last_name = row.find('a', {'data-bind': 'text: last_name, click: $parent.searchByLabels'}).text
        if not last_name:
            return None
        else:
            return last_name

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
        self._browser.wait_until_element_exists_by_xpath('//tbody[@data-bind="foreach: institution_labels"]/tr')
