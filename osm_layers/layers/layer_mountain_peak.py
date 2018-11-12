import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_mountain_peak(layers):
    def __init__(self):
        self.layer_type = 'mountain_peak'
        self.data_source = ['osm']
        self.fields = ['name','name_en','name_de','rank','ele','ele_ft']
    
    def condition(self, feature):
        if feature['geometry']['type'] in ['Point']:
            if value_empty(feature,'natural') == "peak":
                return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "mountain_peak" }
        feature['properties']['name'] = name_variable(feature)
        feature['properties']['name_en'] = name_en_variable(feature)
        feature['properties']['name_de'] = name_de_variable(feature)
        ele = value_empty(feature, 'ele')
        feature['properties']['ele'] = ele
        if ele != "":
            feature['properties']['ele_ft'] = str(int(float(ele)*3.66))
        else:
            feature['properties']['ele_ft'] = ""
        return feature

        