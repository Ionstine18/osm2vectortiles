import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_waterway_linestring(layers):
    def __init__(self):
        self.layer_type = "waterway_linestring"
        self.data_source = ['osm']
        self.fields = ['brunnel','name_en','name','name_de','class']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'LineString':
            return False
        waterway = value_empty(feature,'waterway')
        if waterway in ['river','stream','canal','drain','ditch']:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "waterway_linestring" }
        feature['properties']['name'] = name_variable(feature)
        feature['properties']['name_en'] = name_variable(feature)
        feature['properties']['name_de'] = name_variable(feature)
        feature['properties']['brunnel'] = brunnel(feature)
        feature['properties']['class'] = value_empty(feature,'waterway')
        return feature