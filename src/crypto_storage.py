import common.tms_logger as logger
from common.tms_yaml import py2yaml, yaml2py
import storage.tms_storage as storage
from data_tree.tms_data_tree import DataTree
from key_manager import KeyManager

# aesgcm = aes.init("GCM", b"AES256Key-32Characters1234567890")
# cipher_data, nonce = aesgcm.encrypt(b"Hello World")
# logger.info("Result = " + str(aesgcm.decrypt(cipher_data, nonce)))
key = b"AES256Key-32Characters1234567890"
s = storage.init("./kms.db", "crypto", key)
#s.save(b"123456789")
#data = s.load()
#logger.info("read data = " + str(data))
km = KeyManager(s)
#km.add_key('/', 'a1', b'this is my key')
print(km.get_key('/a1'))
