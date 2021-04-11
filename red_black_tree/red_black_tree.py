from abc import abstractmethod
import enum
from typing import Any, Optional, Protocol, TypeVar

C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


class Colour(enum.Enum):
    black = 0
    red = 1


class Node:
    """Node class of red black tree"""

    def __init__(self, key: C, colour: Colour):
        self.key = key
        self.colour = colour
        self.parent = None
        self.left_node = None
        self.right_node = None

    def is_red(self) -> bool:
        """
        Checks if the node color is Color.red
        :return: True if node color is Color.red, otherwise False
        """
        return self.colour == Colour.red

    def is_black(self) -> bool:
        """
        Checks if the node color is Color.black
        :return: True if node color is Color.black, otherwise False
        """
        return self.colour == Colour.black

    def has_right_son(self) -> bool:
        """
        Checks if the right son of the node is not None
        :return: True if the right son of the node is not None, otherwise False
        """
        return self.right_node is not None

    def has_left_son(self) -> bool:
        """
        Checks if the left son of the node is not None
        :return: True if the left son of the node is not None, otherwise False
        """
        return self.left_node is not None

    def has_no_children(self) -> bool:
        """
        Checks if the both sons are None
        :return: True if the left son of the node is None and the right son of the node is None, otherwise False
        """
        return not self.has_right_son() and not self.has_left_son()

    def has_two_children(self) -> bool:
        """
        Checks if the both sons aren't None
        :return: True if the left son of the node is not None and the right son of the node is not None, otherwise False
        """
        return self.has_right_son() and self.has_left_son()

    def has_black_children(self) -> bool:
        """
        Checks if the both node children aren't None and the color of the right and left son is Color.black
        :return:
        """
        return self.has_two_children() and self.left_node.is_black() and self.right_node.is_black()

    def is_right_son(self) -> bool:
        """
        Checks whether there is a parent of the current node for which the node is the right son
        :return: True if there is a parent of the current node for which the node is the right son, otherwise False
        """
        return self.parent is not None and self.parent.right_node is not None and self == self.parent.right_node

    def is_left_son(self) -> bool:
        """
        Checks whether there is a parent of the current node for which the node is the left son
        :return: True if there is a parent of the current node for which the node is the left son, otherwise False
        """
        return self.parent is not None and self.parent.left_node is not None and self == self.parent.left_node

    def brother_node(self) -> Optional["Node"]:
        """
        Returns the child of the parent of the current node other than it if such child exists
        :return: The child of the parent of the current node other than it exists, otherwise None
        """
        if self.is_left_son():
            return self.parent.right_node
        return self.parent.left_node

    def grandfather_node(self) -> Optional["Node"]:
        """
        Returns the parent of the parent of the current node it if all the mentioned nodes exist
        :return: The parent of the parent of the current node it if all the mentioned nodes exist, otherwise None
        """
        return self.parent.parent


