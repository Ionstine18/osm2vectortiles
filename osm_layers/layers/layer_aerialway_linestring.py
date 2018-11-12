import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_aerialway_linestring(layers):
    def __init__(self):
        self.layer_type = "aerialway_linestring"
        self.data_source = ['osm']
        self.fields = ['layer','service','level','brunnel','indoor','ramp','subclass','oneway','class']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'LineString':
            return False
        aerialway = value_empty(feature,'aerialway')
        if aerialway in ['cable_car']:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "aerialway_linestring" }
        feature['properties']['layer'] = value_empty(feature,'layer')
        feature['properties']['service'] = value_empty(feature,'service')
        feature['properties']['level'] = value_empty(feature,'level')
        feature['properties']['brunnel'] = brunnel(feature)
        feature['properties']['indoor'] = value_empty(feature,'indoor')
        if is_ramp(feature):
            feature['properties']['ramp'] = 1
        else:
            feature['properties']['ramp'] = 0
        ac = value_empty(feature,'aerialway')
        feature['properties']['class'] = ac
        feature['properties']['subclass'] = ""
        oneway = value_empty(feature,'oneway')
        feature['properties']['is_oneway'] = 1 if oneway == 'yes' else 0
        return feature
