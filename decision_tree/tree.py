from decision_tree.node import TreeNode
from datatype.feature import *

class DecisionTree:
    def __init__(self, features, max_depth=None):
        self.root = TreeNode()
        self.features = features
        self.max_depth = max_depth

    def build(self, data):
        self._build_recur(self.root, data)

    def _build_recur(self, node, data):
        for feature in self.features:
            print(feature.type, feature.name)


    def predict(self, x):
        NotImplemented

    