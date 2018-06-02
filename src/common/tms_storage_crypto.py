import cipher.tms_aes_gcm as gcm
import common.tms_logger as logger
class Local:
    pass

__config = Local()
__config.encrypt = None
__config.decrypt = None
__config.key = None

def init(mode, key):
    _mode = str(mode).lower()
    if _mode == "gcm":
        __config.encrypt = gcm.encrypt
        __config.decrypt = gcm.decrypt
        __config.key = key
        logger.info("AES GCM Configured")

def encrypt(plain_data, nounce):
    return __config.encrypt(__config.key, plain_data, nounce)


def decrypt(cipher_data, nounce):
    return __config.decrypt(__config.key, cipher_data, nounce)
