import unittest

from red_black_tree.red_black_tree import Node, RBTree


class RadBlackTreePropertiesMismatch(Exception):
    """
    Red-black tree has to follow property "If a node is red, then both its children are black" and it has to be balanced
    The exception is raised if the properties are not followed
    """
    def __init__(self, text):
        self.txt = text


class BinarySearchTreePropertiesMismatch(Exception):
    """
    Binary-search tree property are "The key value in the left subtree is not greater than the root key" and
    "The key value in the right subtree is greater than in the root key"
    The exception is raised if the properties are not followed
    """
    def __init__(self, text):
        self.txt = text


class Status:
    """
    Stores the keys of the tree and the depth from the root to the leaves
    """

    def __init__(self):
        self.deep = []
        self.keys = set()


def pre_order_travers(tree: RBTree, root: Node, status: Status, curr_depth: int) -> None:
    """
    Traverses the left subtree first, then the right subtree
    Checks if the property "If a node is red, then both its children are black" is being executed
    Checks if the tree is binary-search tree
    Raises exception if some of the above isn't true
    :param curr_depth: depth of current subtree
    :param tree: tree to which the current subtree belongs
    :param root: root of the current subtree
    :param status: class which stores the keys of the entire tree and the depth to the leaves
    :return: None
    """
    if root.has_left_son():
        status.keys.add(root.left_node.key)
        if root.left_node.key > root.key:
            raise BinarySearchTreePropertiesMismatch(
                "The key value in the left subtree " "is greater than the root key"
            )
        if root.is_red() and root.left_node.is_red():
            raise RadBlackTreePropertiesMismatch("The red child of the red parent")
        pre_order_travers(tree, root.left_node, status, curr_depth + 1)
    if root.has_right_son():
        status.keys.add(root.right_node.key)
        if root.right_node.key < root.key:
            raise BinarySearchTreePropertiesMismatch(
                "The key value in the right subtree " "is less than in the root key"
            )
        if root.is_red() and root.right_node.is_red():
            raise RadBlackTreePropertiesMismatch("The red child of the red parent")
        pre_order_travers(tree, root.right_node, status, curr_depth + 1)
    if root.has_no_children():
        status.deep.append(curr_depth)


def checking_children(tree: RBTree) -> Status:
    """
    Checks if the tree is balanced (the depth from the further leaf to the root is not more than twice as deep as depth
    from the nearest leaf to the root)
    Calls a function that:
     1. Checks if the property "If a node is red, then both its children are black" is being executed
     2. Checks if the tree is binary-search tree
    Raises exception is some of the above isn't true
    :param tree: the tree that is checked
    :return: class which stores the keys of the entire tree and the depth to the leaves
    """
    status = Status()
    status.keys.add(tree.root.key)
    pre_order_travers(tree, tree.root, status, 0)
    if max(status.deep) > 2 * min(status.deep):
        raise RadBlackTreePropertiesMismatch("Tree is not balanced")
    return status


def checking_root_color(tree: RBTree) -> None:
    """
    Checks following the red-black tree property "The root color is black"
    The RadBlackTreePropertiesMismatch exception is raised if the property is not followed
    :param tree: the tree that is checked
    :return: None
    """
    if tree.root.is_red():
        raise RadBlackTreePropertiesMismatch("Root is not black")


