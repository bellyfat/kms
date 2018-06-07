import base64
from data_tree.tms_data_tree import DataTree
from common.tms_yaml import yaml2py, py2yaml


class KeyManager():

    __key_tree = None
    __storage = None

    def __init__(self, storage):

        if storage is not None:
            try:
                if storage.is_initialized():
                    self.__storage = storage
                else:
                    raise ValueError('Storage must be initilized.')
            except BaseException as e:
                raise ValueError('Invalid Storage object type')

        else:
            raise ValueError('Must provide storage for initializing KeyManager')

        if storage.is_valid():
            # decode yaml
            s = storage.load()

            py_objs = None
            try:
                print(s)
                py_objs = yaml2py(s)
            except Exception as e:
                raise ValueError('Invalid Yaml read from storage')

            if py_objs is not None:
                # Import objects to data tree
                self.__key_tree = DataTree(py_objs)
            else:
                raise ValueError('Data read from file do not conform with DataTree format')

        else:
            self.__key_tree = DataTree()
            self.__save_key_tree()

    def __save_key_tree(self):
        data = self.__key_tree.get_tree()
        yaml = ''
        try:
            yaml = py2yaml(data)
        except BaseException as e:
            raise ValueError('Failed to encode key tree to yaml')
 
        try:
            file_data = bytes(yaml, 'utf-8')
            self.__storage.save(file_data)
        except BaseException as e:
            raise ValueError('Error saving key tree to storage')

    def add_key(self, path, key_id, key, attrib=None):
        try:
            key_node = {'id': key_id,
                        'key': key,
                        'attrib': attrib}
            self.__key_tree.add_node(path, key_node)
            self.__save_key_tree()
        except BaseException as e:
            raise ValueError('Error adding key.')

    def get_key(self, path):
        return self.__key_tree.get_node(path)

    def del_key(self, path):
        pass

    def update_key(self, path, key=None, attrib=None):
        pass

    def export_key(self, path, out_path):
        pass

    def reseal_storage(self, new_key):
        pass


