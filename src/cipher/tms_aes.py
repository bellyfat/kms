from cipher.tms_aes_gcm import AES_GCM
import common.tms_logger as logger

def init(mode, key):
    _mode = str(mode).upper()
    if _mode == "GCM":
        return AES_GCM(key)

    logger.error("AES mode not supported")
