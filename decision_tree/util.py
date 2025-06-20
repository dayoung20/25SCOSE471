import math
from collections import Counter

def get_std_var(data):
    if len(data) == 0:
        return 0.0
    avg = sum([x for x in data]) / len(data)
    std = math.sqrt(sum([(x-avg)**2 for x in data])/len(data))
    return std

def get_gini_index(data):
    n = len(data)
    if n == 0:
        return 0.0
    
    counter = Counter(data)
    impurity = 1.0
    for x in counter:
        impurity -= (counter[x]/n)**2
    return impurity

def get_entropy(data):
    n = len(data)
    if n == 0:
        return 0.0
    
    counter = Counter(data)
    ent = 0.0
    for x in counter:
        prob = counter[x]/n
        if prob > 0:
            ent -= prob * math.log2(prob)
    return ent

def get_split_info(counts):
    n = sum(counts)
    ent = 100.0
    for x in counts:
        prob = x / n
        if prob > 0:
            ent -= prob * math.log2(prob)
    return ent
