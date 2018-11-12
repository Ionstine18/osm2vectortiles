import numpy
import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_park_polygon(layers):
    def __init__(self):
        self.layer_type = 'park_polygon'
        self.data_source = ['osm']
        self.fields = ['class']
    
    def condition(self, feature):
        if feature['geometry']['type'] in ['Polygon']:
            if value_empty(feature,'leisure') == "nature_reserve":
                return True
            elif value_empty(feature, 'boundary') == 'national_park':
                return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "park_polygon" }
        leisure = value_empty(feature,'leisure')
        boundary = value_empty(feature,'boundary')
        cl = ''
        if leisure != "":
            cl = leisure
        else:
            cl = boundary
        feature['properties']['class'] = cl
        return feature