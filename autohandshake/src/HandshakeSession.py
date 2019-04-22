from autohandshake.src import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError
from autohandshake.src.Pages.LoginPage import LoginPage
from autohandshake.src.constants import MAX_WAIT_TIME


class HandshakeSession:
    """
    A Handshake browsing session.

    Should be used as a context manager. Example:
    ::

        with HandshakeSession(school_url, email, password) as browser:
            # do something

    IMPORTANT: do not store your Handshake password as plain text under any
    circumstances. I recommend entering your password each time you create a HandshakeSession
    using a GUI or the console, via `getpass <https://docs.python.org/3.7/library/getpass.html>`_ or similar.
    """

    def __init__(self, login_url: str, email: str, password: str,
                 max_wait_time: int = MAX_WAIT_TIME):
        """
        :param login_url: a valid Handshake homepage url of the form
                          "https://[school].joinhandshake.com"
        :type login_url: str
        :param email: a valid handshake admin email
        :type email: str
        :param password: the password associated with the given email
        :type password: str
        :param max_wait_time: the maximum time to wait for something to load
                              before throwing a timeout error
        :type max_wait_time: int
        """
        self._login_url = login_url
        self._email = email
        self._password = password
        self._browser = HandshakeBrowser(max_wait_time=max_wait_time)

    def __enter__(self) -> HandshakeBrowser:
        """
        Open a web browser and log into Handshake, beginning the session

        :returns: a logged-in HandshakeBrowser
        :rtype: HandshakeBrowser
        """
        self._browser.get(self._login_url)
        if self._school_is_invalid():
            raise InvalidURLError('Invalid school in login URL')
        # try to log in via the new style of login page if the old one fails
        login_page = LoginPage(self._login_url, self._browser)
        login_page.login(self._email, self._password)
        self._browser.record_school_id()
        return self._browser

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the web browser"""
        self.close()

    def close(self):
        """Close the Handshake Session.

        To be called if HandshakeSession is *not* used as a context manager.
        """
        self._browser.quit()

    def _school_is_invalid(self) -> bool:
        """
        Determine whether or not the Handshake login URL's school is invalid.

        If the page asks the user to select a school before signing in, that
        means the URL had an invalid school to begin with.

        :return: True if the school is invalid, false otherwise
        :rtype: bool
        """
        return self._browser.element_exists_by_xpath('//span[text()=\'Please '
                                                     'select your school to '
                                                     'sign in.\']')

    def _get_school_id(self) -> int:
        """Once on the homepage after logging in, get the id of the school."""
