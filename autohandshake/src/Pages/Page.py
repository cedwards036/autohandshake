from abc import ABC, abstractmethod
from autohandshake.src.HandshakeBrowser import HandshakeBrowser, UserType
from autohandshake.src.exceptions import InvalidURLError, WrongPageForMethodError, \
    InvalidUserTypeError
from typing import Callable


class Page(ABC):
    """
    A single web page on the Handshake site
    """

    def __init__(self, url: str, browser: HandshakeBrowser):
        """
        Create a page object for the given URL

        :param url: the url of the page to initialize
        :type url: str
        :param browser: a HandshakeBrowser that is logged in to Handshake
        :type browser: HandshakeBrowser
        """
        self._validate_url(url)
        self._url = url
        self._browser = browser
        self._browser.get(url)
        self._wait_until_page_is_loaded()

    @abstractmethod
    def _wait_until_page_is_loaded(self):
        """Wait until the page has finished loading.

        For pages without complex javascript involved in the load, simply
        returning immediately is sufficient.
        """
        raise NotImplementedError

    def validate_current_page(self):
        """Ensure that the browser is on the correct page before calling a method.

        To be used to make sure methods on this page are not called while the
        browser is on a different page
        """
        try:
            self._validate_url(self._browser.current_url)
            self._wait_until_page_is_loaded()
        except InvalidURLError:
            raise WrongPageForMethodError()

    @abstractmethod
    def _validate_url(self, url):
        """
        Ensure that the given URL is a valid URL for this page type

        :param url: the url to validate
        :type url: str
        """
        raise NotImplementedError

    @classmethod
    def require_user_type(cls, user_type: UserType):
        """
        Throw an error if the browser is not currently logged in as the required user type.

        To be used as a decorator for Page subclass methods that require the
        browser to be logged in as a specific user type.

        :param func: a page method
        :type func: function
        :param user_type: the user type to require
        :type user_type: UserType
        """

        def require_user_type_decorator(func: Callable):
            def inner_func(self, *args, **kwargs):
                if not self._browser.user_type == user_type:
                    raise InvalidUserTypeError("Invalid user type for method")
                return func(self, *args, **kwargs)

            return inner_func

        return require_user_type_decorator


    @property
    def url(self):
        """Get the page's url"""
        return self._url
