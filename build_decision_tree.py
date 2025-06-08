from decision_tree.tree import *
from datatype.feature import *
from random import shuffle
import csv

features = [
    Feature('인원제한', FeatureType.BOOLEAN),
    Feature('NeMo', FeatureType.BOOLEAN),
    Feature('영강', FeatureType.BOOLEAN),
    Feature('튜토리얼', FeatureType.BOOLEAN),
    Feature('MOOC', FeatureType.BOOLEAN),
    Feature('학점', FeatureType.NUMERICAL),
    Feature('강의시간', FeatureType.NUMERICAL),
    Feature('개설학과', FeatureType.NOMINAL),
    Feature('담당교수', FeatureType.NOMINAL),
    Feature('출석확인자율화', FeatureType.BOOLEAN),
    Feature('Flipped', FeatureType.BOOLEAN),
    Feature('상대평가', FeatureType.BOOLEAN),
    Feature('수강포기제한', FeatureType.BOOLEAN),
    Feature('교환학생', FeatureType.BOOLEAN),
    Feature('무감독시험', FeatureType.BOOLEAN),
    Feature('수업유형', FeatureType.NOMINAL),
]

class_type = ['교직', '교직(비사대)', '군사학', '전공선택', '전공필수', '평생교육사',
              '학문의기초', '학부공통']
#for t in class_type:
#    features.append(Feature('이수구분.' + t, FeatureType.BOOLEAN))

class_components = ['Q&A', '개별지도', '발표', '상시상담', '실습', '실험',
                    '이론강의', '집단지도', '체험', '퀴즈', '토론', '특강',
                    '포럼', '프로젝트', '협동학습']
#for c in class_components:
#    features.append(Feature('수업구성요소_' + c, FeatureType.BOOLEAN))

grade_type = ['P/F', '상대평가', '절대평가']
#for g in grade_type:
#    features.append(Feature('성적평가_' + g, FeatureType.BOOLEAN))

criteria = ['시험', '출석', '과제', '참여도', '발표', '프로젝트', '협동', '보고서', '실험', '태도', '기타']
for c in criteria:
    features.append(Feature(c, FeatureType.NUMERICAL))

data = []
classes = ['Average Score', 'avg_study', 'avg_diff', 'avg_performance', 'avg_satisfaction']
class_label = 'avg_satisfaction'#'Average Score'

with open('final_data.csv', 'r') as f:
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

new_data = []
for x in data:
    #if x['개설학과'] != '컴퓨터학과':
    #    continue
    sumall = sum([x[c] for c in criteria])
    if sumall == 0.0:
        new_data.append(x)
        continue
    for c in criteria:
        x[c] *= 100.0 / sumall
    new_data.append(x)

data = new_data

print(len(data))

shuffle(data)
tmp = math.ceil(len(data)*0.7)
train_data = data[:tmp]
test_data = data[tmp:]

'''
avg = 0.0
for i in train_data:
    avg += i[class_label]
avg /= len(train_data)

tree = DecisionTree(features, max_depth=100)
tree.build(data, class_label)

mse = 0.0
mae = 0.0

mse_ = 0.0
mae_ = 0.0
for item in test_data:
    pred = tree.predict(item)
    if pred == None:
        pred = 0.0
    #print(item['Average Score'], pred)
    mse += (item[class_label] - pred)**2
    mae += abs(item[class_label] - pred)
    mse_ += (item[class_label] - avg)**2
    mae_ += abs(item[class_label] - avg)

#tree.travel()

mse /= len(test_data)
mae /= len(test_data)
mse_ /= len(test_data)
mae_ /= len(test_data)
print(mse, mae)
print(mse_, mae_)
'''

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
        print(f"{a:.4f} {b}")