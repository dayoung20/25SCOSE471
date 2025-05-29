import os
import csv
import numpy as np
from sklearn.cluster import KMeans
from cluster import Instance 
import matplotlib.pyplot as plt

class Clustering:
    def __init__(self, num_clusters):
        self.instances = []
        self.num_clusters = num_clusters
        self.kmeans_model = None

    def load_data(self):
        data_path = os.path.abspath('') + '/final_data.csv'
        with open(data_path, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  
            id = 0
            for row in csvreader:
                self.instances.append(Instance(row, id))
                id += 1

    def preprocess_features(self):
        """
        추출하여 벡터 생성
        """
        

    def kmeans_clustering(self):
        feature_matrix = self.preprocess_features()

        self.kmeans_model = KMeans(n_clusters=self.num_clusters, random_state=42)
        self.kmeans_model.fit(feature_matrix)

        labels = self.kmeans_model.labels_

        # 결과 저장
        for inst, label in zip(self.instances, labels):
            inst.label = label


if __name__ == "__main__":
    clustering = Clustering(num_clusters=3)
    clustering.load_data()
    clustering.kmeans_clustering()
