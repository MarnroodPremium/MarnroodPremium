from __future__ import annotations
from math import floor

class Node:
    uid_counter = 0

    def __init__(self, order):
        self.order = order
        self.parent: Node | None = None
        self.keys = []
        self.values = []

        #  This is for Debugging purposes only!
        Node.uid_counter += 1
        self.uid = self.uid_counter

    def split(self) -> Node:  # Split a full Node to two new ones.
        left = Node(self.order)
        right = Node(self.order)
        mid = int(self.order // 2)

        left.parent = right.parent = self

        left.keys = self.keys[:mid]
        left.values = self.values[: mid + 1]

        right.keys = self.keys[mid + 1 :]
        right.values = self.values[mid + 1 :]

        self.values = [left, right]  # Setup the pointers to child nodes.

        self.keys = [self.keys[mid]]  # Hold the first element from the right subtree.

        # Setup correct parent for each child node.
        for child in left.values:
            if isinstance(child, Node):
                child.parent = left

        for child in right.values:
            if isinstance(child, Node):
                child.parent = right

        return self  # Return the 'top node'

    def get_size(self) -> int:
        return len(self.keys)

    def is_empty(self) -> bool:
        return len(self.keys) == 0

    def is_full(self) -> bool:
        return len(self.keys) == self.order - 1

    def is_nearly_underflowed(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2)

    def is_underflowed(self) -> bool:  # Used to check on keys, not data!
        return len(self.keys) <= floor(self.order / 2) - 1

    def is_root(self) -> bool:
        return self.parent is None


class LeafNode(Node):
    def __init__(self, order):
        super().__init__(order)

        self.prev_leaf: LeafNode | None = None
        self.next_leaf: LeafNode | None = None
        self.values = []

    def add(self, key, value):  # TODO: Implement improved version
        if not self.keys:  # Insert key if it doesn't exist
            self.keys.append(key)
            self.values.append([value])
            return

        for i, item in enumerate(self.keys):  # Otherwise, search key and append value.
            if key == item:  # Key found => Append Value
                self.values[i].append(
                    value
                )  # Remember, this is a list of data. Not nodes!
                break

            elif key < item:  # Key not found && key < item => Add key before item.
                self.keys = self.keys[:i] + [key] + self.keys[i:]
                self.values = self.values[:i] + [[value]] + self.values[i:]
                break

            elif i + 1 == len(self.keys):  # Key not found here. Append it after.
                self.keys.append(key)
                self.values.append([value])
                break

    def split(
        self,
    ) -> Node:  # Split a full leaf node. (Different method used than before!)
        top = Node(self.order)
        right = LeafNode(self.order)
        mid = int(self.order // 2)

        self.parent = right.parent = top

        right.keys = self.keys[mid:]
        right.values = self.values[mid:]
        right.prev_leaf = self
        right.next_leaf = self.next_leaf

        top.keys = [right.keys[0]]
        top.values = [self, right]  # Setup the pointers to child nodes.

        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        self.next_leaf = right  # Setup pointer to next leaf

        return top  # Return the 'top node'


class BPlusTree(object):
    def __init__(self, order=5):
        self.root: Node = LeafNode(order)  # First node must be leaf (to store data).
        self.order: int = order

    @staticmethod
    def find(node: Node, key):
        for i, item in enumerate(node.keys):
            if key < item:
                return node.values[i], i
            elif i + 1 == len(node.keys):
                return node.values[i + 1], i + 1  # return right-most node/pointer.
        return None, -1  # return default value when key is not found

    @staticmethod
    def merge_up(parent: Node, child: Node, index):
        parent.values.pop(index)
        pivot = child.keys[0]

        for c in child.values:
            if isinstance(c, Node):
                c.parent = parent

        for i, item in enumerate(parent.keys):
            if pivot < item:
                parent.keys = parent.keys[:i] + [pivot] + parent.keys[i:]
                parent.values = parent.values[:i] + child.values + parent.values[i:]
                break

            elif i + 1 == len(parent.keys):
                parent.keys += [pivot]
                parent.values += child.values
                break

    def insert(self, key, value):
        node = self.root

        while not isinstance(
            node, LeafNode
        ):  # While we are in internal nodes... search for leafs.
            if not node:
                raise AttributeError

            node, index = self.find(node, key)

        # Node is now guaranteed a LeafNode!
        node.add(key, value)

        while node and node.parent and len(node.keys) == node.order:  # 1 over full
            if not node.is_root():
                parent = node.parent
                node = node.split()  # Split & Set node as the 'top' node.
                _, index = self.find(parent, node.keys[0])
                self.merge_up(parent, node, index)
                node = parent
            else:
                node = node.split()  # Split & Set node as the 'top' node.
                self.root = node  # Re-assign (first split must change the root!)

    def retrieve(self, key):
        node = self.root

        while not isinstance(node, LeafNode):
            if not node:
                return None
            node, _ = self.find(node, key)

        for i, item in enumerate(node.keys):
            if key == item:
                return node.values[i]

        return None

    def delete(self, key):
        node = self.root

        while not isinstance(node, LeafNode):
            if not node:
                return False
            node, parent_index = self.find(node, key)

        if key not in node.keys:
            return False

        index = node.keys.index(key)
        node.values[index].pop()  # Remove the last inserted data.


        if len(node.values[index]) == 0:
            node.values.pop(index)  # Remove the list element.
            node.keys.pop(index)

            while node and node.parent and node.is_underflowed() and not node.is_root():
                # Borrow attempt:
                prev_sibling = self.get_prev_sibling(node)
                next_sibling = self.get_next_sibling(node)
                _, parent_index = self.find(node.parent, key)

                if prev_sibling and not prev_sibling.is_nearly_underflowed():
                    self._borrow_left(node, prev_sibling, parent_index)
                elif next_sibling and not next_sibling.is_nearly_underflowed():
                    self._borrow_right(node, next_sibling, parent_index) # type: ignore
                elif prev_sibling and prev_sibling.is_nearly_underflowed():
                    self._merge_on_delete(prev_sibling, node)
                elif next_sibling and next_sibling.is_nearly_underflowed():
                    self._merge_on_delete(node, next_sibling)

                node = node.parent

            if (
                node.is_root()
                and not isinstance(node, LeafNode)
                and len(node.values) == 1
            ):
                self.root = node.values[0]
                self.root.parent = None

        return True

    @staticmethod
    def _borrow_left(node: Node, sibling: Node, parent_index):
        if not node.parent or not node.parent.keys:
            raise AttributeError

        if isinstance(node, LeafNode):  # Leaf Redistribution
            key = sibling.keys.pop(-1)
            data = sibling.values.pop(-1)
            node.keys.insert(0, key)
            node.values.insert(0, data)

            node.parent.keys[parent_index - 1] = key  # Update Parent (-1 is important!)
        else:  # Inner Node Redistribution (Push-Through)
            parent_key = node.parent.keys.pop(-1)
            sibling_key = sibling.keys.pop(-1)
            data: Node = sibling.values.pop(-1)
            data.parent = node
            node.parent.keys.insert(0, sibling_key)
            node.keys.insert(0, parent_key)
            node.values.insert(0, data)

    @staticmethod
    def _borrow_right(node: LeafNode, sibling: LeafNode, parent_index):
        if not node.parent or not node.parent.keys:
            raise AttributeError
        if isinstance(node, LeafNode):  # Leaf Redistribution
            key = sibling.keys.pop(0)
            data = sibling.values.pop(0)
            node.keys.append(key)
            node.values.append(data)

            node.parent.keys[parent_index] = sibling.keys[0]  # Update Parent
        else:  # Inner Node Redistribution (Push-Through)
            parent_key = node.parent.keys.pop(0)
            sibling_key = sibling.keys.pop(0)
            data: Node = sibling.values.pop(0)
            data.parent = node

            node.parent.keys.append(sibling_key)
            node.keys.append(parent_key)
            node.values.append(data)

    @staticmethod
    def _merge_on_delete(l_node: Node, r_node: Node):
        parent = l_node.parent

        if not parent:
            raise AttributeError

        _, index = BPlusTree.find(parent, l_node.keys[0])  # Reset pointer to child
        parent_key = parent.keys.pop(index)
        parent.values.pop(index)
        parent.values[index] = l_node

        if isinstance(l_node, LeafNode) and isinstance(r_node, LeafNode):
            l_node.next_leaf = r_node.next_leaf  # Change next leaf pointer
        else:
            l_node.keys.append(parent_key)  # TODO Verify dis
            for r_node_child in r_node.values:
                r_node_child.parent = l_node

        l_node.keys += r_node.keys
        l_node.values += r_node.values

    @staticmethod
    def get_prev_sibling(node: Node) -> Node:
        if node.is_root() or not node.keys:
            raise AttributeError
        if not node.parent:
            raise AttributeError

        _, index = BPlusTree.find(node.parent, node.keys[0])
        if not index - 1 >= 0:
            raise AttributeError
        return node.parent.values[index - 1]

    @staticmethod
    def get_next_sibling(node: Node) -> Node:
        if node.is_root() or not node.keys:
            raise AttributeError
        if not node.parent:
            raise AttributeError

        _, index = BPlusTree.find(node.parent, node.keys[0])
        if not index + 1 < len(node.parent.values):
            raise AttributeError
        return node.parent.values[index + 1]

    def show_bfs(self):
        if self.root.is_empty():
            print("The B+ Tree is empty!")
            return
        queue = [self.root, 0]  # Node, Height... Scrappy but it works

        while len(queue) > 0:
            node = queue.pop(0)
            height = queue.pop(0)

            if not isinstance(node, LeafNode):
                queue += self.intersperse(node.values, height + 1)
            print(
                height,
                "|".join(map(str, node.keys)),
                "\t",
                node.uid,
                "\t parent -> ",
                node.parent.uid if node.parent else None,
            )

    def get_leftmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[0]

        return node

    def get_rightmost_leaf(self):
        if not self.root:
            return None

        node = self.root
        while not isinstance(node, LeafNode):
            node = node.values[-1]

        return node

    def show_all_data(self):
        node = self.get_leftmost_leaf()
        if not node:
            return None

        while node:
            for node_data in node.values:
                print("[{}]".format(", ".join(map(str, node_data))), end=" -> ")

            node = node.next_leaf
        print("Last node")

    def show_all_data_reverse(self):
        node = self.get_rightmost_leaf()
        if not node:
            return None

        while node:
            for node_data in reversed(node.values):
                print("[{}]".format(", ".join(map(str, node_data))), end=" <- ")

            node = node.prev_leaf
        print()

    @staticmethod
    def intersperse(lst, item):
        result = [item] * (len(lst) * 2)
        result[0::2] = lst
        return result