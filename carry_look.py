from math import ceil
class Node(object):
    value = 0
    left_son = None
    right_son = None
    parent = None
    level = 0

    def __init__(self, data, level, l_son=None, r_son=None):
        self.value = data
        self.level = level
        self.left_son = l_son
        self.right_son = r_son

    def __str__(self):
        return "Node on level %d, value %d " % (self.level, self.value)


    def __repr__(self):
        return "Node on level %d, value %d " % (self.level, self.value)

class lookupTree(object):

    def __init__(self):
        self.root = None


    def build_tree(self, valuesvec):

        nodes = [Node(val, 0) for val in valuesvec]

        num_pairs = len(valuesvec) / 2
        it = 0

        while(num_pairs > 0):

            it += 1
            temp = [Node(0, it, nodes[2*i], nodes[2*i+1]) for i in range(int(num_pairs))]

            if len(temp) == 1:
                self.root = temp[0]

            print(temp)

            nodes = temp
            num_pairs = len(nodes) / 2

        return self.root

    def printTree(self, root):
        if root == None:
            pass
        else:
            self.printTree(root.left_son)
            print(root)
            self.printTree(root.right_son)

            


a  = [1, 2, 3, 4]
mytree = lookupTree()
r = mytree.build_tree(a)
mytree.printTree(r)


__author__ = 'dougian'
