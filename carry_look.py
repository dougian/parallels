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
        return "Value = %d", self.value

class lookupTree(object):

    def __init__(self):
        self.root = None


    def build_tree(self, valuesvec):

        nodes = [Node(val, 0) for val in valuesvec]

        num_pairs = ceil(len(valuesvec) / 2)
        it = 0

        while(num_pairs > 0):

            it += 1
            temp = [Node(0, it, nodes[i], nodes[i+1]) for i in range(int(num_pairs))]

            if len(temp) == 1:
                self.root = temp[0]

            for j in temp:
                print(j.value, j.level)
            nodes = temp
            num_pairs = len(nodes) / 2

    def printTree(self, root):
        if root == None:
            pass
        else:
            self.printTree(root.left_son)
            print(root.value)
            self.printTree(root.right_son)


a  = [1, 2, 3, 4]
mytree = lookupTree()
mytree.build_tree(a)
print(mytree.root.value, mytree.root.level)
mytree.printTree(mytree.root)


__author__ = 'dougian'
