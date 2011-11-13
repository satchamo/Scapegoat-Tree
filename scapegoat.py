import math
class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.key)


class ScapeGoatTree():
    def __init__(self, a):
        self.a = a
        self.size = 0
        self.max_size = 0
        self.root = None

    # Return the number of keys on the subtree rooted by x (including x's key)
    def sizeOf(self, x):
        if x == None:
            return 0
        return 1 + self.sizeOf(x.left) + self.sizeOf(x.right)

    def haT(self):
        return math.floor(math.log(self.size, 1.0/self.a))

    # Determine if a specific depth of a node makes the tree "deep"
    def isDeep(self, depth):
        return depth > self.haT()

    # Returns the brother node of "node", whose parent is "parent"
    def brotherOf(self, node, parent):
        if parent.left != None and parent.left.key == node.key:
            return parent.right
        return parent.left

    # Builds a new binary tree based on an old one. The new tree is balanced
    def myRebuildTree(self, root, length):
        # Turn a binary tree into a list of nodes in sorted order
        def flatten(node, nodes):
            if node == None:
                return
            flatten(node.left, nodes)
            nodes.append(node)
            flatten(node.right, nodes)

        # Build a balanced binary tree for a sort list of nodes
        def buildTreeFromSortedList(nodes, start, end):
            if start > end:
                return None
            mid = int(math.ceil(start + (end - start) / 2.0))
            node = Node(nodes[mid].key)
            #node = nodes[mid]
            node.left = buildTreeFromSortedList(nodes, start, mid-1)
            node.right = buildTreeFromSortedList(nodes, mid+1, end)
            return node

        nodes = []
        flatten(root, nodes)
        return buildTreeFromSortedList(nodes, 0, length-1)

    # Returns the node with the minimum key in the subtree rooted by x
    def minimum(self, x):
        while x.left != None:
            x = x.left
        return x

    # Delete the node in the tree with a value of delete_me
    def delete(self, delete_me):
        node = self.root
        parent = None
        is_left_child = True
        # find the node, keep track of the parent, and side of the tree
        while node.key != delete_me:
            parent = node
            if delete_me > node.key:
                node = node.right
                is_left_child = False
            else:
                node = node.left
                is_left_child = True

        successor = None
        # case 1: Node to be delete has no children
        if node.left == None and node.right == None:
            pass
        # case 2: Node has only a right child
        elif node.left == None:
            successor = node.right
        # case 3: Node has only a left child
        elif node.right == None:
            successor = node.left
        # case 4: Node has right and left child
        else:
            # find successor
            successor = self.minimum(node.right)
            # the successor is the node's right child -- easy fix
            if successor == node.right:
                successor.left = node.left
            # complicated case
            else:
                print "finding successor"
                successor.left = node.left
                tmp = successor.right
                successor.right = node.right
                node.right.left = tmp

        # Replace the node
        if parent == None:
            self.root = successor
        elif is_left_child:
            parent.left = successor
        else:
            parent.right = successor

        self.size -= 1
        if self.size < self.a * self.max_size:
            #print "Rebuilding the whole tree"
            self.root = self.myRebuildTree(self.root, self.size)
            self.max_size = self.size

    def search(self, key):
        x = self.root
        while x != None:
            if x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            else:
                return x;

        return None

    def insert(self, key):
        z = Node(key)
        y = None
        x = self.root
        # keep track of the depth and parents (so we don't have to recalculate
        # them)
        depth = 0
        parents = []
        # find where to place the node
        while x != None:
            parents.insert(0,x)
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
            depth += 1

        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self.size += 1
        self.max_size = max(self.size, self.max_size)
        
        # Need to do rebuild?
        if self.isDeep(depth):
            scapegoat = None
            parents.insert(0,z)
            sizes = [0]*len(parents)
            I = 0
            # find the highest scapegoat on the tree
            for i in range(1, len(parents)):
                sizes[i] = sizes[i-1] + self.sizeOf(self.brotherOf(parents[i-1], parents[i])) + 1
                if not self.isAWeightBalanced(parents[i], sizes[i]+1):
                    scapegoat = parents[i]
                    I = i
                    #print "When inserting %d Node %d is not weight balanced and could be a scapegoat" % (key, parents[I].key)
            
            tmp = self.myRebuildTree(scapegoat, sizes[I]+1)
            
            scapegoat.left = tmp.left
            scapegoat.right = tmp.right
            scapegoat.key = tmp.key
            
    def isAWeightBalanced(self, x, size_of_x):
        a = self.sizeOf(x.left) <= (self.a * size_of_x)
        b = self.sizeOf(x.right) <= (self.a * size_of_x)
        return a and b

    # these procedures are from the paper and do not work
    #def flatten(self, root, head):
    #    if root == None:
    #        return head
    #    root.right = self.flatten(root.right, head)
    #    return self.flatten(root.left, root)

    #def buildTree(self, size, head):
    #    if size == 1:
    #        return head
    #    elif size == 2:
    #        (head.right).left = head
    #        return head.right
    #    root = (self.buildTree(math.floor((size-1)/2.0), head)).right
    #    last = self.buildTree(math.floor((size-1)/2.0), root.right)
    #    root.left = head
    #    return last

    #def rebuildTree(self, scapegoat, size):
    #    head = self.flatten(scapegoat, None)
    #    self.buildTree(size, head)
    #    return head

    def preOrder(self, x):
        if x != None:
            print x.key
            self.preOrder(x.left)
            self.preOrder(x.right)

    def printTree(self):
        self.preOrder(self.root)


if __name__ == '__main__':
    import sys
    import re
    # Use tree.txt or command line for file
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'tree.txt'

    f = open(filename, 'r')
    t = None
    for line in f.readlines():
        line = re.split(r'\s+', line) 
        cmd = line[0]
        if cmd == "BuildTree":
            t = ScapeGoatTree(float(line[1]))
            t.insert(int(line[2]))
        elif cmd == "Insert":
            t.insert(int(line[1]))
        elif cmd == "Print":
            t.printTree()
        elif cmd == "Delete":
            t.delete(int(line[1]))
        elif cmd == "Done":
            print "Exiting"
            exit(0)
        elif cmd == "Search":
            val = t.search(int(line[1]))
            if val != None:
                print "Found %d" % (val.key)
            else:
                print "Error: Key %d not found" % (int(line[1]))
        else:
            print "Error: Command not recognized"

