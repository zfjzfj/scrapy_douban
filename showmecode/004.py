#coding:utf-8
#author:Elvis

class TreeNode(object):
    def __init__(self):
        self.data = '#'
        self.l_child = None
        self.r_child = None

class Tree(TreeNode):
    #create a tree
    def create_tree(self, tree):
        data = raw_input('->')
        if data == '#':
            tree = None
        else:
            tree.data = data
            tree.l_child = TreeNode()
            self.create_tree(tree.l_child)
            tree.r_child = TreeNode()
            self.create_tree(tree.r_child)

    def insertNode(self, tree):
        if self.data == "#":
            self.data = tree.data
            self.l_child = tree.l_child
            self.r_child = tree.r_child
            return
        print self.data,tree.data

        if tree.data < self.data:
            self.l_child = tree
        else:
            self.r_child = tree


    def insertdata(self, data):
        for i in data:
            print i
            node = TreeNode()
            node.data = i
            self.insertNode(node)

    #visit a tree node
    def visit(self, tree):
        #输入#号代表空树
        if tree.data is not '#':
            print str(tree.data) + '\t',
    #先序遍历
    def pre_order(self, tree):
        if tree is not None:
            self.visit(tree)
            self.pre_order(tree.l_child)
            self.pre_order(tree.r_child)

    #中序遍历
    def in_order(self, tree):
        if tree is not None:
            self.in_order(tree.l_child)
            self.visit(tree)
            self.in_order(tree.r_child)

    #后序遍历
    def post_order(self, tree):
        if tree is not None:
            self.post_order(tree.l_child)
            self.post_order(tree.r_child)
            self.visit(tree)

    def getDepth(self, tree):
        if tree is None:
            return 0

        tree_left = self.getDepth(tree.l_child)
        tree_right = self.getDepth(tree.r_child)

        return 1 + (tree_left >= tree_right and tree_left or tree_right)

t = TreeNode()
tree = Tree()
tree.insertdata([10,9,8])
tree.pre_order(t)




'''
t = TreeNode()
print t.data,t.l_child,t.r_child
tree = Tree()
print tree.data,tree.l_child,tree.r_child
print tree,type(tree)

tree.create_tree(t)
print "defpth is ",tree.getDepth(t)

tree.pre_order(t)
print '\n'
tree.in_order(t)
print '\n'
tree.post_order(t)
'''
