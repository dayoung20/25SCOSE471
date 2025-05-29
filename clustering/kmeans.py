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

    def preprocess_features_avgScore_avgStudy(self):
        """
        Average Score와 avg_study만 추출하여 벡터 생성 + 유효 인스턴스 저장
        """
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_score = float(inst.features[6])  # Average Score의 인덱스
                avg_study = float(inst.features[7])  # avg_study의 인덱스
                data.append([avg_score, avg_study])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances  # 👈 여기 추가!
        return np.array(data)

    
    def preprocess_features_avgStudy_avgDiff(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_score = float(inst.features[7])  # avg_study
                avg_diff = float(inst.features[8])   # avg_diff
                data.append([avg_score, avg_diff])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances  # ← 따로 저장
        return np.array(data)


    def visualize_clusters(self):
        data = self.preprocess_features_avgStudy_avgDiff()
        labels = self.kmeans_model.labels_

        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(
            data[:, 0],  # x축
            data[:, 1],  # y축
            c=labels,
            cmap='viridis',
            s=50,
            edgecolors='k'
        )

        plt.xlabel("Average Study")
        plt.ylabel("Average Diff")
        plt.title("KMeans Clustering Results")
        plt.grid(True)
        plt.colorbar(scatter, label='Cluster Label')
        plt.show()

    # def kmeans_clustering(self):
    #     feature_matrix = self.preprocess_features_avgStudy_avgDiff()

    #     self.kmeans_model = KMeans(n_clusters=self.num_clusters, random_state=42)
    #     self.kmeans_model.fit(feature_matrix)

    #     labels = self.kmeans_model.labels_

    #     # 결과 저장
    #     for inst, label in zip(self.instances, labels):
    #         inst.label = label

    def kmeans_clustering(self):
        feature_matrix = self.preprocess_features_avgScore_avgStudy()
        self.kmeans_model = KMeans(n_clusters=self.num_clusters, random_state=42)
        self.kmeans_model.fit(feature_matrix)

        labels = self.kmeans_model.labels_
        for inst, label in zip(self.valid_instances, labels):
            inst.label = label


    def print_clusters(self):
        clusters = {}
        for inst in self.instances:
            clusters.setdefault(inst.label, []).append(inst.id)

        for cid, member_ids in clusters.items():
            print(f"Cluster {cid} | Size: {len(member_ids)}")
            print(f"Sample IDs: {member_ids[:10]} ...\n")  # 처음 10개만 표시


if __name__ == "__main__":
    clustering = Clustering(num_clusters=3)
    clustering.load_data()
    clustering.kmeans_clustering()
    clustering.print_clusters()
    clustering.visualize_clusters()
