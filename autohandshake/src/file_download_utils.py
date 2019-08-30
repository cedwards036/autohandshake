import time
import os
import glob
from typing import List


def confirm_file_downloaded(dir: str, filename_pattern: str, wait_time: int = 300) -> str:
    """
    Confirm that a new file matching the filename_pattern downloaded successfully.

    :param dir: the expected download directory for the file
    :type dir: str
    :param filename_pattern: a regex pattern describing the newly-downloaded file
    :type filename_pattern: str
    :param wait_time: the maximum time to wait for the file to download
    :type wait_time: integer
    :return: the file path of the newly downloaded file
    :rtype: str
    """
    baseline_matches = _get_filename_matches(filename_pattern, dir)
    start_time = time.time()
    time_to_stop = start_time + wait_time
    while time.time() <= time_to_stop:
        time.sleep(0.5)
        updated_matches = _get_filename_matches(filename_pattern, dir)
        if len(updated_matches) == len(baseline_matches) + 1:
            return max(updated_matches, key=os.path.getctime)
    raise RuntimeError('File did not download in time')


def _get_filename_matches(filename_pattern: str, dir: str) -> List[str]:
    return glob.glob(os.path.join(dir, filename_pattern))
