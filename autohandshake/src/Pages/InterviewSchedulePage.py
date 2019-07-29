from typing import List

from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.exceptions import NoSuchElementError


class InterviewSchedulePage(Page):
    """The main page for an Interview Schedule."""

    def __init__(self, schedule_id: int, browser: HandshakeBrowser):
        """
        :param type_id: the id of the interview schedule to load
        :type type_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        self._id = schedule_id
        super().__init__(f'{BASE_URL}/interview_schedules/{schedule_id}', browser)

    @Page.require_user_type(UserType.STAFF)
    def get_contact_info(self) -> List[dict]:
        """
        Retrieve the name and email of each person listed under "Contacts" on the interview schedule page.

        Method returns a list of dicts of the form:

        [
            {'name': 'Jane Recruiter', 'email': 'jrec@company.com'},
            {'name': 'John Employer', 'email': 'jemp@company.com'}
        ]

        :return: a list of dicts containing contact info
        """

        contacts = []
        there_are_unprocessed_contacts = True
        i = 1
        email_xpath = '//p[contains(@data-bind, "text: email_address")]'
        close_btn_xpath = '//div[@id="show-contact"]//div[@class="modal-header"]//button[@data-dismiss="modal"]'

        while there_are_unprocessed_contacts:
            contact_link_xpath = f'//p[@data-bind="foreach: contacts"]/a[{i}]'
            try:
                # get contact name
                name = self._browser.get_element_attribute_by_xpath(contact_link_xpath, 'text')
                # open modal and get contact email
                self._browser.click_element_by_xpath(contact_link_xpath)
                self._browser.wait_until_element_exists_by_xpath(email_xpath)
                email = self._browser.get_element_attribute_by_xpath(email_xpath, 'text')
                contacts.append({'name': name, 'email': email})
                # close modal and move onto next contact
                self._browser.wait_until_element_is_clickable_by_xpath(close_btn_xpath)
                self._browser.click_element_by_xpath(close_btn_xpath)
                self._browser.wait_until_element_does_not_exist_by_xpath(
                    '//*[@id="show-contact"]//div[@class="modal-content"]')
                i += 1
            except NoSuchElementError:
                there_are_unprocessed_contacts = False
        return contacts

    def get_reserved_rooms(self):
        """
        Get the number of rooms reserved for the interview schedule.

        :return: the number of rooms reserved for the schedule
        """
        reserved_text = self._browser.get_element_attribute_by_xpath('//span[contains(text(), " reserved")]', 'text')
        return int(reserved_text.split()[0])


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
        self._browser.wait_until_element_exists_by_xpath('//*[@class="property-box"]/h4[text()="Employer"]')
