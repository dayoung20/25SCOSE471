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
            id = 0
            for row in csvreader:
                self.instances.append(Instance(row, id))
                id += 1


    # 두가지 attribute 사용
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
        self.valid_instances = valid_instances 
        return np.array(data)

    
    def preprocess_features_avgStudy_avgDiff(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_study = float(inst.features[7])  # avg_study
                avg_diff = float(inst.features[8])   # avg_diff
                data.append([avg_study, avg_diff])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances 
        return np.array(data)
    
    def preprocess_features_avgScore_avgPerformance(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_score = float(inst.features[6])  # avgScore
                avg_performance = float(inst.features[9])   # avgPerformance
                data.append([avg_score, avg_performance])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances  
        return np.array(data)
    
    def preprocess_features_avgPerformance_avgSatisfaction(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_performance = float(inst.features[9])  # avgPerformance
                avg_satisfaction = float(inst.features[10])   # avgSatisfaction
                data.append([avg_performance, avg_satisfaction])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances  
        return np.array(data)
    

    # 세가지 attribute 사용
    def preprocess_features_avgScore_diff_perf(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_score = float(inst.features[6])  # Average Score
                avg_diff = float(inst.features[8])   # avg_diff
                avg_perf = float(inst.features[9])   # avg_performance
                data.append([avg_score, avg_diff, avg_perf])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances
        return np.array(data)
    
    def preprocess_features_avgStudy_diff_satis(self):
        data = []
        valid_instances = []
        for inst in self.instances:
            try:
                avg_study = float(inst.features[7])  # avg_study
                avg_diff = float(inst.features[8])   # avg_diff
                avg_satisfaction = float(inst.features[10])   # avg_satisfaction
                data.append([avg_study, avg_diff, avg_satisfaction])
                valid_instances.append(inst)
            except ValueError:
                continue
        self.valid_instances = valid_instances
        return np.array(data)
    
    

    

    def kmeans_clustering(self):
        feature_matrix = self.preprocess_features_avgStudy_diff_satis()
        self.kmeans_model = KMeans(n_clusters=self.num_clusters, random_state=42)
        self.kmeans_model.fit(feature_matrix)

        labels = self.kmeans_model.labels_
        for inst, label in zip(self.valid_instances, labels):
            inst.label = label

    def visualize_clusters_3d(self):
        data = self.preprocess_features_avgStudy_diff_satis()
        labels = self.kmeans_model.labels_

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(
            data[:, 0], data[:, 1], data[:, 2],
            c=labels,
            cmap='viridis',
            s=40,
            edgecolors='k'
        )

        ax.set_xlabel("Average Study")
        ax.set_ylabel("Average Diff")
        ax.set_zlabel("Average Satisfaction")
        ax.set_title("KMeans Clustering (3D)")
        fig.colorbar(scatter, label='Cluster')
        plt.show()

    def visualize_clusters(self):
        data = self.preprocess_features_avgPerformance_avgSatisfaction()
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

        plt.xlabel("Average Performance")
        plt.ylabel("Average Satisfaction")
        plt.title("KMeans Clustering Results")
        plt.grid(True)
        plt.colorbar(scatter, label='Cluster Label')
        plt.show()

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
    clustering.visualize_clusters_3d()
