import numpy
import json
from abc import ABCMeta, abstractmethod
import re

from .layers import *
from .functions import *

class layer_highway_linestring(layers):
    def __init__(self):
        self.layer_type = "highway_linestring"
        self.data_source = ['osm']
        self.fields = ['layer','service','level','brunnel','indoor','ramp','subclass','oneway','class']
        
    def condition(self, feature):
        if feature['geometry']['type'] != 'LineString':
            return False
        highway = value_empty(feature,'highway')
        if highway in ['motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary',
                       'secondary_link','tertiary','tertiary_link','unclassified','residential','road',
                       'living_street','raceway','track','service','path','cycleway','bridleway','footway',
                       'corridor','pedestrian','steps']:
            return True
        public_transport = value_empty(feature,'public_transport')
        if public_transport in ['platform']:
            return True
        return False
    
    def update_feature(self, feature):
        feature = feature.copy()
        feature["tippecanoe"] = {"layer" : "highway_linestring" }
        feature['properties']['layer'] = value_empty(feature,'layer')
        feature['properties']['service'] = value_empty(feature,'service')
        feature['properties']['level'] = value_empty(feature,'level')
        feature['properties']['brunnel'] = brunnel(feature)
        feature['properties']['indoor'] = value_empty(feature,'indoor')
        highway = value_empty(feature,'highway')
        if highway_is_link(feature) or highway == 'steps':
            feature['properties']['ramp'] = 1
        elif is_ramp(feature):
            feature['properties']['ramp'] = 1
        else:
            feature['properties']['ramp'] = 0
        hc = highway_class(feature)
        feature['properties']['class'] = hc
        public_transport = value_empty(feature,'public_transport')
        highway = value_empty(feature, 'highway')
        scl = ""
        if (highway != "" or public_transport != "") and hc == "path":
            scl = public_transport if public_transport != "" else highway
        feature['properties']['subclass'] = scl
        oneway = value_empty(feature,'oneway')
        feature['properties']['is_oneway'] = 1 if oneway == 'yes' else 0
        return feature
    