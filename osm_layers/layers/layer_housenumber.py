import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_housenumber(layers):
    def __init__(self):
        self.layer_type = 'housenumber'
        self.data_source = ['osm']
        self.fields = ['housenumber']
    
    def condition(self, feature):
        if feature['geometry']['type'] in ['Point','Polygon']:
            if value_empty(feature,'addr:housenumber') != "":
                return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "housenumber" }
        feature['properties']['housenumber'] = value_empty(feature, 'addr:housenumber')
        return feature
