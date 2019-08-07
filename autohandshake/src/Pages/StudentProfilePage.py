from autohandshake.src.Pages.Page import Page
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.constants import BASE_URL


class StudentProfilePage(Page):
    """
    The old Handshake login page
    """

    def __init__(self, student_id: int, browser: HandshakeBrowser):
        """
        :param student_id: the id of the student whose page to load
        :type student_id: int
        :param browser: a HandshakeBrowser that has not logged in yet
        :type browser: HandshakeBrowser
        """
        self._id = student_id
        super().__init__(f'{BASE_URL}/users/{student_id}', browser)

    @Page.require_user_type(UserType.STAFF)
    def view_as_student(self):
        view_as_btn_xpath = '//a[@href="/users/8534543/view_as"]'
        self._browser.wait_until_element_is_clickable_by_xpath(view_as_btn_xpath)
        self._browser.click_element_by_xpath(view_as_btn_xpath)
        self._browser.wait_until_element_is_clickable_by_xpath('//a[@href="/users/stop_viewing_as"]')
        self._browser.update_constants()

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
        self._browser.wait_until_element_exists_by_xpath(
            '//div[contains(@class, "student-profile-card student-profile-card__actions")]')
