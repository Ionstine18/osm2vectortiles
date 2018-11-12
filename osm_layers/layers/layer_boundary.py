import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_boundary(layers):
    def __init__(self):
        self.layer_type = "boundary"
        self.data_source = ['osm']
        self.fields = ['admin_level','disputed','maritime']
        
    def condition(self, feature):
        var_list = ['admin_level']
        tmp = combined_keys(feature, var_list)
        return tmp
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "boundary" }
        feature['properties']['admin_level'] = value_empty(feature, 'admin_level')
        feature['properties']['disputed'] = value_empty(feature,'disputed')
        feature['properties']['maritime'] = value_empty(feature,'maritime')
        return feature
        