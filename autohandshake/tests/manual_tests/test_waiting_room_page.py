"""
Since the contents of the Handshake waiting room is a *highly* time-and-day
dependant thing, and is no way to create records to test against without
polluting the live waiting room, I do not believe it is possible to write
automated tests for it. Therefore, this file is to serve as a manual testing
"sandbox" of sorts o allow for testing against whatever the waiting room happens
to contain that day.
"""
from autohandshake import WaitingRoomPage
from autohandshake.tests import TestSession
import time

if __name__ == '__main__':
    with TestSession() as browser:
        waiting_room = WaitingRoomPage(browser)
        print(waiting_room.get_checkin_data())
        time.sleep(300)
