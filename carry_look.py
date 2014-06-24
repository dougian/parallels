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
    done = False


    def __init__(self, data, level, l_son=None, r_son=None):
        self.value = data
        self.level = level
        self.left_son = l_son
        self.right_son = r_son
        self.buff = []

    def __str__(self):
        tmp = ''
        if len(self.buff) > 0:
            tmp = self.buff[0]
        return "{%s}[%s]" % (self.value, tmp)


    def __repr__(self):
        tmp = ''
        if len(self.buff) > 0:
            tmp = self.buff[0]
        return "{%s}[%s]" % (self.value, tmp)

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

    def transmit(self):
        if not self.value == '0':
            self.right_son.value = self.value
            self.left_son.value = self.value



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

        while (num_pairs > 0):

            it += 1
            temp = [Node('0', it, nodes[2 * i], nodes[2 * i + 1]) for i in range(int(num_pairs))]

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


    def leaves_array(self, root):
        '''
            Returns the leaves of the tree as an array.
        '''
        arr = []
        if root.is_leaf():
            arr.append(root.value)
            return arr
        else:
            a = self.leaves_array(root.left_son)
            b = self.leaves_array(root.right_son)
            return a+b


    def propagate_up(self, root, step):
        '''
            Performs an upwards step, sending values from the nodes to their parents
            as explained in the carry lookahead algorithm
        '''
        #if it's time to compute value, do it
        if root.level == step:
            root.compute_value()
        else:
            if not root.is_leaf():
                self.propagate_up(root.left_son, step)
                self.propagate_up(root.right_son, step)


    def propagate_down(self, root):
        '''
            Performs an downwards step, sending values that the nodes received from the right child
            to the children of a node (both of them) as explained in the carry lookahead algorithm
        '''
        if root.level == step - 1:
            root.left_son.value = root.right_son.value
            root.right_son.value = '0'
            root.value = '0'
        else:
            if not root.is_leaf():
                self.propagate_up(root.left_son, step)
                self.propagate_up(root.right_son, step)


    def propagating_values(self, root):
        if root == None:
            return False
        else:
            assume = len(root.buff) > 0
            exist_left = assume or self.propagating_values(root.left_son)
            exist_right = assume or self.propagating_values(root.left_son)
            return exist_left or exist_right


a = ['g', 'p', 's', 'p']
#a = ['s','g','p','p','g','p','s','s','p','p','s','g','p','p','p','s']
mytree = lookupTree()
r = mytree.build_tree(a)

step = 0
mytree.printTree(r)

while step == 0 or mytree.propagating_values(r):

    step += 1
    if r.value == '0':
        mytree.propagate_up(r, step)
        print('Up')
        mytree.printTree(r)
        print()

    mytree.printTree(r)
    print()
    print('doing Down')

    mytree.propagate_down2(r)
    print("done")
    mytree.printTree(r)
    print()

print(mytree.leaves_array(r))

__author__ = 'dougian'
