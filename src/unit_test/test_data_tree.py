import unittest
from data_tree.tms_data_tree import DataTree


class TestDataTree(unittest.TestCase):

    def __get_list_item_by_id(self, list_items, item_id):
        for i in list_items:
            if i.get('id') == item_id:
                return i
        return None

    def test_add_node_at_root(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234', 'attrib': {}, 'children': []}
        path = '/'
        d.add_node(path, n)
        tree = d.get_tree()
        node = self.__get_list_item_by_id(tree, 'a1')
        self.assertEqual(n, node)

    def test_add_tree_in_constructor(self):
        t = [{'id': 'a1', 'key': b'1234', 'attrib': {}, 'children': []}]
        d = DataTree(t)
        tree = d.get_tree()
        self.assertEqual(t, tree)

    def test_init_with_missing_optional_field(self):
        t1 = [{'id': 'a1', 'key': b'1234', 'children': []}]
        d = DataTree(t1)
        t2 = [{'id': 'a1', 'key': b'1234', 'attrib': {}, 'children': []}]
        tree = d.get_tree()
        self.assertEqual(t2, tree)

    def test_init_with_missing_mandatory_field(self):
        t1 = [{'id': 'a1', 'children': []}]
        self.assertRaises(ValueError, DataTree, t1)
        t2 = [{'key': b'1234', 'children': []}]
        self.assertRaises(ValueError, DataTree, t2)

    def test_init_with_missing_optional_field_in_children(self):
        t1 = [{'id': 'a1', 'key': b'1234',
               'children': [{'id': 'a1',
                             'key': b'1234'}]}]
        d = DataTree(t1)
        t2 = [{'id': 'a1', 'key': b'1234', 'attrib': {},
               'children': [{'id': 'a1',
                             'key': b'1234',
                             'attrib': {},
                             'children': []}]}]
        tree = d.get_tree()
        self.assertEqual(t2, tree)

    def test_init_with_missing_mandatory_field_in_children(self):
        d = DataTree()
        t1 = {'id': 'a1', 'key': b'1234',
              'children': [{'key': b'1234'}]}
        self.assertRaises(ValueError, d.add_node, '/', t1)
        t2 = {'id': 'a1', 'key': b'1234',
              'children': [{'id': 'a1'}]}
        self.assertRaises(ValueError, d.add_node, '/', t2)

    def test_add_node_with_missing_optional_field_in_children(self):
        d = DataTree()
        n1 = {'id': 'a1', 'key': b'1234',
              'children': [{'id': 'a1',
                            'key': b'1234'}]}
        d.add_node('/', n1)
        n2 = {'id': 'a1', 'key': b'1234', 'attrib': {},
              'children': [{'id': 'a1',
                            'key': b'1234',
                            'attrib': {},
                            'children': []}]}
        node = d.get_node('/a1')
        self.assertEqual(n2, node)

    def test_add_node_with_missing_mandatory_field_in_children(self):
        t1 = [{'id': 'a1', 'key': b'1234',
               'children': [{'key': b'1234'}]}]
        self.assertRaises(ValueError, DataTree, t1)
        t2 = [{'id': 'a1', 'key': b'1234',
               'children': [{'id': 'a1'}]}]
        self.assertRaises(ValueError, DataTree, t2)

    def test_add_duplicate_node(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)

        n = {'id': 'a1', 'key': b'1234', 'children': []}
        path = '/'
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'id': 'b1', 'key': b'1234', 'children': []}
        path = '/a1/'
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_add_tree_at_root(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)
        tree = d.get_tree()
        node = self.__get_list_item_by_id(tree, 'a1')
        self.assertEqual(n, node)

    def test_add_n_level_hierarchy(self):
        d = DataTree()
        path = ''
        for l in range(100):
            level_id = 'a' + str(l)
            n = {'id': level_id, 'key': b'1234', 'children': []}
            path += '/'
            d.add_node(path, n)
            path += level_id

        tree = d.get_tree()
        t = tree
        for l in range(100):
            level_id = 'a' + str(l)
            n = self.__get_list_item_by_id(t, level_id)
            self.assertEqual(n.get('id'), level_id)
            t = n['children']

    def test_addnode_without_id(self):
        d = DataTree()
        n = {'children': [], 'key': b'1234'}
        path = '/'
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_without_key(self):
        d = DataTree()
        n = {'children': [], 'id': 'a1'}
        path = '/'
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_with_invalid_key(self):
        d = DataTree()
        path = '/'
        n = {'children': [], 'id': 'a1', 'key': None}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': [], 'id': 'a1', 'key': 'abc'}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': [], 'id': 'a1', 'key': {}}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': [], 'id': 'a1', 'key': b''}
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_with_invalid_attrib(self):
        d = DataTree()
        path = '/'
        n = {'children': [], 'id': 'a1', 'key': b'123', 'attrib': b''}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': [], 'id': 'a1', 'key': b'123', 'attrib': 1}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': [], 'id': 'a1', 'key': b'123', 'attrib': 'test'}
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_without_children(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234'}
        path = '/'
        d.add_node(path, n)

        n['children'] = []

        self.assertEqual(d.get_node('/a1'), n)

    def test_addnode_with_invalid_id(self):
        d = DataTree()
        path = '/'
        n = {'id': '', 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'id': 1, 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'id': None, 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_with_invalid_children(self):
        d = DataTree()
        path = '/'
        n = {'children': '', 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': 1, 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)
        n = {'children': None, 'key': b'1234'}
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_add_n_children(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)
        path = '/a1/b1'
        for l in range(100):
            child_id = 'c' + str(l)
            n = {'id': child_id, 'key': b'1234', 'children': []}
            d.add_node(path, n)

        tree = d.get_tree()
        t = self.__get_list_item_by_id(tree, 'a1')
        self.assertNotEqual(t, None)
        t = self.__get_list_item_by_id(t['children'], 'b1')
        self.assertNotEqual(t, None)
        t = t['children']

        for l in range(100):
            child_id = 'c' + str(l)
            n = self.__get_list_item_by_id(t, child_id)
            self.assertEqual(n.get('id'), child_id)

    def test_addnode_without_path(self):
        d = DataTree()
        n = {'children': [], 'key': b'1234', 'id': 'a1'}
        path = None
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_addnode_with_invalid_path(self):
        d = DataTree()
        n = {'children': [], 'key': b'1234', 'id': 'x1'}
        path = ''
        self.assertRaises(ValueError, d.add_node, path, n)
        path = 'abc'
        self.assertRaises(ValueError, d.add_node, path, n)
        path = '/a3'
        self.assertRaises(ValueError, d.add_node, path, n)
        path = '/a2/'
        self.assertRaises(ValueError, d.add_node, path, n)
        path = 1
        self.assertRaises(ValueError, d.add_node, path, n)
        path = {}
        self.assertRaises(ValueError, d.add_node, path, n)
        path = '/'
        d.add_node(path, n)
        n = {'children': [], 'key': b'1234', 'id': 'x2'}
        path = '/a4'
        self.assertRaises(ValueError, d.add_node, path, n)

    def test_getnode_with_invalid_path(self):
        d = DataTree()
        path = None
        self.assertRaises(ValueError, d.get_node, path)
        path = ''
        self.assertRaises(ValueError, d.get_node, path)
        path = 'abc'
        self.assertRaises(ValueError, d.get_node, path)
        path = '/a1'
        self.assertRaises(ValueError, d.get_node, path)
        path = '/a1/'
        self.assertRaises(ValueError, d.get_node, path)
        path = '//'
        self.assertRaises(ValueError, d.get_node, path)
        path = 1
        self.assertRaises(ValueError, d.get_node, path)
        path = {}
        self.assertRaises(ValueError, d.get_node, path)

    def test_get_n_level_children(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)
        path = '/a1/b1'
        for l in range(100):
            child_id = 'c' + str(l)
            n = {'id': child_id, 'key': b'1234', 'children': []}
            d.add_node(path, n)

        for l in range(100):
            path = '/a1/b1/'
            child_id = 'c' + str(l)
            path += child_id
            n = d.get_node(path)
            self.assertEqual(n.get('id'), child_id)

    def test_get_n_level_hierarchy(self):
        d = DataTree()
        path = ''
        for l in range(100):
            level_id = 'a' + str(l)
            n = {'id': level_id, 'key': b'1234', 'children': []}
            path += '/'
            d.add_node(path, n)
            path += level_id

        path = ''
        for l in range(100):
            level_id = 'a' + str(l)
            n = {'id': level_id, 'key': b'1234', 'children': []}
            path += '/' + level_id
            d.get_node(path)
            self.assertEqual(n.get('id'), level_id)

    def test_getnode_children_with_invalid_path(self):
        d = DataTree()
        path = None
        self.assertRaises(ValueError, d.get_node_children, path)
        path = ''
        self.assertRaises(ValueError, d.get_node_children, path)
        path = 'abc'
        self.assertRaises(ValueError, d.get_node_children, path)
        path = '/a1'
        self.assertRaises(ValueError, d.get_node_children, path)
        path = '/a1/'
        self.assertRaises(ValueError, d.get_node_children, path)
        path = '//'
        self.assertRaises(ValueError, d.get_node_children, path)
        path = 1
        self.assertRaises(ValueError, d.get_node_children, path)
        path = {}
        self.assertRaises(ValueError, d.get_node_children, path)

    def test_get_node_children(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)
        path = '/a1/b1'
        for l in range(100):
            child_id = 'c' + str(l)
            n = {'id': child_id, 'key': b'1234', 'children': []}
            d.add_node(path, n)

        path = '/a1/b1'
        children = d.get_node_children(path)
        for l in range(100):
            child_id = 'c' + str(l)
            t = self.__get_list_item_by_id(children, child_id)
            self.assertNotEqual(t, None)

    def test_get_node_children_with_trailing_slash(self):
        d = DataTree()
        n = {'id': 'a1', 'key': b'1234',
             'children': [{'id': 'b1', 'key': b'1234', 'children': []}]}
        path = '/'
        d.add_node(path, n)
        path = '/a1/b1/'
        for l in range(100):
            child_id = 'c' + str(l)
            n = {'id': child_id, 'key': b'1234', 'children': []}
            d.add_node(path, n)

        path = '/a1/'
        children = d.get_node_children(path)
        path = '/a1/b1/'
        children = d.get_node_children(path)
        for l in range(100):
            child_id = 'c' + str(l)
            t = self.__get_list_item_by_id(children, child_id)
            self.assertNotEqual(t, None)

    def test_add_node_attribute(self):
        n = [{'id': 'a1', 'key': b'1234', 'children': []}]
        d = DataTree(n)
        d.add_node_attrib('/a1', 'attrib1', 123)
        a = d.get_node_attrib('/a1', 'attrib1')
        self.assertEqual(a, 123)

    def test_add_node_attribute_with_invalid_name(self):
        n = [{'id': 'a1', 'key': b'1234', 'children': []}]
        d = DataTree(n)
        self.assertRaises(ValueError, d.add_node_attrib, '/a1', '', 123)
        self.assertRaises(ValueError, d.add_node_attrib, '/a1', None, 123)
        self.assertRaises(ValueError, d.add_node_attrib, '/a1', 123, 123)
        self.assertRaises(ValueError, d.add_node_attrib, '/a1', {}, 123)

    def test_del_node_attribute(self):
        n = [{'id': 'a1', 'key': b'1234',
              'attrib': {'attrib1': 123},
              'children': []}]
        d = DataTree(n)
        a = d.get_node_attrib('/a1', 'attrib1')
        self.assertEqual(a, 123)
        d.del_node_attrib('/a1', 'attrib1')
        a = d.get_node_attrib('/a1', 'attrib1')
        self.assertEqual(a, None)

    def test_get_node_attribute_list(self):
        t1 = [{'id': 'a1', 'key': b'1234', 'attrib': {},
              'children': [{
                                'id': 'a1',
                                'key': b'1234',
                                'attrib': {
                                    'attrib1': 123,
                                    'attrib2': '1234',
                                    'attrib3': {'abc': 123},
                                    'attrib4': [1236],
                                    'attrib5': b'1273'
                                },
                                'children': []
                           },
                           {
                                'id': 'a1',
                                'key': b'1234',
                                'attrib': {},
                                'children': []
                           }]}]

        d = DataTree(t1)
        nl = d.get_node_attrib_list('/a1/a1')
        self.assertEqual(t1[0]['children'][0]['attrib'], nl)


if __name__ == '__main__':
    unittest.main()
