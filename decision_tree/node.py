
class TreeNode:
    def __init__(self, match_rule=None, value=None, children=None, ):
        self.match_rule = match_rule
        self.children = children
        self.value = value

    def route(self, x):
        if self.children == None:
            return None
        for child in self.children:
            if child.math_rule(x):
                return child
        return None
