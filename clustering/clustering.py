import os
import csv
import copy
from queue import Queue
import pandas as pd
import numpy as np

import cluster

# from kmodes.kmodes import KModes

class Clustering:
    def __init__(self, file_name):
        self.instances = []
        self.clusters = {}
        self.cluster_cnt = 0
        self.num_clusters = 0
        self.neighbor_ids = {}
        
        self.load_data(file_name)
    
    def load_data(self, file_name):
        # data 위치할 파일 임의로 /data로 설정, 추후 수정 가능 
        data_path = os.path.abspath('../') + '/data/' + file_name
        data = pd.read_csv(data_path)

        self.key_to_index(data.iloc[0])

        for i in range(len(data)):
            self.instances.append(cluster.Instance(data.iloc[i], data.iloc[i, 0], self.feature_category2idx))
        self.feature_types = self.instances[0].feature_types
    
    def dissimilarity(self, inst1, inst2):
        '''
        calculates dissimilarity between two distinct data instances

        :param inst1: first data instance
        :param inst2: second data instance
        '''
        assert inst1 != inst2

        total_features_cnt = len(inst1.features)
        TF_features_cnt = 0
        diff_cnt = 0
        for i in range(total_features_cnt):
            if inst1.features[i].lower() in ['true', 'false'] or inst2.features[i].lower() in ['true', 'false']:
                TF_features_cnt += 1
                if inst1.features[i] != inst2.features[i]:
                    diff_cnt += 1
        dissim = diff_cnt / TF_features_cnt
        return dissim

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