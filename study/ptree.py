#!/usr/bin/env python

''' Simple tree for parser '''

class Node:
    """
    Class Node
    """
    def __init__(self, value):
        self.left = None
        self.data = value
        self.right = None

class Tree:
    """
    Class tree will provide a tree as well as utility functions.
    """

    def createNode(self, data):
        """
        Utility function to create a node.
        """
        return Node(data)

    def insert(self, node , data):
        """
        Insert function will insert a node into tree.
        Duplicate keys are not allowed.
        """
        #if tree is empty , return a root node
        if node is None:
            return self.createNode(data)
        # if data is smaller than parent , insert it into left side
        if data < node.data:
            node.left = self.insert(node.left, data)
        elif data > node.data:
            node.right = self.insert(node.right, data)

        return node

    def search(self, node, data):
        """
        Search function will search a node into tree.
        """
        # if root is None or root is the search data.
        if node is None or node.data == data:
            return node

        if node.data < data:
            return self.search(node.right, data)
        else:
            return self.search(node.left, data)

    def deleteNode(self,node,data):
        """
        Delete function will delete a node into tree.
        Not complete , may need some more scenarion that we can handle
        Now it is handling only leaf.
        """

        # Check if tree is empty.
        if node is None:
            return None

        # searching key into BST.
        if data < node.data:
            node.left = self.deleteNode(node.left, data)
        elif data > node.data:
            node.right = self.deleteNode(node.right, data)
        else: # reach to the node that need to delete from BST.
            if node.left is None and node.right is None:
                del node
            if node.left == None:
                temp = node.right
                del node
                return  temp
            elif node.right == None:
                temp = node.left
                del node
                return temp

        return node

    def traverseInorder(self, arrx, lev, root):
        """
        traverse function will print all the node in the tree.
        """
        if root is not None:
            self.traverseInorder(arrx, lev, root.left)
            arrx.append((root.data, len(lev)))
            lev.append(len(lev))
            self.traverseInorder(arrx, lev, root.right)

    #def traversePreorder(self, arrx, root):
    #    """
    #    traverse function will print all the node in the tree.
    #    """
    #    if root is not None:
    #        arrx.append(root.data)
    #        self.traversePreorder(arrx, root.left)
    #        self.traversePreorder(arrx, root.right)
    #
    #def traversePostorder(self, arrx, root):
    #    """
    #    traverse function will print all the node in the tree.
    #    """
    #    if root is not None:
    #        self.traversePostorder(arrx, root.left)
    #        self.traversePostorder(arrx, root.right)
    #        arrx.append(root.data)

def main():
    root = None
    tree = Tree()
    root = tree.insert(root, 10)
    #print(root)
    tree.insert(root, 20) ; tree.insert(root, 30)
    tree.insert(root, 40) ; tree.insert(root, 70)
    tree.insert(root, 60) ; tree.insert(root, 80)

    print("Traverse Inorder:  ", end = " ")
    arrx = [] ; lev = []
    tree.traverseInorder(arrx, lev, root)
    print(arrx, lev)

    #arrx = []
    #print("Traverse Preorder: ", end = " ")
    #tree.traversePreorder(arrx, root)
    #print(arrx)
    #arrx = []
    #print("Traverse Postorder:", end = " ")
    #tree.traversePostorder(arrx, root)
    #print(arrx)

def test_main():

    root = None
    tree = Tree()
    root = tree.insert(root, 10)
    #print(root)
    tree.insert(root, 20)
    tree.insert(root, 30)
    tree.insert(root, 40)
    tree.insert(root, 70)
    tree.insert(root, 60)
    tree.insert(root, 80)
    arrx = tree.traverseInorder(root)

    assert "10 20 30 40 60 70 80" == arrx

if __name__ == "__main__":
    print ("This module was not meant to operate as main.")
    main()

 # EOF