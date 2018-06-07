import copy
import pprint
from common.exception import TMSError

class DataTree():
    def __str__(self):
        return str(self.__tree)

    def __init__(self, obj=None):
        __tree = {
                    'id': 'root',
                    'key': b'root',
                    'attrib': {},
                    'children': []
                 }

        self.__tree = __tree
        if obj is not None:
            node = copy.deepcopy(obj)
            node = self.__sanitize_tree(node)
            self.__tree['children'].append(node)

        self.__sanitize_node(self.__tree)

    def get_tree(self):
        return copy.deepcopy(self.__tree)

    def add_node(self, path, node):
        # validate new node
        node = self.__sanitize_node(copy.deepcopy(node))
        if len(node['children']) is not 0:
            self.__sanitize_tree(node)
        # validate path
        path_list = self.__get_path_list(path)
        # get parent path
        parent = self.__get_node(path_list, self.__tree)
        # check duplicate
        if self.__get_list_item_by_id(parent['children'], node.get('id'))[1] is not None:
            raise TMSError("Node with this id already exist")
        # add node
        parent['children'].append(node)

    def del_node(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        if len(path_list) == 1 and path_list[0] == 'root':
            raise TMSError('Path not found')

        node_id = path_list[-1]
        parent_path = path_list[:-1]
        # get parent path
        parent = self.__get_node(parent_path, self.__tree)
        child_idx = self.__get_list_item_by_id(parent['children'], node_id)[0]
        if child_idx is None:
            raise TMSError("Path not found")
        else:
            del parent['children'][child_idx]

    def del_node_children(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        # get parent path
        parent = self.__get_node(path_list, self.__tree)

        for i in range(len(parent['children']):
            del parent['children'][i]

    def add_node_attrib(self, path, name, value):
        if not name or type(name) is not str:
            raise TMSError("Node attribute name must be string")

        path_list = self.__get_path_list(path)
        n = self.__get_node(path_list, self.__tree)
        n['attrib'][name] = copy.deepcopy(value)

    def get_node_attrib(self, path, name):
        if not name or type(name) is not str:
            raise TMSError("Node attribute name must be string")

        path_list = self.__get_path_list(path)
        n = self.__get_node(path_list, self.__tree)
        return copy.deepcopy(n['attrib'].get(name))

    def del_node_attrib(self, path, name):
        if not name or type(name) is not str:
            raise TMSError("Node attribute name must be string")

        path_list = self.__get_path_list(path)
        n = self.__get_node(path_list, self.__tree)
        n['attrib'].pop(name, None)

    def copy_node(self, src_path, dst_path):
        node = self.get_node(src_path)
        self.add_node(dst_path, node)

    def copy_node_children(self, src_path, dst_path):
        src_node = self.get_node(src_path)
        for child in src_node['children']:
            self.add_node(dst_path, child)

    def move_node(self, src_path, dst_path):
        self.copy_node(src_path, dst_path)
        self.del_node(src_path)

    def move_node_children(self, src_path, dst_path):
        self.copy_node_children(src_path, dst_path)
        self.del_nodei_children(src_path)

    def get_node_attrib_list(self, path):
        path_list = self.__get_path_list(path)
        n = self.__get_node(path_list, self.__tree)
        return copy.deepcopy(n['attrib'])

    def get_node(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        if len(path_list) == 1 and path_list[0] == 'root':
            raise TMSError('Path not found')

        # get parent path
        node = self.__get_node(path_list, self.__tree)

        return copy.deepcopy(node)

    def get_node_children(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        # get parent path
        node = self.__get_node(path_list, self.__tree)
        return copy.deepcopy(node['children'])

    def __sanitize_node(self, node):
        if node is None or node is "" or type(node) is not dict:
            raise TMSError("DataTree new node type must be a dict")
        if not node.get('id') or type(node.get('id')) is not str:
            raise TMSError("New Node must have field 'id' of type string")
        if not node.get('key') or type(node.get('key')) is not bytes:
            raise TMSError("New Node must have field 'key' of type bytes")
        if node.get('children') is not None:
            if type(node.get('children')) is not list:
                raise TMSError("New Node must have field 'children' of type list")
        if node.get('attrib') is not None:
            if type(node.get('attrib')) is not dict:
                raise TMSError("New Node must have field 'attrib' of type dict")
        if node.get('children') is None:
            node['children'] = []
        if node.get('attrib') is None:
            node['attrib'] = {}
        return node

    def __sanitize_tree(self, tree):
        if tree is None or type(tree) is not dict:
            raise TMSError("Tree must be of type dict")
        self.__sanitize_node(tree)

        if len(tree['children']) is not 0:
            duplicate_check = {}
            for node in tree['children']:
                self.__sanitize_tree(node)
                node_id = node.get('id')
                if node_id in duplicate_check:
                    raise TMSError('Node contains duplicate children')
                else:
                    duplicate_check[node['id']] = True

        return tree

    def __get_path_list(self, path):
        if type(path) is not str or path is None:
            raise TMSError("Path must be a string")
        if path is '':
            raise TMSError("path cannot be empty")
        if path[0] is not '/':
            raise TMSError("path must start with '/'")
        path = path.strip('/')
        path_list = path.split('/')
        if len(path_list) is 1 and path_list[0] is '':
            path_list = []
        return ['root'] + path_list

    def __get_list_item_by_id(self, list_items, item_id):
        for idx, val in enumerate(list_items):
            if val.get('id') == item_id:
                return idx, val
        return None, None

    def __get_node(self, path_list, root):
        if path_list is None or path_list is "":
            raise TMSError("DataTree path cannot be empty")
        if type(root) is not dict:
            raise TMSError("Root must be a dict")
        if type(path_list) is not list:
            raise TMSError("path_list must be a list")

        # Check whether current node matches with path
        if path_list[0] != root['id']:
            raise TMSError("Path not found")

        if len(path_list[1:]) is 0:
            return root
        else:
            children = root['children']
            if len(children) is not 0:
                child = self.__get_list_item_by_id(children, path_list[1])[1]
                if not child:
                    raise TMSError("Path not found")
                else:
                    return self.__get_node(path_list[1:], child)
            else:
                raise TMSError("Path not found")
