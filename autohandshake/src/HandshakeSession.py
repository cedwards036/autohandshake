from autohandshake.src import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError, InvalidPasswordError
from autohandshake.src.Pages.LoginPage import LoginPage
from autohandshake.src.constants import MAX_WAIT_TIME
import keyring


class HandshakeSession:
    """
    A Handshake browsing session.

    Should be used as a context manager. Example:
    ::

        with HandshakeSession(school_url, email) as browser:
            # do something

    """

    def __init__(self, login_url: str, email: str, password: str = None, max_wait_time: int = MAX_WAIT_TIME,
                 chromedriver_path=None, download_dir: str = None):
        """
        :param login_url: a valid Handshake homepage url of the form
                          "https://[school].joinhandshake.com"
        :type login_url: str
        :param email: a valid handshake admin email
        :type email: str
        :param password: the password associated with the given email. If
                         password is not specified, HandshakeSession will instead
                         look for a password associated with the given login_url
                         and email within the machine's default password manager
                         (e.g. Windows Credential Manager, macOS Keychain, etc.).
                         **This is the preferred usage**, since it is more secure.
        :type password: str
        :param max_wait_time: the maximum time to wait for something to load
                              before throwing a timeout error
        :type max_wait_time: int
        :param chromedriver_path: the filepath to chromedriver.exe. If not specified, the package's own driver will be used
        :type chromedriver_path: str
        :param download_dir: the directory in which to download any files. If not
                             specified, defaults to system's default download location.
        :type download_dir: str
        """
        self._login_url = login_url
        self._email = email
        if password:
            self._password = password
        else:
            self._password = keyring.get_password(self._login_url, self._email)
            if not self._password:
                raise InvalidPasswordError("Keyring unable to find password for "
                                           f"service {login_url} and user {email}")
        self._browser = HandshakeBrowser(max_wait_time=max_wait_time,
                                         chromedriver_path=chromedriver_path,
                                         download_dir=download_dir)

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
        self._browser.update_constants()
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
