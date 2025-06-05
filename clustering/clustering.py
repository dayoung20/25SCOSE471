import os
import csv
import copy
from queue import Queue
import pandas as pd
import numpy as np

import cluster
import torch
import torch.nn as nn

# from kmodes.kmodes import KModes

feature_category = {
    'nominal' : ['Unnamed: 0', 'ID', 'Title', '담당교수', '교과목명'], 
    'categorical' : ['Class', 'Semester', '개설학과'],
    'ordinal' : ['Year', ], 
    'numerical' : ['Average Score', 'avg_study', 'avg_diff', 'avg_performance', 'avg_satisfaction', 'recc_rate', '학점', '강의시간', '시험', '출석', '과제', '참여도', '발표', '프로젝트', '협동', '보고서', '실험', '태도', '기타'], 
    'etc' : ['학과제한'],
    'binary' : []
}

class Clustering:
    def __init__(self, file_name):
        self.instances = []
        self.clusters = {}
        self.cluster_cnt = 0
        self.num_clusters = 0
        self.neighbor_ids = {}

        self.load_data(file_name)
    
    def binary_feature_index(self, features):
        self.binary_feature_indices = []
        for i, f in enumerate(features):
            if type(f) == np.bool:
                self.binary_feature_indices.append(i)

    def key_to_index(self, features):
        feature_keys = list(features.index)
        for f in feature_keys:
            is_binary = True
            for category in feature_category.keys():
                if f in feature_category[category]:
                    is_binary = False
                    break
            if is_binary:
                feature_category['binary'].append(f)

        self.feature_category2idx = {}
        for category, key in feature_category.items():
                self.feature_category2idx[category] = [feature_keys.index(k) for k in key]

    def load_data(self, file_name):
        # data 위치할 파일 임의로 /data로 설정, 추후 수정 가능 
        data_path = os.path.abspath('../') + '/data/' + file_name
        data = pd.read_csv(data_path)

        self.key_to_index(data.iloc[0])

        for i in range(len(data)):
            self.instances.append(cluster.Instance(data.iloc[i], data.iloc[i, 0], self.feature_category2idx))
        self.feature_types = self.instances[0].feature_types
    
    def binary_dissimilarity(self, inst1, inst2):
        '''
        calculates dissimilarity based on binary features between two distinct data instances

        :param inst1: first data instance
        :param inst2: second data instance
        '''
        assert inst1 != inst2

        diff_cnt = sum(inst1.features.iloc[self.binary_feature_indices] != inst2.features.iloc[self.binary_feature_indices])
        binary_features_cnt = len(self.binary_feature_indices)

        dissim = diff_cnt / binary_features_cnt
        return dissim

    def gower_dissimilarity(self, inst1, inst2, ranges=None, ordinals=None):
        """
        calculates gower dissimilarity based on various features between two distinct data instances

        :param inst1: first data instance
        :param inst2: second data instance 
        :param ranges: list of (min, max) for each numerical/ordinal feature
        :param ordinals: list of lists specifying the order for each ordinal feature (optional)
        """
        assert inst1 != inst2

        x = inst1.features
        y = inst2.features

        assert len(x) == len(y) == len(self.feature_types)
        dissim = 0.0
        valid = 0

        for ftype in self.feature_types:
            if ftype == 'numerical':
                if ranges is not None and ranges[ftype] is not None:
                    min_, max_ = ranges[ftype]
                    denom = max_ - min_
                    if denom == 0:
                        continue
                    dissim += sum(abs(x[ftype] - y[ftype])) / denom
                else:
                    dissim += sum(abs(x[ftype] - y[ftype])) / (np.nanmax([x[ftype], y[ftype]]) - np.nanmin([x[ftype], y[ftype]]) + 1e-9)
                valid += 1
            elif ftype == 'binary':
                dissim += sum(x[ftype] != y[ftype])
                valid += 1
            elif ftype == 'categorical':
                dissim += sum(x[ftype] != y[ftype])
                valid += 1
            elif ftype == 'ordinal':
                if ordinals is not None and ordinals[ftype] is not None:
                    order = ordinals[ftype]
                    xi = order.index(x[ftype])
                    yi = order.index(y[ftype])
                    denom = len(order) - 1
                    if denom == 0:
                        continue
                    dissim += sum(abs(xi - yi)) / denom
                    valid += 1
                elif ranges is not None and ranges[ftype] is not None:
                    min_, max_ = ranges[ftype]
                    denom = max_ - min_
                    if denom == 0:
                        continue
                    dissim += sum(abs(x[ftype] - y[ftype])) / denom
                    valid += 1
                else:
                    dissim += sum(x[ftype] != y[ftype])
                    valid += 1
            else:
                pass

        return dissim / valid if valid > 0 else 0.0

    def get_neighbor_ids(self, center, radius):
        if center.id in self.neighbor_ids.keys():
            return self.neighbor_ids[center.id]
        neighbor_ids = []
        for inst in self.instances:
            if inst == center:
                continue
            if self.dissimilarity(center, inst) <= radius:
                neighbor_ids.append(inst.id)
        self.neighbor_ids[center.id] = neighbor_ids
        return neighbor_ids

    def dbscan(self, radius, minPts):
        checkpoint = 10
        for idx, inst in enumerate(self.instances):
            if idx / len(self.instances) * 100 > checkpoint:
                print(idx / len(self.instances) * 100)
                checkpoint += 10


            if inst.label is not None:
                continue
            neighbor_ids = self.get_neighbor_ids(inst, radius)
            if len(neighbor_ids) < minPts:
                inst.label = -1 # denotes noise instance
                continue
            self.cluster_cnt += 1
            self.clusters[self.cluster_cnt] = []
            inst.label = self.cluster_cnt
            self.clusters[self.cluster_cnt].append(inst)

            seed_set = Queue()
            for neighbor_id in neighbor_ids:
                seed_set.put(neighbor_id)
            
            while not seed_set.empty():
                curr_id = seed_set.get()
                curr_instance = self.instances[curr_id]

                if curr_instance.label == -1:
                    curr_instance.label = self.cluster_cnt
                    self.clusters[self.cluster_cnt].append(curr_instance)
                elif curr_instance.label is None:
                    curr_instance.label = self.cluster_cnt
                    self.clusters[self.cluster_cnt].append(curr_instance)

                    n_neighbor_ids = self.get_neighbor_ids(curr_instance, radius)

                    if len(n_neighbor_ids) >= minPts:
                        for n_neighbor_id in n_neighbor_ids:
                            if self.instances[n_neighbor_id].label is None or self.instances[n_neighbor_id].label == -1:
                                seed_set.put(n_neighbor_id)