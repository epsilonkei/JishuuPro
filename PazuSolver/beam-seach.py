# Binary Search Tree:
#
# Smaller values go to the left
# Larger values go to the right
 
class Node(object):
    def __init__(self, key, value, parent):
        self._key = key
        self._value = value
        self._parent = parent
        self._left = None
        self._right = None
 
    @property
    def key(self):
        return self._key
 
    @property
    def value(self):
        return self._value
 
    @property
    def parent(self):
        return self._parent
 
    @property
    def left(self):
        return self._left
 
    @property
    def right(self):
        return self._right
 
    @key.setter
    def key(self, value):
        self._key = value
 
    @value.setter
    def value(self, value):
        self._value = value
 
    @parent.setter
    def parent(self, value):
        self._parent = value
 
    @left.setter
    def left(self, value):
        self._left = value
 
    @right.setter
    def right(self, value):
        self._right = value
 
    def is_leaf(self):
        return not self.right or self.left
 
    def has_children(self):
        return self.right or self.left
 
    def has_both_children(self):
        return self.right and self.left
 
    def successor(self):
        pass
 
 
class BinarySearchTree(object):
    def __init__(self, root=None):
        self.root = root
        self.size = 0
 
    def put(self, key, value):
        if self.root:
            self._put(key, value, self.root)
        else:
            self.root = Node(key, value, None)
 
        self.size = self.size + 1
 
    def _put(self, key, value, current_node):
        if key < current_node.key:
            if current_node.left:
                self._put(key, value, current_node.left)
            else:
                current_node.left = Node(key, value, current_node)
        else:
            if current_node.right:
                self._put(key, value, current_node.right)
            else:
                current_node.right = Node(key, value, current_node)
 
    def get(self, key):
        if self.root:
            node = self._get(key, self.root)
            return node.value
        else:
            return None
 
    def _get(self, key, current_node):
        if not current_node:
            return None
        elif current_node.key == key:
            return current_node
        elif key < current_node.key:
            return self._get(key, current_node.left)
        elif key > current_node.key:
            return self._get(key, current_node.right)
        else:
            return None
 
    # __contains__ overloads the "in" operator
    def __contains__(self, key):
        return bool(self._get(key, self.root))
 
    def delete(self, key):
        if self.size > 1:
            node = self._get(key, self.root)
            if node:
                self._remove(node)
                self.size = self.size-1
            else:
                print("Sorry, the key '{}' wasn't found".format(key))
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = 1
        else:
            print("Sorry, the key '{}' wasn't found".format(key))
 
    def _remove(self, node):
        if node.is_leaf():
            self._remove_leaf(node)
        elif node.has_children():
            self._remove_with_child(node)
        else:
            self._remove_with_children(node)
 
    def _remove_leaf(self, node):
        if node == node.parent.left:
            node.parent.left = None
        else:
            node.parent.right = None
 
    def _remove_with_child(self, node):
        if node.left:
            node.left.parent = node.parent
            node.parent.left = node.left
        else:
            node.right.parent = node.parent
            node.parent.right = node.right
 
    def _remove_with_children(self, node):
        successor = self._find_min(node.right) # smallest key in right subtree
        self._remove(successor)
        self.put(successor.key, successor.value)
 
    def _find_min(self, node):
        current = node
        while current.left:
            current = current.left
        return current
 
 
if __name__ == "__main__":
    BST = BinarySearchTree()
    BST.put(5, "foo")
    BST.put(2, "bar")
    BST.put(8, "baz")
    BST.put(15, "qux")
    BST.put(10, "qiz")
    BST.put(1, "beep")
    BST.put(3, "boop")
 
# Binary Search Tree:
#
#         (5)
#        /   \
#     (2)     (8)
#    /   \       \
# (1)     (3)     (15)
#                /
#            (10)
#
# Visualisation tool:
#   http://btv.melezinek.cz/binary-search-tree.html
 
    print("10: ", BST.get(10))
    print("5: ", BST.get(5))
    print("8: ", BST.get(8))
    print("3: ", BST.get(3))
 
    if 15 in BST:
        print("found the key I'm searching for")
    else:
        print("didn't find the key")
 
    print("size: ", BST.size) # 7
 
    BST.delete(2)
 
    print("size: ", BST.size) # 6
