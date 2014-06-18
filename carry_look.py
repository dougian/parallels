from math import ceil
class Node(object):
    '''
        A node of the tree. Knows its children and its value.
    '''

    value = ''
    left_son = None
    right_son = None
    parent = None
    level = 0

    def __init__(self, data, level, l_son=None, r_son=None):
        self.value = data
        self.level = level
        self.left_son = l_son
        self.right_son = r_son
        self.buff = []

    def __str__(self):
        #return "Node on level %d, value %d " % (self.level, self.value)
        return "{%s} " % (self.value)


    def __repr__(self):
        #return "Node on level %d, value %d " % (self.level, self.value)
        return "{%s} " % (self.value)

    def compute_value(self):
        l_val = self.right_son.value
        r_val = self.left_son.value

        if l_val == 's' or r_val == 's':
            self.value = 's'
        else:
            if l_val == 'g' or r_val == 'g':
                self.value = 'g'
            else:
                self.value = 'p'

    def is_leaf(self):
        return self.left_son == None and self.right_son == None

class lookupTree(object):

    '''
    A carry lookahead tree. It's a binary tree, but initially there are only leaves
    round by round the nodes are populated, built from ground-up.
    '''
    def __init__(self):
        self.root = None


    def build_tree(self, valuesvec):
        '''
            Builds an initial binary tree with values of valuesvec as leaves and
            nodes with value 0 acting as their parents.
            Returns the root of the tree to the user
        '''
        nodes = [Node(val, 0) for val in valuesvec]

        num_pairs = len(valuesvec) / 2
        it = 0

        while(num_pairs > 0):

            it += 1
            temp = [Node(0, it, nodes[2*i], nodes[2*i+1]) for i in range(int(num_pairs))]

            if len(temp) == 1:
                self.root = temp[0]

            #print(temp)

            nodes = temp
            num_pairs = len(nodes) / 2

        return self.root



    def printTree(self, root):
        '''
            Prints the tree.
        '''
        if root == None:
            pass
        else:
            self.printTree(root.left_son)
            ind = "\t" * root.level
            print(ind + str(root))
            self.printTree(root.right_son)


    def propagate_up(self, root, step):

        if root.level == step:
            root.compute_value()
            root.buff.append(root.right_son.value)

        else:
            self.propagate_up(root.left_son, step)
            self.propagate_up(root.right_son, step)

    def propagate_down(self, root):

        if len(root.buff) > 0 :
            if not root.is_leaf():
                temp = root.buff[0]
                root.left_son.buff.append(temp)
                root.buff.remove(temp)
            else:
                root.value = root.buff[0]
        else:
            self.propagate_down(root.left_son)
            self.propagate_down(root.right_son)


a  = ['g','s','g','p']
mytree = lookupTree()
r = mytree.build_tree(a)
mytree.printTree(r)
mytree.propagate_up(r,1)
mytree.printTree(r)
mytree.propagate_down(r)
mytree.printTree(r)



__author__ = 'dougian'
