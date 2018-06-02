from storage.tms_storage_crypto import STORAGE_CRYPTO
import common.tms_logger as logger

def init(path, mode, key):
    _mode = str(mode).lower()
    if _mode == "crypto":
        return STORAGE_CRYPTO(path, "AES", "GCM", key)
