import unittest

from autohandshake.src.Pages.Page import Page


class TestPage(unittest.TestCase):

    def test_throws_error_when_required_methods_not_implemented(self):
        with self.assertRaises(TypeError):
            class SomePage(Page):
                pass
            some_page = SomePage()