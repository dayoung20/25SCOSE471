
class TreeNode:
    def __init__(self, match_rule=None, match_rule_str='', value=None, children=None):
        self.match_rule = match_rule
        self.match_rule_str = match_rule_str
        self.children = children
        self.value = value

    def route(self, x):
        if self.children == None:
            return None
        for child in self.children:
            if child.match_rule(x):
                return child
        return None