class RBTree:
    """
    Red-black tree

    Red-black tree is self-balancing binary search tree
    The properties are executed:
        1. Each node is either red or black
        2. If a node is red, then both its children are black
        3. Every path from a given node to any of its leaves goes through the same number of black nodes

    In this implementation, the keys should not be repeated
    """

    def __init__(self, *elements: C):
        """
        Builds a red-black tree from list elements
        :param elements: the list of elements that the red-black tree will consist of
        :return: red-black tree
        """
        self.root = None
        for elem in elements:
            self.insert(elem)

    def _node_is_root(self, node: Node) -> bool:
        """
        Checks whether node is the root of the tree
        :param node: assumed root
        :return: True if node is the root of the tree, otherwise False
        """
        return node == self.root

    def is_empty(self) -> bool:
        """
        Checks if there are any inserted notes in the tree
        :return: True if there are any inserted notes in the tree, otherwise False
        """
        return self.root is None

    def _left_rotate(self, node: Node) -> None:
        """
        The left rotation at node x makes x goes down in the left direction and as a result, its right child goes up.
        The order "<" between nodes is preserved

                            |                            |
                            x                            y
                           / \   _left_rotation(x)     /  \
                          a   y  ================>    x    c
                             / \                     / \
                            b   c                   a   b

        :param node: the node x relative to which the rotation will occur
        :return: None
        """
        right_son_copy = node.right_node
        node.right_node = right_son_copy.left_node

        if right_son_copy.left_node is not None:
            right_son_copy.left_node.parent = node

        right_son_copy.parent = node.parent
        if node.parent is None:
            self.root = right_son_copy
        elif node.is_left_son():
            node.parent.left_node = right_son_copy
        else:
            node.parent.right_node = right_son_copy

        right_son_copy.left_node = node
        node.parent = right_son_copy

    def _right_rotate(self, node: Node) -> None:
        """
        The right rotation at node x makes x goes down in the right direction and as a result, its left child goes up.
        The order "<" between nodes is preserved

                                 /                            |
                                y                             x
                               / \     _right_rotation(x)   /  \
                              x   c    ================>   a    y
                             / \                               / \
                            a   b                             b   c

        :param node: the node x relative to which the rotation will occur
        :return:
        """
        left_son_copy = node.left_node
        node.left_node = left_son_copy.right_node
        if left_son_copy.right_node is not None:
            left_son_copy.right_node.parent = node

        left_son_copy.parent = node.parent
        if node.parent is None:
            self.root = left_son_copy
        elif node.is_right_son():
            node.parent.right_node = left_son_copy
        else:
            node.parent.left_node = left_son_copy

        left_son_copy.right_node = node
        node.parent = left_son_copy

    def _balance_after_insert(self, inserted_node: Node) -> None:
        """
        Performs balancing after inserting a new element restoring compliance with the property "If a node is red,
        then both its children are black"
        :param inserted_node: the node inserted by the insert() function
        :return: None
        """
        is_valid_operation = (
            inserted_node is not None
            and inserted_node.parent is not None
            and inserted_node.grandfather_node() is not None
        )
        if not is_valid_operation:
            return
        while inserted_node.parent.is_red():
            if inserted_node.parent.is_right_son():
                uncle = inserted_node.grandfather_node().left_node
                if uncle is not None and uncle.is_red():
                    uncle.colour = Colour.black
                    inserted_node.parent.colour = Colour.black
                    inserted_node.grandfather_node().colour = Colour.red
                    inserted_node = inserted_node.grandfather_node()
                else:
                    if inserted_node.is_left_son():
                        inserted_node = inserted_node.parent
                        self._right_rotate(inserted_node)
                    inserted_node.parent.colour = Colour.black
                    inserted_node.grandfather_node().colour = Colour.red
                    self._left_rotate(inserted_node.grandfather_node())
            else:
                uncle = inserted_node.grandfather_node().right_node
                if uncle is not None and uncle.is_red():
                    uncle.colour = Colour.black
                    inserted_node.parent.colour = Colour.black
                    inserted_node.grandfather_node().colour = Colour.red
                    inserted_node = inserted_node.grandfather_node()
                else:
                    if inserted_node.is_right_son():
                        inserted_node = inserted_node.parent
                        self._left_rotate(inserted_node)
                    inserted_node.parent.colour = Colour.black
                    inserted_node.grandfather_node().colour = Colour.red
                    self._right_rotate(inserted_node.grandfather_node())
            if self._node_is_root(inserted_node):
                break
        self.root.colour = Colour.black

    def insert(self, key: C) -> None:
        """
        Inserts a new node with a specific key into the tree
        The behavior is undefined if a node with such a key already exists in the tree
        :param key: the key that will become the key of the inserted node
        :return: None
        """
        if self.is_empty():
            self.root = Node(key, Colour.black)
            return

        node_to_insert = Node(key, Colour.red)
        prev_root = self.root
        curr_root = None

        while prev_root is not None:
            curr_root = prev_root
            if node_to_insert.key < prev_root.key:
                prev_root = prev_root.left_node
            else:
                prev_root = prev_root.right_node

        node_to_insert.parent = curr_root

        if curr_root is None:
            self.root = node_to_insert
        elif node_to_insert.key < curr_root.key:
            curr_root.left_node = node_to_insert
        else:
            curr_root.right_node = node_to_insert

        self._balance_after_insert(node_to_insert)

    def _find_key_in_subtree(self, root: Node, key: C) -> Optional[Node]:
        """
        Recursively searches for a node by key in the subtree with the given root
        :param root: root of the subtree that is currently being searched
        :param key: the key that the node is being searched for with
        :return: the desired node, if it exists in the tree, otherwise None
        """
        if root is None:
            return None
        if root.key == key:
            return root
        if root.key < key:
            return self._find_key_in_subtree(root.right_node, key)
        return self._find_key_in_subtree(root.left_node, key)

    def find_key(self, key: C) -> Optional[Node]:
        """
        Searches for a node by key in the tree
        :param key: the key that the node is being searched for with
        :return: the desired node, if it is in the tree, otherwise None
        """
        return self._find_key_in_subtree(self.root, key)

    def _delete_childless_node(self, node: Node) -> None:
        """
        Deletes the leaf node
        :param node: node to delete
        :return: None
        """
        if self._node_is_root(node):
            self.root = None
            return
        if node.is_right_son():
            node.parent.right_node = None
        else:
            node.parent.left_node = None

    def _find_next_key(self, node: Node) -> Node:
        """
        Returns the node with the key that is the smallest of the keys larger than the node's key
        Looks at the right son of the node and goes down the left sons until it reaches the leaves
        :param node: node, the larger key for which is being sought
        :return: the desired node, if it exists in the tree, otherwise None
        """
        start_node = node.right_node
        while start_node.has_left_son():
            start_node = start_node.left_node
        return start_node

    def _balance_after_delete(self, node: Node) -> None:
        """
        Performs balancing after deleting the node from the tree restoring compliance with the property "If a node is
        red, then both its children are black" and "Every path from a given node to any of its leaves goes through the
        same number of black nodes."
        :param node: the node deleted by the delete() function
        :return: None
        """
        while node != self.root and node.is_black():
            is_left_son = node.has_right_son() and node.right_node.parent == node.parent or node.is_left_son()
            if (is_left_son and node.parent.right_node is None) and (
                node.is_right_son() and node.parent.left_node is None
            ):
                break
            if is_left_son:
                brother = node.parent.right_node
                if brother is None:
                    break
                if brother.is_red():
                    brother.colour = Colour.black
                    node.parent.colour = Colour.red
                    self._left_rotate(node.parent)
                    brother = node.parent.right_node
                    if brother is None:
                        break
                elif brother.has_no_children() or brother.has_black_children():
                    brother.colour = Colour.red
                    node = node.parent
                else:
                    if brother.right_node is None or brother.right_node.is_black():
                        brother.left_node.colour = Colour.black
                        brother.colour = Colour.red
                        self._right_rotate(brother)
                        brother = node.parent.right_node
                        if brother is None:
                            break
                    brother.colour = node.parent.colour
                    node.parent.colour = Colour.black
                    brother.right_node.colour = Colour.black
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                brother = node.parent.left_node
                if brother is None:
                    break
                if brother.is_red():
                    brother.colour = Colour.black
                    node.parent.colour = Colour.red
                    self._right_rotate(node.parent)
                    brother = node.parent.left_node
                    if brother is None:
                        break
                if brother.has_no_children() or brother.has_black_children():
                    brother.colour = Colour.red
                    node = node.parent
                else:
                    if brother.left_node is None or brother.left_node.is_black():
                        brother.right_node.colour = Colour.black
                        brother.colour = Colour.red
                        self._left_rotate(brother)
                        brother = node.parent.left_node
                        if brother is None:
                            break
                    brother.colour = node.parent.colour
                    node.parent.colour = Colour.black
                    brother.left_node.colour = Colour.black
                    self._right_rotate(node.parent)
                    node = self.root

        node.colour = Colour.black

    def delete(self, key: C) -> None:
        """
        Removes node with the key from the tree
        If there is no such node, it does nothing
        :param key: the key that the node will be removed from the tree with
        :return: None
        """
        key_node = self.find_key(key)
        if key_node is None:
            return

        if key_node.has_no_children():
            self._delete_childless_node(key_node)
            return

        next_key_node = key_node
        if key_node.has_right_son() and not key_node.has_left_son():
            if self._node_is_root(key_node):
                key_node.right_node.parent = None
                self.root = key_node.right_node
                self.root.colour = Colour.black
                return
            else:
                key_node.parent.left_node = key_node.right_node
                key_node.right_node.parent = key_node.parent
        elif not key_node.has_right_son() and key_node.has_left_son():
            if self._node_is_root(key_node):
                key_node.left_node.parent = None
                self.root = key_node.left_node
                self.root.colour = Colour.black
                return
            else:
                key_node.parent.left_node = key_node.left_node
                key_node.left_node.parent = key_node.parent
        else:
            next_key_node = self._find_next_key(key_node)
            if next_key_node.has_right_son():
                next_key_node.right_node.parent = next_key_node.parent
                if self._node_is_root(next_key_node):
                    self.root = next_key_node.right_node
                elif next_key_node.parent == key_node:
                    next_key_node.parent.right_node = next_key_node.right_node
                    next_key_node.right_node.parent = next_key_node.parent
                else:
                    next_key_node.parent.left_node = next_key_node.right_node
                    next_key_node.right_node.parent = next_key_node.parent
            elif next_key_node.parent == key_node:
                key_node.right_node = None
                key_node.key = next_key_node.key
                self.root.colour = Colour.black
                if next_key_node.colour == Colour.black:
                    self._balance_after_delete(next_key_node)
                return
            else:
                next_key_node.parent.left_node = None

        if next_key_node != key_node:
            key_node.colour = next_key_node.colour
            key_node.key = next_key_node.key

        self.root.colour = Colour.black

        if next_key_node.colour == Colour.black:
            self._balance_after_delete(next_key_node)
