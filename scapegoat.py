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

    def sizeOf(self, x):
        if x == None:
            return 0
        return 1 + self.sizeOf(x.left) + self.sizeOf(x.right)

    def haT(self):
        return math.floor(math.log(self.size, 1.0/self.a))

    def isDeep(self, depth):
        return depth > self.haT()

    def brother(self, x):
        pass

    def brotherOf(self, parent, child):
        if parent.left != None and parent.left.key == child.key:
            return parent.right
        elif parent.right != None:
            return parent.left
        return None

    def myFlatten(self, node, nodes):
        if node == None:
            return
        self.myFlatten(node.left, nodes)
        nodes.append(node)
        self.myFlatten(node.right, nodes)

    def myRebuildTree(self, x, size):
        nodes = []
        self.myFlatten(x, nodes)
        def helper(nodes, start, end):
            if start > end:
                return None
            mid = start + (end - start) / 2;
            node = Node(nodes[mid].key)
            node.left = helper(nodes, start, mid-1)
            node.right = helper(nodes, mid+1, end)
            return node

        return helper(nodes, 0, size-1)
        


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
                sizes[i] = sizes[i-1] + self.sizeOf(self.brotherOf(parents[i], parents[i-1])) + 1
                if not self.isAWeightBalanced(parents[i], sizes[i]+1):
                    scapegoat = parents[i]
                    I = i
            print "Node %d is not weight balanced and could be a scapegoat" % (parents[I].key)
            
            print "found scapegoat, it's = %d, with size %d" % (scapegoat.key, sizes[I])
            #tmp = self.rebuildTree(sizes[i], scapegoat)
            #tmp = self.rebuildTree(sizes[i]+1, scapegoat)
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

    def flatten(self, x, y):
        if x == None:
            return y
        x.right = self.flatten(x.right, y)
        return self.flatten(x.left, x)

    def buildTree(self, n, x):
        if n == 0:
            x.left = None
            return x
        r = self.buildTree(math.ceil((n-1)/2.0), x)
        s = self.buildTree(math.floor((n-1)/2.0), r.right)
        r.right = s.left
        s.left = r
        return s

    def rebuildTree(self, n, scapegoat):
        w = Node(-20)
        z = self.flatten(scapegoat, w)
        next_ = z
        result = []
        while next_ != None:
            result.append(next_.key)
            next_ = next_.right
        print ("flattend tree with %d nodes => " + str(result)) % (n)
        self.buildTree(n, z)
        return w.left

    def preOrder(self, x):
        if x != None:
            print x.key
            self.preOrder(x.left)
            self.preOrder(x.right)

    def printTree(self):
        self.preOrder(self.root)


t = ScapeGoatTree(0.57)
#nums = [2,1,6,5,4,3,15,12,9,7,11,10,13,14, 15,16,17,18,8]
#nums = [5,3,7,6,8,9]
nums = [8,1,13,10,20,19,22, 29]
for e in nums:
    t.insert(e)
print "----------------"
t.printTree()
