import configparser
import os
from cryptography.fernet import Fernet
from autohandshake import HandshakeSession
from autohandshake.src.constants import MAX_WAIT_TIME

config = configparser.ConfigParser()
config.read(os.path.dirname(__file__) + './config.ini')

password = Fernet(config['CONSTANTS']['KEY']).decrypt(bytes(config['CONSTANTS']['PASSWORD'],
                                                            encoding='utf-8')).decode("utf-8")
homepage = config['CONSTANTS']['HOMEPAGE']
email = config['CONSTANTS']['EMAIL']
school_id = config['CONSTANTS']['SCHOOL_ID']
download_dir = config['CONSTANTS']['DOWNLOAD_DIR']


class TestSession(HandshakeSession):
    """A testing instance of HandshakeSession that always logs in with config-based credentials"""

    download_dir = download_dir

    def __init__(self, max_wait_time=MAX_WAIT_TIME):
        super().__init__(homepage, email, password, max_wait_time)
