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

    def __str__(self):
        return "{%s}" % self.value


    def __repr__(self):
        return "{%s}" % self.value

    def compute_value(self):
        l_val = self.right_son.value
        r_val = self.left_son.value

        if l_val == 'p':
            self.value = r_val
        elif l_val == 's':
            if r_val == 'g':
                self.value = r_val
            else:
                self.value = 's'
        else:
            if r_val == 's':
                self.value = r_val
            else:
                self.value = 'g'


    def set_val(self):
        pass

    def is_leaf(self):
        return self.left_son == None and self.right_son == None

    def is_done(self):
        return self.done

    def transmit(self):
        if self.value != '0' and not self.is_leaf():
            if not self.level == 1:
                self.right_son.value = self.value
                self.left_son.value = self.value
            else:
                if not self.right_son.done and not self.value == 'p':
                    self.right_son.value = self.value
                    self.right_son.done = True
                if not self.left_son.done and not self.value == 'p':
                    self.left_son.value = self.value
                    self.left_son.done = True


class lookahead_Tree(object):
    '''
    A carry lookahead tree. It's a binary tree, but initially there are only leaves
    round by round the nodes are populated, built from ground-up.
    '''

    def __init__(self):
        self.root = None
        self.result = '0'

    def get_depth(self):
        return self.root.level + 1

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
            nodes = temp
            num_pairs = len(nodes) / 2

        return self.root


    def print_tree(self, root):
        '''
            Prints the tree.
        '''
        if root == None:
            pass
        else:
            self.print_tree(root.left_son)
            ind = "\t" * root.level
            print(ind + str(root))
            self.print_tree(root.right_son)


    def leaves_array(self, root):
        '''
            Returns the leaves of the tree as an array.
        '''
        arr = []
        if root.is_leaf():
            arr.append(root)
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


    def propagate_down(self, root, step):
        '''
            Performs an downwards step, sending values that the nodes received from the right child
            to the children of a node (both of them) as explained in the carry lookahead algorithm
        '''
        d = self.get_depth() - 1
        if (root.level == step - 1 or root.level == 2 * d - step + 1 ) and not root.is_leaf():
            #print('changes on level %d' %root.level)
            #take the value from the right son, give it to the left son
            #delete your own value.
            if root.right_son.value != '0' and step <= self.get_depth():
                root.left_son.value = root.right_son.value
                if root.left_son.value != 'p' and root.left_son.is_leaf():
                    root.left_son.done = True
                root.right_son.value = '0'
                #root.value = '0'

            #exception of the rule is for the root:
            if step == self.get_depth():
                #print("Root value: %s " % root.value)
                self.result = root.value
                root.value = 's'

            self.propagate_down(root.left_son, step)
            self.propagate_down(root.right_son, step)

        else:
            if not root.is_leaf():
                self.propagate_down(root.left_son, step)
                self.propagate_down(root.right_son, step)

        if step > root.level + 1:
            root.transmit()


    def propagating_values(self, root):
        leaves = self.leaves_array(root)
        done_trees = [l.is_done() for l in leaves]
        return all(done_trees)


    def run(self, r):
        step = 0
        depth = self.get_depth()
        while not self.propagating_values(r):
            step += 1
            if step < depth:
                self.propagate_up(r, step)
            self.propagate_down(r,step)
        res = [l.value for l in self.leaves_array(r)]
        res = [self.result] + res
        return (res, step)



__author__ = 'dougian'
