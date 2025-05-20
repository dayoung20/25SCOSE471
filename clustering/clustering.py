import os
import csv
# import pandas as pd

import cluster

# from kmodes.kmodes import KModes

class Clustering:
    def __init__(self):
        self.instances = []
        self.clusters = []
        self.num_clusters = 0
    
    def load_data(self):
        # data 위치할 파일 임의로 /data로 설정, 추후 수정 가능 
        data_path = os.path.abspath('') + '/data' + '/final.csv'
        with open(data_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)
            for row in csvreader:
                self.instances.append(cluster.Instance(row))
    
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
