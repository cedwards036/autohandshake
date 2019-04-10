import unittest

from autohandshake.src.Pages import Page
from autohandshake import HandshakeBrowser
from autohandshake.src.constants import BASE_URL


class TestPage(unittest.TestCase):

    def test_throws_error_when_required_methods_not_implemented(self):
        with self.assertRaises(TypeError):
            class SomePage(Page):
                pass

            some_page = SomePage(BASE_URL, HandshakeBrowser())