class TestTree(unittest.TestCase):
    def test_empty_tree(self):
        tree = RBTree()
        self.assertTrue(tree.root is None)

    def test_insert_in_empty_tree(self):
        tree = RBTree(1)
        self.assertTrue(not tree.is_empty())
        self.assertEqual(tree.root.key, 1)
        self.assertTrue(tree.root.is_black())
        self.assertFalse(tree.root.has_left_son())
        self.assertFalse(tree.root.has_right_son())

    def test_second_insert_with_large_key(self):
        tree = RBTree(1, 2)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertEqual(tree.root.key, 1)
        self.assertTrue(tree.root.has_right_son())
        self.assertFalse(tree.root.has_left_son())
        self.assertEqual(tree.root.right_node.key, 2)
        self.assertEqual(tree.root.right_node.parent.key, 1)

    def test_insert_two_children(self):
        tree = RBTree(1, 2, 3)
        self.assertEqual(tree.root.key, 2)

    def test_second_insert_with_smaller_key(self):
        tree = RBTree(1, 0)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertEqual(tree.root.key, 1)
        self.assertFalse(tree.root.has_right_son())
        self.assertTrue(tree.root.has_left_son())
        print(tree.root.left_node.key)
        self.assertEqual(tree.root.left_node.key, 0)
        self.assertEqual(tree.root.left_node.parent.key, 1)

    def test_insert_in_place_of_root(self):
        tree = RBTree(0, 3, 1, 4, 2)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        try:
            status = checking_children(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()
        except BinarySearchTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertEqual(status.keys, set(range(5)))

    def test_insert_lots_inserts(self):
        tree = RBTree(5, 3, 1, 4, 2, 8, 10, 7, 11, 0, 6, 9)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        try:
            status = checking_children(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()
        except BinarySearchTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertEqual(status.keys, set(range(12)))

    def test_balance_after_insert(self):
        tree = RBTree(*list(range(12)))
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        try:
            status = checking_children(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()
        except BinarySearchTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertEqual(status.keys, set(range(12)))

    def test_delete_single_root(self):
        tree = RBTree(1)
        tree.delete(1)
        self.assertTrue(tree.is_empty())

    def test_delete_son(self):
        tree = RBTree(1, 2, 3)
        tree.delete(3)
        self.assertFalse(tree.root.has_right_son())
        tree.delete(1)
        self.assertFalse(tree.root.has_left_son())

    def test_delete_root_simple(self):
        tree = RBTree(1, 2, 3)
        tree.delete(3)
        tree.delete(2)
        self.assertEqual(tree.root.key, 1)

    def test_delete_root_second(self):
        tree = RBTree(*list(range(14)))
        tree.delete(tree.root.key)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()
        except BinarySearchTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

    def test_delete_brother_with_red_child(self):
        """
        The case in which the right child of the deleted node's brother is red
        Repaints the brother in the color of the father, repaints his child and father in black, makes a rotation
        In that case the black brother is 1, it's red son is 2
        """
        tree = RBTree(1, 3, 5, 2)
        tree.delete(3)
        try:
            checking_root_color(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        try:
            checking_children(tree)
        except RadBlackTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()
        except BinarySearchTreePropertiesMismatch as exception:
            print(exception.txt)
            self.fail()

        self.assertIsNone(tree.find_key(3))

    def test_delete_lots_deletions(self):
        tree = RBTree(5, 3, 1, 4, 2, 8, 10, 7, 11, 0, 6, 9)
        correct_keys = set(range(12))

        for key_to_delete in [5, 3, 2, 7, 1, 11, 6, 8, 9, 4, 10]:
            tree.delete(key_to_delete)
            try:
                checking_root_color(tree)
            except RadBlackTreePropertiesMismatch as exception:
                print(exception.txt)
                self.fail()

            try:
                status = checking_children(tree)
            except RadBlackTreePropertiesMismatch as exception:
                print(exception.txt)
                self.fail()
            except BinarySearchTreePropertiesMismatch as exception:
                print(exception.txt)
                self.fail()

            correct_keys.remove(key_to_delete)
            self.assertEqual(status.keys, correct_keys)

        tree.delete(0)
        self.assertTrue(tree.is_empty())

    def test_find(self):
        tree = RBTree(1, 0, 3, 2, 5, 4, 6)
        self.assertIsNotNone(tree.find_key(1))
        self.assertIsNotNone(tree.find_key(0))
        self.assertIsNotNone(tree.find_key(3))
        self.assertIsNotNone(tree.find_key(2))
        self.assertIsNotNone(tree.find_key(5))
        self.assertIsNotNone(tree.find_key(4))
        self.assertIsNotNone(tree.find_key(6))
        self.assertIsNone(tree.find_key(7))

    def test_double_delete(self):
        tree = RBTree(1, 3)
        tree.delete(3)
        tree.delete(3)

        self.assertIsNone(tree.find_key(3))
