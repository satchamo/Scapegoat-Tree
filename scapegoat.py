import re
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
                successor.left = node.left
                tmp = successor.right
                successor.right = node.right
                node.right.left = tmp

        # Replace the node
        if parent == None:
            self.root = None
        elif is_left_child:
            parent.left = successor
        else:
            parent.right = successor

    def insert(self, key):
        z = Node(key)
        y = None
        x = self.root
        depth = 0
        parents = []
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
        
        if self.isDeep(depth):
            print "BEFORE"
            self.printTree()
            print "IT'S DEEP"
            scapegoat = None
            parents.insert(0,z)
            print "Parents", parents
            sizes = [0]*len(parents)
            I = 0
            for i in range(1, len(parents)):
                sizes[i] = sizes[i-1] + self.sizeOf(self.brotherOf(parents[i-1], parents[i])) + 1
                if not self.isAWeightBalanced(parents[i], sizes[i]+1):
                    scapegoat = parents[i]
                    I = i
            print "Node %d is not weight balanced and could be a scapegoat" % (parents[I].key)
            
            print "found scapegoat, it's = %d, with size %d" % (scapegoat.key, sizes[I])
            #tmp = self.rebuildTree(sizes[i], scapegoat)
            #tmp = self.rebuildTree(sizes[I]+1, scapegoat)
            tmp = self.myRebuildTree(scapegoat, sizes[I]+1)
            print "New list is:"
            self.preOrder(tmp)
            print "/"
            
            scapegoat.left = tmp.left
            scapegoat.right = tmp.right
            scapegoat.key = tmp.key
            print "AFTER"
            self.printTree()
            return
            
    def isAWeightBalanced(self, x, size_of_x):
        a = self.sizeOf(x.left) <= (self.a * size_of_x)
        b = self.sizeOf(x.right) <= (self.a * size_of_x)
        return a and b

    def flatten(self, root, head):
        if root == None:
            return head
        root.right = self.flatten(root.right, head)
        return self.flatten(root.left, root)

    #def buildTree(self, size, head):
    #    if size == 1:
    #        return head
    #    elif size == 2:
    #        head.right.left = head
    #        return head.right
    #    root = (self.buildTree(math.floor((size-1)/2.0), head)).right
    #    last = self.buildTree(math.floor((size-1)/2.0), root.right)
    #    root.left = head
    #    return last
    def buildTree(self, n, x):
        if n == 0:
            x.left = None
            return x
        r = self.buildTree(math.ceil((n-1)/2.0),x)
        s = self.buildTree(math.floor((n-1)/2.0), r.right)
        r.right = s.left
        s.left = r
        return s

    #def rebuildTree(self, size, scapegoat, parents):
    #    head = self.flatten(scapegoat, None)
    #    self.buildTree(size, head)
    #    print "HERE"
    #    while head.parent != None:
    #        head = head.parent
    #    head = parents[-1]
    #    return head

    def rebuildTree(self, n, scapegoat):
        w = Node(-1)
        z = self.flatten(scapegoat, w)
        self.buildTree(n, z)
        return w.left

    def preOrder(self, x):
        if x != None:
            print x.key
            self.preOrder(x.left)
            self.preOrder(x.right)

    def printTree(self):
        self.preOrder(self.root)


def main():
    f = open('tree.txt', 'r')
    t = None
    for line in f.readlines():
        line = re.split(r'\s+', line) 
        cmd = line[0]
        if cmd == "BuildTree":
            t = ScapeGoatTree(float(line[1]))
            t.insert(int(line[2]))
        elif cmd == "Insert":
            t.insert(int(line[1]))




main()
#t = ScapeGoatTree(0.57)
##nums = [2,1,6,5,4,3,15,12,9,7,11,10,13,14, 15,16,17,18,8]
##nums = [5,3,7,6,8,9]
#nums = [8,1,13,10,20,19,22, 29]
#for e in nums:
#    t.insert(e)
##print "----------------"
##t.delete(13)
#t.printTree()
