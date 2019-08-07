from autohandshake.src import HandshakeBrowser
from autohandshake.src.Pages.StudentProfilePage import StudentProfilePage
from autohandshake.src.constants import BASE_URL


class ViewAsStudent:
    """
    A sub-session in which the user logs in as a student.

    Should be used as a context manager. Example:
    ::

        with HandshakeSession(school_url, email) as browser:
            with ViewAsStudent(student_id):
                # do something
    """

    def __init__(self, student_id: int, browser: HandshakeBrowser, stay_on_page: bool = False):
        """

        :param student_id: the numeric Handshake id of the student to view as
        :type student_id: int
        :param browser: a logged-in Handshake browser with a STAFF user type
        :type browser: HandshakeBrowser
        :param stay_on_page: whether or not to stay on the same page when logging
                             back out of the "View as Student" session. If False,
                             navigate back to the Handshake homepage when the
                             session is over. Defaults to False.
        :type stay_on_page: bool
        """
        self._id = student_id
        self._browser = browser
        self._stay_on_page = stay_on_page

    def __enter__(self):
        """
        Log in as the specified student.
        """
        profile_page = StudentProfilePage(self._id, self._browser)
        profile_page.view_as_student()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the web browser"""
        self._browser.click_element_by_xpath('//a[@href="/users/stop_viewing_as"]')
        self._browser.update_constants()
        if not self._stay_on_page:
            self._browser.get(BASE_URL)
