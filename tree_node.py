# Stores only what UCT needs per node: wi and ni
class TreeNode:
    def __init__(self, parent=None):
        self.wi = 0          # total score accumulated through this node
        self.ni = 0          # number of times this node has been visited
        self.parent = parent # reference to parent node
        self.children = {}   # maps column number (move) -> child TreeNode