import os
import sys
import cipher.tms_aes as aes
import common.tms_logger as logger

class STORAGE_CRYPTO:
    __path = None
    __cipher = None

    def __init__(self, path, cipher, mode, key):
        # sanitize path

        self.__path = path
        # Init crypto engine
        if cipher.upper() == "AES":
            if mode.upper() == "GCM":
                self.__cipher = aes.init(mode, key)
                return
        logger.error("Invalid ciper or mode for crypto storage initialization.")

    def save(self, data):
        try:
            if data is None:
                logger.error("No data to save")
                raise("No data to save")

            # Encrypt Data
            cipher_data, nonce = self.__cipher.encrypt(data)
            print(type(nonce))
            print(type(cipher_data))
            file_data = b''.join([nonce, cipher_data])

            # Save Data
            with open(self.__path, "wb", 0) as fh:
                fh.write(file_data)

        except Exception as e:
            logger.error(e)
            logger.error("saving data to file failed using crypto storage")
            raise

    def load(self):
        try:
            data = None
            # Read data
            with open(self.__path, "rb", 0) as fh:
                file_data = fh.read()
                # Decrypt data
                cipher_data = file_data[self.__cipher.NONCE_BYTE_SIZE:]
                nonce = file_data[:self.__cipher.NONCE_BYTE_SIZE]
                data = self.__cipher.decrypt(cipher_data, nonce)

            if data is None:
                raise("Failed to load data from File")
            return data
        except Exception as e:
            logger.error(e)
            logger.error("saving data to file failed using crypto storage")
            raise
