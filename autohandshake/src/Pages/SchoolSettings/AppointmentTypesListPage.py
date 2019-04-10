from autohandshake.src.Pages import Page
from autohandshake.src.constants import BASE_URL
from autohandshake.src.HandshakeBrowser import HandshakeBrowser


class AppointmentTypesListPage(Page):
    """The overview settings page listing all appointment types"""

    def __init__(self, browser: HandshakeBrowser):
        """
        Load the appointment types list view from the school settings

        :param browser: a logged-in HandshakeBrowser
        :type browser: HandshakeBrowser
        """
        super().__init__(f'{BASE_URL}/schools/{browser.school_id}/appointment_types',
                         browser)
