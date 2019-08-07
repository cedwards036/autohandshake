from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL


class CareerInterestsPage(Page):
    """A settings page for a single student's career interests.

    Only accessible while logged in as a student.
    """

    def __init__(self, student_id: int, browser: HandshakeBrowser):
        """
        :param student_id: the id of the student whose career interests page you are to visit
        :type student_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        self._id = student_id
        super().__init__(f'{BASE_URL}/users/{student_id}/career_interests', browser)

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
        self._browser.wait_until_element_exists_by_xpath("//div[@data-bind='foreach: custom_job_interest_options']")
