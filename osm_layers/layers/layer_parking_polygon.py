import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_parking_polygon(layers):
    def __init__(self):
        self.layer_type = "parking_polygon"
        self.data_source = ['osm']
        self.fields = ['name','class']
        
    def condition(self, feature):
        if feature['geometry']['type'] not in ['Polygon','MultiPolygon']:
            return False
        amenity = value_empty(feature,'amenity')
        if amenity == 'parking':
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "parking_polygon" }
        feature['name'] = name_variable(feature)
        feature['class'] = 'parking'
        return feature
    