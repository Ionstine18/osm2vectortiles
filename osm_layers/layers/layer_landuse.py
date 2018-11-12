import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_landuse(layers):
    def __init__(self):
        self.layer_type = 'landuse'
        self.data_source = ['osm']
        self.fields = ['class']
    
    def condition(self, feature):
        if feature['geometry']['type'] != 'Polygon':
            return False
        amenity_range = ['bus_station','school','university','kindergarten','college','library','hospital']
        landuse_range = ['railway','cemetery','military','residential','commercial','industrial','retail']
        leisure_range = ['stadium','pitch','playground']
        tourism_range = ['theme_park','zoo']
        amenity = value_empty(feature, 'amenity')
        landuse = value_empty(feature, 'landuse')
        leisure = value_empty(feature, 'leisure')
        tourism = value_empty(feature, 'tourism')
        if amenity in amenity_range:
            return True
        if landuse in landuse_range:
            return True
        if leisure in leisure_range:
            return True
        if tourism in tourism_range:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "landuse" }
        amenity = value_empty(feature, 'amenity')
        landuse = value_empty(feature, 'landuse')
        leisure = value_empty(feature, 'leisure')
        tourism = value_empty(feature, 'tourism')
        cl = ""
        if amenity != "":
            cl = amenity
        elif landuse != "":
            cl = landuse
        elif leisure != "":
            cl = leisure
        else:
            cl = tourism
        feature['properties']['class'] = cl
        return feature
    