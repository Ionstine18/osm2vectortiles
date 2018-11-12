import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_place(layers):
    def __init__(self):
        self.layer_type = "place"
        self.data_source = ['osm']
        self.fields = ['name','name_en','name_de','capital','iso_a2','class','rank']
        
    def condition(self, feature):
        if feature['geometry']['type'] == "Point":
            place_range = ['continent','country','island','state','city','town','village','hamlet','suburb',
                           'neighbourhood','isolated_dwelling']
            if 'name' in feature['properties'].keys():
                place = value_empty(feature, 'place')
                if place in place_range:
                    return True
        if feature['geometry']['type'] == "Polygon":
            place_range = ['island']
            if 'name' in feature['properties'].keys():
                place = value_empty(feature, 'place')
                if place in place_range:
                    return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "place" }
        feature['properties']['name'] = name_variable(feature)
        feature['properties']['name_en'] = name_en_variable(feature)
        feature['properties']['name_de'] = name_de_variable(feature)
        feature['properties']['capital'] = normalize_capital_level(feature)
        ### to add later
        feature['properties']['iso_a2'] = ''
        ### to add later
        feature['properties']['rank'] = ''
        feature['properties']['class'] = value_empty(feature,'place')     
        return feature