from decision_tree.tree import DecisionTree
from datatype.feature import *

features = [
    Feature('a', FeatureType.BOOLEAN),
    Feature('b', FeatureType.NOMINAL),
    Feature('c', FeatureType.NUMERICAL)
]

tree = DecisionTree(features)
tree.build(None)