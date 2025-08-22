#!/usr/bin/python

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []  # A list to store child nodes

    def add_child(self, child_node):
        """Adds a child node to the current node."""
        self.children.append(child_node)

    def __repr__(self):
        """String representation of the node for easy printing."""
        return f"Node({self.data})"

# Building a simple tree
if __name__ == "__main__":
    # Create the root node
    root = Node("Root")

    # Create child nodes for the root
    child1 = Node(" Child 1")
    child2 = Node(" Child 2")

    # Add children to the root
    root.add_child(child1)
    root.add_child(child2)

    # Create a grandchild node for child1
    grandchild1 = Node("  Grandchild 1.1")
    child1.add_child(grandchild1)

    # You can now access the tree structure
    print(root)
    print(root.children)
    print(root.children[0].children)

# EOF
