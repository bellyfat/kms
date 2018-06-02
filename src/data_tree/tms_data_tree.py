from common.tms_logger import logger


class DataTree():
    __tree = []

    def __init__(self, obj=None):
        if obj is not None:
            tree = self.__sanitize_tree(obj)
            self.__tree = tree
        else:
            self.__tree = []

    def get_tree(self):
        return self.__tree

    def add_node(self, path, node):
        # validate new node
        node = self.__sanitize_node(node)
        if len(node['children']) is not 0:
            self.__sanitize_tree(node['children'])
        # validate path
        path_list = self.__get_path_list(path)

        # get parent path
        branch = self.__get_node(path_list, self.__tree)
        # add new node
        if type(branch) is not list:
            branch = branch['children']
        elif len(path_list) is not 0 and path_list[-1] is not '':
            # check if last path name exist or not
            raise ValueError("Path not found")
        # check duplicate
        if self.__get_list_item_by_id(branch, node.get('id')) is not None:
            raise ValueError("Node with this id already exist")

        branch.append(node)

    def add_node_attrib(self, path, name, value):
        if not name or type(name) is not str:
            raise ValueError("Node attribute name must be string")

        n = self.get_node(path)
        n['attrib'][name] = value

    def get_node_attrib(self, path, name):
        if not name or type(name) is not str:
            raise ValueError("Node attribute name must be string")

        n = self.get_node(path)
        return n['attrib'].get(name)

    def del_node_attrib(self, path, name):
        if not name or type(name) is not str:
            raise ValueError("Node attribute name must be string")

        n = self.get_node(path)
        n['attrib'].pop(name, None)

    def get_node_attrib_list(self, path):
        n = self.get_node(path)
        return n['attrib']

    def get_node(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        # get parent path
        node = self.__get_node(path_list, self.__tree)

        # add new node
        if type(node) is not list:
            return node
        else:
            raise ValueError("Path Does not Exist")

    def get_node_children(self, path):
        # validate path
        path_list = self.__get_path_list(path)

        # get parent path
        node = self.__get_node(path_list, self.__tree)

        # Get node children
        if path is '/':
            return self.__tree
        if type(node) is not list:
            return node['children']
        else:
            raise ValueError("Path not found")

    def __sanitize_node(self, node):
        if node is None or node is "" or type(node) is not dict:
            raise ValueError("DataTree new node type must be a dict")
        if not node.get('id') or type(node.get('id')) is not str:
            raise ValueError("New Node must have field 'id' of type string")
        if not node.get('key') or type(node.get('key')) is not bytes:
            raise ValueError("New Node must have field 'key' of type bytes")
        if node.get('children') is not None and type(node.get('children')) is not list:
            raise ValueError("New Node must have field 'children' of type list")
        if node.get('attrib') is not None and type(node.get('attrib')) is not dict:
            raise ValueError("New Node must have field 'attrib' of type dict")
        if node.get('children') is None:
            node['children'] = []
        if node.get('attrib') is None:
            node['attrib'] = {}
        return node

    def __sanitize_tree(self, tree):
        if tree is None or type(tree) is not list:
            raise ValueError("Tree must be of type list")
        for node in tree:
            node = self.__sanitize_node(node)
            if len(node['children']) is not 0:
                self.__sanitize_tree(node['children'])

        return tree
    
    def __get_path_list(self, path):
        if type(path) is not str or path is None:
            raise ValueError("Path must be a string")
        if path is '':
            raise ValueError("path cannot be empty")
        if path[0] is not '/':
            raise ValueError("path must start with '/'")
        path = path.strip('/')
        return path.split('/')

    def __get_list_item_by_id(self, list_items, item_id):
        for i in list_items:
            if i.get('id') == item_id:
                return i
        return None

    def __get_node(self, path_list, root):
        if path_list is None or path_list is "":
            raise ValueError("DataTree path cannot be empty")
        if type(root) is not list:
            raise ValueError("Root must be a list")
        if type(path_list) is not list:
            raise ValueError("path_list must be a list")

        item = self.__get_list_item_by_id(root, path_list[0])

        # Termination condition
        if path_list[1:] == []:
            if item is not None:
                return item
            else:
                return root

        elif item is not None and item.get('children') is not None:
            if item.get('children') is not None:
                return self.__get_node(path_list[1:], item.get('children'))
            raise ValueError("Object has no children attribute")
        else:
            raise ValueError("Path not found")
