from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.HandshakeBrowser import HandshakeBrowser

class AppointmentTypePage(Page):
    """A settings page for a single appointment type."""

    def __init__(self, type_id: int, browser: HandshakeBrowser):
        """
        Load the appointment type settings page for the type with the given id

        :param type_id: the id of the appointment type to load
        :type type_id: int
        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/appointment_types/{type_id}/edit', browser)