import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_railway_linestring(layers):
    def __init__(self):
        self.layer_type = "railway_linestring"
        self.data_source = ['osm']
        self.fields = ['layer','service','level','brunnel','indoor','ramp','subclass','oneway','class']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'LineString':
            return False
        railway = value_empty(feature,'railway')
        if railway in ['rail','narrow_gauge','preserved','funicular','subway','light_rail','monorail','tram']:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "railway_linestring" }
        feature['properties']['layer'] = value_empty(feature,'layer')
        feature['properties']['service'] = value_empty(feature,'service')
        feature['properties']['level'] = value_empty(feature,'level')
        feature['properties']['brunnel'] = brunnel(feature)
        feature['properties']['indoor'] = value_empty(feature,'indoor')
        if is_ramp(feature):
            feature['properties']['ramp'] = 1
        else:
            feature['properties']['ramp'] = 0
        rc = railway_class(feature)
        feature['properties']['class'] = rc
        railway = value_empty(feature, 'railway')
        feature['properties']['subclass'] = railway
        oneway = value_empty(feature,'oneway')
        feature['properties']['is_oneway'] = 1 if oneway == 'yes' else 0
        return feature
