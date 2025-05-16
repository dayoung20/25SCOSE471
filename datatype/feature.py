from enum import Enum

class FeatureType(Enum):
    BOOLEAN = 'boolean'
    NOMINAL = 'nominal'
    NUMERICAL = 'numerical'

class Feature:
    def __init__(self, name, type):
        self.name = name
        self.type = type