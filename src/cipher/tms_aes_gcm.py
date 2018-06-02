import os
import sys
import uuid
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import common.tms_logger as logger


class AES_GCM():

    NONCE_BYTE_SIZE = 12
    __aesgcm = None

    def __init__(self, key):
        self.__aesgcm = AESGCM(key)

    def encrypt(self, plain_data, nonce=None):
        try:
            if nonce is None:
                nonce = os.urandom(self.NONCE_BYTE_SIZE)

            cipher_data = self.__aesgcm.encrypt(nonce, plain_data, None)
        except Exception as e:
            logger.error(e)
            raise

        return cipher_data, nonce

    def decrypt(self, cipher_data, nonce):
        try:
            plain_data = self.__aesgcm.decrypt(nonce, cipher_data, None)
        except Exception as e:
            logger.error(e)
            raise

        return plain_data

