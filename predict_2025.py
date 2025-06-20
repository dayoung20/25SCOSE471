from decision_tree.tree import *
from datatype.feature import *
from feature_selector import *
from web_scraper import courses_scraper
import csv

features = get_features(filter=['담당교수', '개설학과', '학점', '강의시간'])

courses = courses_scraper.get_courses('2025', '1R')

courses = [x for x in courses if x['department'] == '컴퓨터학과']

for c in courses:
    c['담당교수'] = c['prof_nm']
    c['개설학과'] = c['department']
    c['학점'] = float(c['time'].split('(')[0])
    c['강의시간'] = float(c['time'].split('(')[1][:-1])

class_label = 'course evaluation'
data = []

with open('merged_preprocessing.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        flag = False
        if row[class_label] != None and row[class_label] != '':
            row[class_label] = float(row[class_label])
            flag = True
        if row['개설학과'] != '컴퓨터학과':
            flag = False
        if flag:
            data.append(row)

for x in data:
    for f in features:
        if f.type == FeatureType.NUMERICAL:
            x[f.name] = float(x[f.name])

tree = DecisionTree(features=features, max_depth=10)
tree.build(data, class_label)

result = []

for c in courses:
    try:
        pred = tree.predict(c)
    except:
        pred = 0.0
    result.append((pred, c))

result.sort(reverse=True, key=lambda x:x[0])

result_major = [x for x in result if '전공' in x[1]['isu_nm']]

print(f'예측 강의 수 : {len(courses)} ({len([1 for x in result if x[0] != 0.0])})')

print('\n컴퓨터학과 강의 ===============')
for pred, c in result[:30]:
    print(f"{pred:.2f} {c['cour_cd']}-{c['cour_cls']} {c['cour_nm']} {c['담당교수']}")

print("\n컴퓨터학과 전공 강의 ==========")
for pred, c in result_major[:30]:
    print(f"{pred:.2f} {c['cour_cd']}-{c['cour_cls']} {c['cour_nm']} {c['담당교수']}")

print("\n예측 실패 ==========")
for pred, c in [x for x in result if x[0] == 0.0]:
    print(f"{pred:.2f} {c['cour_cd']}-{c['cour_cls']} {c['cour_nm']} {c['담당교수']}")