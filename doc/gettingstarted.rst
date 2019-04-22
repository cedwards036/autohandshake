===============
Getting Started
===============

HandshakeSession
================

Autohandshake's central class is :class:`~autohandshake.HandshakeSession`, a `context manager <https://www.geeksforgeeks.org/context-manager-in-python/>`_ that represents a browsing
session on the Handshake platform. Instantiating the class using a "with" statement and providing valid login credentials
will log you into Handshake and plop you on the homepage. From there, you can use the various `Pages <./pages.html>`_  to perform
actions on different webpages within Handshake.

Example:
::

    with HandshakeSession(school_url, email, password) as browser:
        # do something

Pages
=====

The main functionality of autohandshake comes from its Page classes. These are essentially collections of methods that
are associated with specific pages in Handshake. For example, the InsightsPage class can do things like download an Insights
report and change the dates in a date range filter.

Every Page-type class takes at least one constructor argument: a logged-in :class:`~autohandshake.HandshakeBrowser`.
While each Page class specifies the possible actions that can be taken on their respective pages, the :class:`~autohandshake.HandshakeBrowser`
actually performs those actions, such as clicking a button, waiting for a page to load, or entering text. The :class:`~autohandshake.HandshakeSession`
context manager returns a logged-in :class:`~autohandshake.HandshakeBrowser` that can be injected into any Page class.

To load a page, simply instantiate the page's class, passing in the session's :class:`~autohandshake.HandshakeBrowser` as well as
any other arguments required by the page's constructor. You are now free to use any of the available methods on that page.

Example:
::

    from autohandshake import HandshakeBrowser, InsightsPage
    import datetime

    appts_by_status_report = 'https://app.joinhandshake.com/analytics/explore_embed?insights_page=ZXhwbG9yZS9nZW5lcmF0ZWRfaGFuZHNoYWtlX3Byb2R1Y3Rpb24vYXBwb2ludG1lbnRzP3FpZD1pcDFLd0ZlSmh4VVdobXYxa212U2xuJmVtYmVkX2RvbWFpbj1odHRwczolMkYlMkZhcHAuam9pbmhhbmRzaGFrZS5jb20mdG9nZ2xlPWZpbA=='

    with HandshakeBrowser(school_url, email, password) as browser:
        insights_page = InsightsPage(appts_by_status_report, browser)
        insights_page.set_date_range_filter('Appointments', 'Start Date Date',
                                            start_date = datetime.datetime(2018, 1, 1),
                                            end_date = datetime.datetime(2019, 1, 1))
        report_data = insights_page.get_data()

IMPORTANT: only the most recently loaded page's methods are available for use at any given time. Attempting something like
the following will throw an error, since the first page is no longer active in the browser when its method is called:
::

    from autohandshake import HandshakeBrowser, MajorSettingsPage, AppointmentTypePage

    with HandshakeBrowser(school_url, email, password) as browser:
        # load a page
        major_settings_page = MajorSettingsPage(browser)
        # load a second page
        appt_type_page = AppointmentTypePage(232523, browser)
        # call a method on the first page
        major_settings_page.get_major_mapping() # ERROR!




