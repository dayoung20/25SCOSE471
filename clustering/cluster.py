import numpy as np

feature_category = {
    'nominal' : ['Unnamed: 0', 'ID', 'Title', '담당교수', '교과목명'], 
    'categorical' : ['Class', 'Semester', '개설학과'],
    'ordinal' : ['Year', ], 
    'numerical' : ['Average Score', 'avg_study', 'avg_diff', 'avg_performance', 'avg_satisfaction', 'recc_rate', '학점', '강의시간', '시험', '출석', '과제', '참여도', '발표', '프로젝트', '협동', '보고서', '실험', '태도', '기타'], 
    'etc' : ['학과제한'],
    'binary' : []
}

class Instance:
    def __init__(self, features, id, feature_category2idx):
        self.features = {}
        self.id = id
        self.label = None
        self.feature_category2idx = feature_category2idx
        self.split_features(features)
    
    def split_features(self, features):
        self.feature_types = feature_category.keys()
        for ftype in self.feature_types:
            self.features[ftype] = np.array([])
        for ftype in self.feature_types:
            self.features[ftype] = np.append(self.features[ftype], features.iloc[self.feature_category2idx[ftype]])