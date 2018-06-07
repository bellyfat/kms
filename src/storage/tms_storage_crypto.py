import os
import cipher.tms_aes as aes
import common.tms_logger as logger
import cryptography


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
            else:
                raise ValueError('Invalid Cipher mode for storage initialization')
        else:
            raise ValueError('Invalid Cipher for storage initialization')
        # create empty file not exit
        if not os.path.exists(self.__path):
            with open(self.__path, "wb", 0):
                pass

    def save(self, data):
        try:
            if data is None:
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
            raise ValueError("saving data to file failed using crypto storage")

    def load(self):
        data = None
        # Read data
        try:
            with open(self.__path, "rb", 0) as fh:
                file_data = fh.read()
                # Decrypt data
                cipher_data = file_data[self.__cipher.NONCE_BYTE_SIZE:]
                nonce = file_data[:self.__cipher.NONCE_BYTE_SIZE]
                try:
                    data = self.__cipher.decrypt(cipher_data, nonce)
                except cryptography.exceptions.InvalidTag as e:
                    raise ValueError('storage corrupted or not initialized')
        except BaseException as e:
            raise ValueError("Failed to load data from file")

        if data is None:
            raise ValueError("Failed to load data from File")
        return data

    def is_valid(self):
        try:
            self.load()
        except BaseException as e:
            return False

        return True

    def is_initialized(self):
        return self.__path and self.__cipher
