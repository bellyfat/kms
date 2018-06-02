import common.tms_logger as logger
from common.tms_yaml import py2yaml, yaml2py
import storage.tms_storage as storage
from data_tree.tms_data_tree import DataTree

# aesgcm = aes.init("GCM", b"AES256Key-32Characters1234567890")
# cipher_data, nonce = aesgcm.encrypt(b"Hello World")
# logger.info("Result = " + str(aesgcm.decrypt(cipher_data, nonce)))
key = b"AES256Key-32Characters1234567890"
s = storage.init("./data.enc", "crypto", key)
s.save(b"123456789")
data = s.load()
logger.info("read data = " + str(data))


s = """\
root:
  - id: a1
  - id: a2
  - id: a3
  - id: a4
    attrib:
      - id: b1
        name: xyz
"""
p1 = yaml2py(s)
print(p1)
s1 = py2yaml(p1)
print(s1)

p2 = yaml2py(s1)
print(p2)
s2 = py2yaml(p2)
print(s2)



d = DataTree()
d.add_node('/', {'id': 'a1', 'children': []})
print(d.get_tree())
d.add_node('/a1', {'id': 'b1', 'children': []})
print(d.get_tree())
d.add_node('/', {'id': 'a2', 'children': []})
print(d.get_tree())
d.add_node('/', {'id': 'a3', 'children': []})
print(d.get_tree())
