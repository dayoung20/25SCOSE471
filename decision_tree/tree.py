from decision_tree.node import TreeNode
from datatype.feature import *
import math
from decision_tree.match_rule import *
from decision_tree.util import *

class DecisionTree:
    def __init__(self, features, purity_measure='std-var', max_depth=None):
        self.root = TreeNode()
        self.features = features
        self.max_depth = max_depth
        self.purity_measure = purity_measure

    def build(self, data, class_label):
        self.root = TreeNode()
        self._build_recur(self.root, data, class_label, 0)

    def _build_recur(self, node, data, class_label, depth):
        if depth == self.max_depth:
            if len(data) == 0:
                node.value = 0
                return
            node.value = sum([x['class_label'] for x in data]) / len(data)
            return
        
        impurity = self._get_impurity(data, class_label)
        # impurity condition
        if impurity < 0.1:
            if len(data) == 0:
                node.value = 0
                return
            node.value = sum([x['class_label'] for x in data]) / len(data)
            return

        # max gain ratio
        max_gr = -math.inf
        feature_name = ''
        value = ''
        split_type = ''

        for feature in self.features:
            # ignore class label feature
            if feature == class_label:
                continue

            if feature.type == FeatureType.BOOLEAN:
                splits = [
                    [x for x in data if x[feature.name]],
                    [x for x in data if not x[feature.name]]
                ]
                gr = self._get_gain_ratio(impurity, splits)
                if gr > max_gr:
                    max_gr = gr
                    feature_name = feature.name
                    value = True
                    split_type = 'eq'
            elif feature.type == FeatureType.NOMINAL:
                all_values = set([x[feature.name] for x in data])
                
                # type 1: x | others
                for v in all_values:
                    splits = [
                        [x for x in data if x[feature.name] == v],
                        [x for x in data if x[feature.name] != v]
                    ]
                    gr = self._get_gain_ratio(impurity, splits)
                    if gr > max_gr:
                        max_gr = gr
                        feature_name = feature.name
                        value = v
                        split_type = 'eq'

                # type 2 : x | y | z
                splits = [[y for y in data if y[feature.name] == x] for x in all_values]
                gr = self._get_gain_ratio(impurity, splits)
                if gr > max_gr:
                    max_gr = gr
                    feature_name = feature.name
                    split_type = 'all'
            elif feature.type == FeatureType.NUMERICAL:
                all_values = list(set([x[feature.name] for x in data])).sort()
                for i, v in enumerate(all_values[:-1]):
                    mid = (all_values[i] + all_values[i+1]) / 2
                    splits = [
                        [x for x in data if x[feature.name] < mid],
                        [x for x in data if x[feature.name] >= mid]
                    ]
                    gr = self._get_gain_ratio(impurity, splits) 
                    if gr > max_gr:
                        max_gr = gr
                        feature_name = feature.name
                        value = mid
                        split_type = 'less_than'
                

        # split and build recursively
        if split_type == 'eq':
            eq_node = TreeNode(EQ(feature_name, value))
            not_eq_node = TreeNode(NOT(EQ(feature_name, value)))
            node.children = [eq_node, not_eq_node]
            self._build_recur(eq_node, {x for x in data if x[feature_name] == value}, class_label, depth+1)
            self._build_recur(not_eq_node, {x for x in data if x[feature_name] != value}, class_label, depth+1)
        elif split_type == 'less_than':
            less_node = TreeNode(LESS_THAN(feature_name, value))
            larger_node = TreeNode(NOT(LESS_THAN(feature_name, value)))
            node.children = [less_node, larger_node]
            self._build_recur(less_node, {x for x in data if x[feature_name] < value}, class_label, depth+1)
            self._build_recur(larger_node, {x for x in data if x[feature_name] >= value}, class_label, depth+1)
        elif split_type == 'all':
            all = set([x[feature_name] for x in data])
            node.children = []
            for v in all:
                node.children.append(TreeNode(EQ(feature_name, v)))
                self._build_recur(node.children[-1], {x for x in data if x[feature_name] == v}, class_label, depth+1)

    def _get_impurity(self, data, class_label):
        if self.purity_measure == 'std-var':
            return get_std_var([x['class_label'] for x in data])
        elif self.purity_measure == 'gini':
            return get_gini_index([x['class_label'] for x in data])
        elif self.purity_measure == 'entropy':
            return get_entropy([x['class_label'] for x in data])
        
    def _get_gain_ratio(self, impurity, splits):
        cnt = sum([len(x) for x in splits])
        tmp = [self._get_impurity(data) * len(data) / cnt for data in splits]
        return (impurity - sum(tmp)) / get_split_info([len(x) for x in splits])

    def predict(self, x):
        current = self.root
        while current.children != None:
            current = current.route(x)
            if current == None:
                raise Exception('자식 노드 탐색 실패')
        return current.value

    
