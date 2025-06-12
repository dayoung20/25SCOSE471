from decision_tree.tree import *
from datatype.feature import *
from feature_selector import *
from random import shuffle
import csv

features = get_features(filter=[''])

data = []
classes = ['course evaluation', 'learning load', 'course difficulty', 'teaching ability', 'achievement level']
class_label = 'course evaluation'

with open('merged_preprocessing.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        flag = False
        for class_label in classes:
            if row[class_label] != None and row[class_label] != '':
                row[class_label] = float(row[class_label])
                flag = True
        if flag:
            data.append(row)

for x in data:
    for f in features:
        if f.type == FeatureType.NUMERICAL:
            x[f.name] = float(x[f.name])

print(len(data))

shuffle(data)
tmp = math.ceil(len(data)*0.7)
train_data = data[:tmp]
test_data = data[tmp:]

def get_mae(tree, test_data, class_label):
    error_sum = 0.0
    for item in test_data:
        pred = tree.predict(item)
        if pred == None:
            pred = 0.0
        error_sum += abs(item[class_label] - pred)
    return error_sum / len(test_data)

for class_label in classes:
    tree = DecisionTree(features, max_depth=100)
    
    # train_data 대신 data로 train 시킨다.
    # 만약 train_data로 학습시켜서 빠지는 교수님 정보가 생긴다면 test_data에서 오류가 생길 수 있어서..
    tree.build(data, class_label)

    mae_all = get_mae(tree, test_data, class_label)

    f_list = []

    for f in features:
        new_features = [fe for fe in features if fe is not f]
        new_tree = DecisionTree(new_features, max_depth=100)
        new_tree.build(data, class_label)
        mae = get_mae(new_tree, test_data, class_label)
        f_list.append((abs(mae_all - mae), f.name))

    f_list.sort(reverse=True)
    print('\nClass label =', class_label)
    for a, b in f_list:
        print(f"{a:.6f} {b}")
