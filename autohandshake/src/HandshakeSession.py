import re

from autohandshake.src.HandshakeBrowser import HandshakeBrowser
from autohandshake.src.exceptions import InvalidURLError


class HandshakeSession:
    """
    A Handshake browsing session.

    Should be used as a context manager. Example:

    with HandshakeSession("https://jhu.joinhandshake.edu", username, password) as hs:
        [do something]

    """

    def __init__(self, login_url: str):
        """
        Initialize Handshake session.

        :param login_url: a valid Handshake homepage url of the form
                          "https://[school].joinhandshake.com"
        :type login_url: str
        """
        self._login_url = login_url
        self._browser = HandshakeBrowser()


    def __enter__(self)->HandshakeBrowser:
        """Open a web browser and log into Handshake, beginning the session"""
        self._browser.get(self._login_url)
        if self._school_is_invalid():
            raise InvalidURLError('Invalid school in login URL')
        return self._browser


    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the web browser"""
        self.close()


    def close(self):
        """Close the Handshake Session.

        To be called if HandshakeSession is *not* used as a context manager.
        """
        self._browser.quit()


    def _school_is_invalid(self)->bool:
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